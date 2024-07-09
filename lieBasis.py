##################################################################
#
# Functions for generating Lyndon(-Shirshov) words as well as Lie and coLie bases
#  © 2024 Benjamin Walter <benjamin.walter@uvi.edu>
#
# Included functions:
#   gen_LS( word )
#
#   bracketStd(  LS-word )
#   bracketLeft( LS-word )
#   bracketRight(LS-word )
#   bracketCfg(  LS-word )
#   bracketChib( LS-word )
#
#   symbolsStar( LS-word )
#
# See docstrings for more information on use
#
##################################################################


import math   # Duval's algorithm genLS_old() uses math.ceil()

#######################################################################
#######################################################################
def genLS_old(word):
    """Use Duval's algorithm (1988) to generate all Lyndon(-Shirshov) words using given alphabet and multiplicities
       Duval's algorithm generates all words of a given length.  We ignore words with incorrect multiplicities.
    """
    
    # create alphabet = list of (letter,count) pairs
    alphabet = sorted(list(set(word)))
    count    = [word.count(letter) for letter in alphabet]

    
    if alphabet == []:
        return
    
    N = len(word)
   
    LSWord = [alphabet[0]]
    
    # apply algorithm from Duval (1988)
    
    while LSWord != []:
        if len(LSWord) == len(word) and all([LSWord.count(l)==n for l,n in zip(alphabet,count)]):
            yield(''.join(LSWord))
            
        LSWord = LSWord * math.ceil(N/len(LSWord))
                
        n = N-1
        
        while n >= 0 and LSWord[n] == alphabet[-1]:
            n -= 1
            
        LSWord = LSWord[:n+1]
        
        if n >= 0:
            LSWord[n] = alphabet[alphabet.index(LSWord[n])+1]
            
    return


#######################################################################
# An alternate algorithm is given by Cattell et al (2000) 
#   https://www.cis.uoguelph.ca/~sawada/papers/un.pdf
#
# This seems to be about the same speed as Duval's algorithm
#
def genLS_all(word, t=1, p=1, N=None, K=None, root=True, LSWord=None):
    """Cattell et al (2000) algorithm generating all LS words of a given length
       Running time is similar to Duval (1998)
    """
    if root:
        N = len(word)
        if N < 2:
            yield word
        
        LSWord = [0] * (N + 1)    # Cattell's algorithm uses 1-indexing... ugh
        word   = sorted(list(set(word)))  # later iterations need alphabet
        K      = len(word)
        
        
    if t > N:
        if p == N:
            yield(''.join(word[num] for num in LSWord[1:]))
    else:
        LSWord[t] = LSWord[t-p]
        yield from genLS_all(word, t+1, p, N, K, False, LSWord)
        
        for j in range(LSWord[t-p]+1, K):
            LSWord[t] = j
            yield from genLS_all(word, t+1, t, N, K, False, LSWord)


#######################################################################
#######################################################################            
# It is possible to modify this algorithm to generate only words with specific multiplicies of letters
#  below is modification of Joe Sawada's C code (2019) available at http://combos.org/necklace
#
# This is considerably faster than generating everything and throwing out ones with wrong multiplicity
#
# We use a linked list to track multiplicity and availability of letters in the alphabet
#  Once all of a letter's multiplicity is used up, we modify the linked list to skip it
# As we build a LS word, the alphabet linked list will be continually updated adding and removing letters
#
######################################################
# The LListElement class has attributes
#   value = multiplicity of an letter
#   index = index of the letter
#   prev  = previous element in alphabet
#   next  = next element in alphabet
###########################################################
class LListElement:
    def __init__(self,value=0,index=0,n=None,p=None):
        self.value , self.index = value , index
        self._prev , self._next = p , n
        
    def __bool__(self):
        return self.value != 0

#######################################################
# The ValuedList class will be used to store the alphabet
# Attributes:
#   _nodes = array containing all linked list elements 
#   head   = first available element in alphabet 
#
# Methods:
#   mult(n)      = remaining multiplicity of letter n
#   decrement(n) = lowers available multiplicity of n (and maybe removes from alphabet)
#   increment(n) = raises available multiplicity of n (and maybe reinserts in alphabet)
#   nextval(n)   = get next available letter (after n)
###########################################################
class ValuedLList:
    def __init__(self,count):
        if len(count) < 1:
            return
         
        self._nodes  = [LListElement(count[0])]
        for n in range(1,len(count)):
            self._nodes.append(LListElement(count[n],n,self._nodes[n-1]))
            self._nodes[n-1]._prev = self._nodes[n]
            
        self.head = self._nodes[-1]
    
    def mult(self,n):
        return self._nodes[n].value
    
    def decrement(self,n):
        self._nodes[n].value -= 1
        
        if not self._nodes[n]:
            if self.head == self._nodes[n]:
                self.head = self._nodes[n]._next
                
            if self._nodes[n]._next:
                self._nodes[n]._next._prev = self._nodes[n]._prev
            if self._nodes[n]._prev:
                self._nodes[n]._prev._next = self._nodes[n]._next

    def increment(self,n):
        if not self._nodes[n]:
            if self._nodes[n]._next:
                self._nodes[n]._next._prev = self._nodes[n]
            if self._nodes[n]._prev:
                self._nodes[n]._prev._next = self._nodes[n]
            else:
                self.head = self._nodes[n]
                
        self._nodes[n].value += 1

    def nextval(self,n):
        if self._nodes[n]._next:
            return self._nodes[n]._next.index
        return -1
    
###########################################################
# TODO:  allow alphabet with multiplicity to be specified in other ways
#
#  currently:   "aaabbbcc"
#  also allow:  [ ("a",3) , ("b",3) , ("c",2) ]  
#      (dictionary, list of tuples, list of lists)
###########################################################
def genLS(word, t=2, p=1, s=2, N=None, K=None, root=True, LSWord=None, count=None, tmp=None):
    """genLS(word)  is generator for Lyndon-(Shirshov) words with a given grading
       Words are generated with the same multiplicities of letters as the input word
       Words are generated in reverse lexicographic order!
       
       Example: genLS("aaabbc") will generate all LS words with 3x 'a', 2x 'b', and 1x 'c'
        --> 'ababac', 'aacbab', 'aacabb', 'aabcab', 'aabbac', 'aabacb', 'aababc', 'aaacbb', 'aaabcb', 'aaabbc'
    """
    if root:
        N = len(word)
        if N < 2:
            yield word
        
        tmp    = sorted(list(set(word)))
        count  = ValuedLList([word.count(letter) for letter in tmp])
        word   = tmp              # later iterations need alphabet
        K      = len(word)
        LSWord = [K-1] * (N + 1)    # Cattell's algorithm uses 1-indexing... ugh
        tmp    = [0] * (N + 1)
        
        LSWord[1] = 0             # Cattell's algorithm uses 1-indexing... ugh
        count.decrement(0)
        
    if count.mult(-1) == N-t+1:
        if count.mult(-1) == tmp[t-p] and N == p:
            yield(''.join(word[num] for num in LSWord[1:]))
        elif count.mult(-1) > tmp[t-p]:
            yield(''.join(word[num] for num in LSWord[1:]))
            
    elif count.mult(0) != N-t+1:
        j = count.head.index
        ss = s
        while j >= LSWord[t-p]:
            tmp[s]    = t-s
            LSWord[t] = j
            
            count.decrement(j)
            
            if j != K-1:
                ss = t+1
            if j == LSWord[t-p]:
                yield from genLS(word,t+1,p,ss,N,K,False,LSWord,count,tmp)
            else:
                yield from genLS(word,t+1,t,ss,N,K,False,LSWord,count,tmp)
                
            count.increment(j)
            
            j = count.nextval(j)
            
        LSWord[t] = K-1



#######################################################
#######################################################
#  Lyndon words are minimal in their cyclic ordering class
#   usually we use lexicographic ordering
#   alternately we could use deg-lex ordering
###########################################################
def genDL():
    passs

    
#######################################################################
#######################################################################



#######################################################################
# Code below makes Lie bases from LS words using different rules      #
#                                                                     #
# Most of this code is directly translated from my old Javascript     # 
#  code from 2015 without any optimazation or cleaning....            #
#    (see pairing.html)                                               
#######################################################################


############################################################
# This makes the classical bracketing on an LS word - recursively defined as
#    B(w) = [ B(a) , B(b) ]  where w = ab and b is a maximal LS subword
#
# There are two standard approaches to making this bracketing --
#   Inside->out (inductive): finding the inner-most bracket first  
#                                (look for "right-most inversion")
#   Outside->in (recursive): finding outer-most bracket first
#                                (look for largest Lyndon suffix)
#
#  ... the code below is outside-in... this looks unnecessarily complex??? oh well.
###########################################################
def bracketStd(word):
    """Convert Lyndon word to standard Lie bracketing.
       The standard bracketing is defined as B(w) = [ B(a) , B(b) ] where w=ab and b is the maximal proper LS suffix.
    """
    if len(word) == 1:
        return LieTree(word)
    
    end = len(word)-1
    newprefix , myprefix = 1 , 0     # number of times initial letter is repeated
    split = end
    
    repeat = True
    
    for j in range(end-1, 0, -1):
        if repeat:                     # if current word is repeating suffix
            if word[j] == word[end]:   # if repeat continues
                end -= 1               #   move repeat pointer 
            else:
                repeat = False         # no longer repeating suffix
                end = len(word) - 1    #   reset repeat pointer
                
        if word[j] < word[split]:       # found new low -- better suffix start!
            newprefix , myprefix = 1 , 1
            split = j
            repeat = True               # start checking for repeats again
            
        elif word[j] > word[split]:     # not a possible Lyndon suffix start!
            myprefix = 0                # reset repeats to 0
            
        else:                        # possible cutpoint! (word[j] == word[split])
            myprefix += 1            #  count # repeating letters at cutpoint
                
            if not repeat:
                if myprefix == newprefix: # compare new cutpoint to old cutpoint
                    i = 1
                    while split+i < len(word) and word[j+i] == word[split+i]:
                        i += 1
                    if split+i < len(word) and word[j+i] < word[split+i]:
                        split  = j
                        repeat = True
                elif myprefix > newprefix: # found longer prefix -- new cutpoint
                    newprefix = myprefix
                    split = j
                    repeat = True                             
                
    
    bracket = LieTree()
    bracket.bracket = [ bracketStd(word[:split]) , bracketStd(word[split:]) ]
    
    return bracket  



#########################################################
# see also algorithm by Sawada and Ruskey (2002) .. generating words and brackets at same time
#  https://webhome.cs.uvic.ca/~ruskey/Publications/LieBasis/LieBasis.pdf
#          Journal of Algorithms 46 (2003) 21-26
#
# algorithm is implemented in C at http://combos.org/necklace
##########################################################



###########################################################
# code below is translated from my javascript code
#
# Note: this is a basis by [WaSh15] and pairs diagonally with the star basis for symbols!!!
# 
# TODO: modify this so that it will also left-greedy bracket non-Lyndon words!
###########################################################
def bracketLeft(word):
    """Convert Lyndon word to left-greedy bracketing as described in Walter-Shiri"""
    if len(word) <= 1:
        return LieTree(word)
    
    i , j = 0 , 1

# Idea:  look for repeated subword in topmost partition  ww..wx
#  by moving two pointers across the word and looking for repetitions

# current code requires word to be LS. more general version?
#
#    while j < len(word)-1 and word[i] <= word[j]: # 2nd condition only needed for deg-lex words?
    while j < len(word)-1:                         # 2nd condition never fails for LS words.
        if word[i] == word[j]:
            i += 1
        else:
#            if word[i] > word[j]:    # test necessity of 2nd condition
#                print("oops") 
            i = 0
        j += 1
    
    bracket = LieTree()
    bracket.bracket = [ bracketLeft(word[:j-i]) , bracketLeft(word[j-i:]) ]
    
    return bracket



###########################################################
# code below is translated from my old javascript code
#
# I'm pretty sure this is a basis, but I don't remember if I/anyone ever proved it....
#
# TODO: verify whether this will right-greedy bracket non-Lyndon words!
###########################################################
def bracketRight(word):
    """Convert Lyndon word to right-greedy bracketing"""
    return bracketRG(list(word))

def bracketRG(word):
    if len(word) == 1:
        return word[0] if isinstance(word[0],LieTree) else LieTree(word[0])

    newWord = []
    
    i = 1
    while i < len(word):
        subbracket = bracketRG([word[i-1]])
        
        while i < len(word) and str(word[i]) != str(word[0]):
            tmpbracket = LieTree()
            tmpbracket.bracket = [ bracketRG([subbracket]) , bracketRG([word[i]]) ]
            subbracket = tmpbracket
            i += 1
        
        newWord.append(subbracket)
        i += 1
        
    return bracketRG(newWord)



###########################################################        
# "Configuration basis"  This is a basis by:
#   B. Walter.  The configuration basis of a Lie algebra and its dual
#      https://arxiv.org/abs/1010.4765
#
# this is a direct translation of my javascript code to python
###########################################################
def bracketCfg(word):
    """Convert Lyndon word to Configuration bracketing as described by Walter"""
    return LieTree(bracketConfig(list(word)))


def bracketConfig(word):
    if len(word) == 1:
        return word[0]
    
    newWord = []
    
    start , i = 0 , 1 
    
    while i < len(word):
        bracket = ['[', word[start] ]
        
        while word[i] == word[0]:
            bracket.extend([ ',[' , word[i] ])
            i += 1
        bracket.extend(["," , word[i]])
        bracket.extend(["]"] * (i-start))
                
        i += 1
        while i < len(word) and word[i] != word[0]:
            bracket.insert(0, '[')
            bracket.extend([',' , word[i] , ']'])
            i += 1
            
        newWord.append(''.join(bracket))
                
        start = i
        i += 1
        
    return bracketConfig(newWord)
    


###########################################################
# "right normed" basis of Chibrikov:
#   https://core.ac.uk/download/pdf/82357333.pdf
#
# this is a direct translation of my javascript code to python
###########################################################
def bracketChib(word):
    """Convert Lyndon word to Chibrikov's 'right-normed' bracketing"""
    return LieTree(bracketChibrikov(list(word)))

def bracketChibrikov(word):
    if len(word) == 1:
        return word[0]
    
    newWord = []
    
    end , i = len(word)-1 , len(word)-2     

    while i>=0:
        bracket = [word[end], ']']
        
        while word[i] != word[0]:
            bracket.insert(0,']')
            bracket.insert(0,word[i])
            i -= 1

        bracket.insert(0,word[i])
        
        while end > i:
            bracket.insert(0,'[')
            end -= 1
        
        i -= 1
        while i >= 0 and word[i] == word[0]:
            bracket.insert(0,word[i])
            bracket.insert(0,'[')
            bracket.append(']')
            i -= 1
            
        newWord.insert(0,''.join(bracket))
        
        end = i
        i -= 1
        
    return bracketChibrikov(newWord)


#######################################################################
#######################################################################

###########################################################
# code below is modification of bracketLeft() code
#
# Note: this is a basis by [WaSh15] and pairs nicely with the leftGreedy basis for Lie algebras
###########################################################
def symbolStar(word):
    """Convert Lyndon word into coLie star symbol.  See [Walter-Shiri]"""
    if len(word) <= 1:
        return EilTree(word)
    
    i , j = 0 , 1
    N = len(word)
    
    # look for repeated subword in topmost partition  ww..wx
    #  by moving two pointers across the word and looking for repetitions
    #
    while j != N-1:    # current code requires word to be LS. more general version?
        if word[i] == word[j]: 
            i += 1
        else:
            i = 0
        j += 1
    
    k = j - i       # width of subword w in top partition ww..wx
    
    subsymbols = [symbolStar(word[:k])]  # this is subword w
    
    n = k         
    while n < N-k:  # attach repetitions of subword (if any)
        subsymbols[:0] = [subsymbols[0].copy()]
        n += k
    
    symbol = symbolStar(word[n:]) # this is the suffix word x
    symbol.extend(subsymbols)     # stick the w's onto the x
    
    return symbol
    
#######################################################################
#######################################################################    

def bracket_to_left(bracket,short=False):
    """Use orthogonal projection and star symbols to write Lie brackets in terms of Left-Greedy Basis
       
       Arguments:
       ----------
        bracket : string or LieTree
           Lie bracket expression to convert
        short   : boolean  [False]
           Write output brackets in 'short form' (i.e. without ,)
           
       Result:
       -------
        dictionary { bracket : coefficient }
           
    """
    if not isinstance(bracket,LieTree):
        bracket = LieTree(bracket)
    
    result = dict()
    
    for word in genLS(bracket.letters()):
        eil, lie = symbolStar(word) , bracketLeft(word)
        
        coeff = (eil * bracket) / (eil * lie)
        
        if coeff != 0:
            if short:
                result[lie.short] = int(coeff)
            else: 
                result[str(lie)] = int(coeff)
            
    return result

#######################################################################
#######################################################################  