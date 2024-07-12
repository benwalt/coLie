##################################################################
#
# Data structures and methods for computing with coLie symbols
#  © 2024 Benjamin Walter <benjamin.walter@uvi.edu>
#      (dedicated to the memory of Aydin Ozbek)
#
# Included classes:
#   LieTree( bracket string )
#   EilTree( symbol string  )
#   EilWord( assoc word     )
#   SignedWord( signed word )
#
# See docstrings for more information on use
#
##################################################################

import re   # used for weakly comparing trees 


class ValueTree():
    """ValueTree is class with attributes and methods common to trees of values
    
    Parameters
    ----------
    value : str     (default = "")
          Value for the root vertex of tree (used to generate the rest of tree)
    root  : boolean (default = True)
          Indicates if this is the root vertex (first call) of tree
          
    Attributes
    ----------
    value    : string
          Value of this vertex
    weight   : integer
          Weight (number of edges) supported by vertex
    _branches : list of ValueTrees
          Array of child nodes (subtrees)
    """
    
    
    _pos = 0   # use global position variable when scanning expressions to build trees
    
    
    def __init__(self,root=True):
        self._branches = []   # list of branches out of vertex ("child trees")
        self.value    = ""     # value tree stores a value at each vertex
        self.weight   = -1     # weight is total number of edges supported at vertex
                
        if root:               # if this is not within a recursion
            ValueTree._pos = 0 #  then start reading at the beginning

            
    def __str__(self):
        """String version of tree is value at root"""
        return self.value
    
    
    def __len__(self):
        """weight is number of edges, len is number of vertices"""
        return self.weight + 1
    
    def letters(self):
        """Get letters and multiplicities from tree"""
        return ''.join(sorted(re.sub(r'[/\W+/g]', '', self.value)))
    
    #########################
    # & is 'weak pairing' -- verify that objects use same letters with same multiplicity
    #                        this is used when computing pairings of symbols and Lie brackets
    #
    def __and__(self,other):
        """weak pairing of two objects: compare letters and multiplicity"""
        
        if self.weight != other.weight:                           # check lengths
            return False
        
        for x in list(set(re.sub(r'[/\W+/g]', '', self.value))):  # get list of unique letters
            if not self.value.count(x) == other.value.count(x):   # compare multiplicity of letters
                return False
        return True
    #
    ##########################
    

    
    def __iter__(self):
        """Dept-first iteration"""
        yield self
        
        for branch in self._branches:
            for twig in branch:
                yield twig
                
        # note: maybe better to use chain and imap from itertools???
        #
        # from itertools import chain, imap
        # for node in chain(*imap(iter, self._branches)):
        #     yield node
        # yield self

        
    #################
    #
    #  currently unused methods, but interesting
    #
    def __bool__(self):
        """True if tree is nonempty"""
        return self.weight != -1
       
    
    def __eq__(self,other):
        """trees are equal if values at root are equal"""
        return str(self) == str(other)
    
    
    def __lt__(self,other):
        """ordering is by weight then value"""
        return (self.weight, self.value) < (other.weight, other.value)
    
        
        
##################################################################
##################################################################

   
class LieTree(ValueTree):
    """LieTree is a Lie bracket and tree of subbrackets, used to quickly get left and right subbrackets
    
    Parameters
    ----------
    bracket : string   (default "")
         The Lie bracket to split apart. Use letters for generators, spaces are ignored, commas optional.
    root    : boolean  (default True)
         This parameter is only used interally when recursively building a tree.  DON'T USE IT!
         
    Example
    -------
    bracket = LieTree("[ [a,b] , [ [c,d], e] ]")
    
    
    Attributes
    ----------
    value    : string
         The Lie bracket supported at this node
    weight   : integer
         The weight (number of bracket symbols) of bracket
    bracket  : list of LieTrees
         The left and right subbrackets
    short    : string
         Short version of bracket (don't print ,)
    """

    
    def __init__(self, bracket="", root=True):
        super().__init__(root)
        
        if root:            # on initial call, strip whitespace, comma, and ]
            #                 (assume valid bracket input with single letter entries)
            bracket = re.sub(r'[\],\s]', '', bracket)
     
        if bracket == "":
            return
        
        # read left to right across the bracket expression using the _pos pointer to
        # track where we are looking between recursive calls

        
        if bracket[ValueTree._pos] == "[":   # this node is a bracket of subexpressions
            ValueTree._pos += 1                            # advance past [
            
            self.bracket = [LieTree(bracket,False) , LieTree(bracket,False)] 

        else:                            # this node is a single element
            self.value  = bracket[ValueTree._pos]         # include element
            self.weight = 0
            ValueTree._pos += 1                           # advance to next position
                    

    @property
    def bracket(self):
        return _branches
    
    
    @bracket.setter
    def bracket(self, bracket):
        """"set left and right values of bracket -- only do this at a root!"""
        self._branches = bracket
        self.value = f'[{self._branches[0].value},{self._branches[1].value}]'
        self.weight = 1 + self._branches[0].weight + self._branches[1].weight


    @property
    def left(self):
        """Left subbracket expression"""
        
        if self.weight > 0:
            return self._branches[0]
        
        return None
    
    @property
    def right(self):
        """Right subbracket expression"""
        
        if self.weight > 0:
            return self._branches[1]
        
        return None        
    
    @left.setter
    def left(self, subbracket):
        """set left subbracket -- only do this at the root!"""
        if len(self._branches) == 0:
            self._branches.append(subbracket)
        else:
            self._branches[0] = subbracket
        
        if len(self._branches) == 2 and isinstance(self._branches[1],LieTree):
            self.value  = f'[{self._branches[0].value},{self._branches[1].value}]'
            self.weight = 1 + self._branches[0].weight + self._branches[1].weight
            
    @right.setter
    def right(self, subbracket):
        """set right subbracket -- only do this at the root!"""
        if len(self._branches) == 0:
            self._branches[0] = None
            self._branches.append(subbracket)
        elif len(self._branches) == 1:
            self._branches.append(subbracket)
        else:            
            self._branches[1] = subbracket
        
        if isinstance(self._branches[0],LieTree):
            self.value  = f'[{self._branches[0].value},{self._branches[1].value}]'
            self.weight = 1 + self._branches[0].weight + self._branches[1].weight
        
    
    @property
    def short(self):
        return re.sub(',','', self.value)
    
    @short.setter         # you probably shouldn't change the bracket value of a node
    def short(self,string):
        value = list(string)
        for i in reversed(range(1,len(value))):
            if ((value[i-1].isalpha() and value[i].isalpha()) or
                (value[i-1] == ']'    and value[i].isalpha()) or
                (value[i-1].isalpha() and value[i] == '[')):
                value[i:i] = [',']
        self.value = ''.join(value)
    

    ###################
    #
    # Interesting things that aren't currently used
    #    
    def __mul__(self, other):
        """Overload multiplication to be Lie bracket"""
        
        if isinstance(other, LieTree):
            product = LieTree()
        
            product.bracket = [ self , other ]
            
            return product
        
        return NotImplemented

        
    def __repr__(self):
        return f"LieTree('{self.value}')"


##################################################################
##################################################################

class EilWord():
    """EilWord is a linear coLie symbol <=> associative word
      EilWord objects have multiplication overloaded to perform pairing with Lie brackets and configuration braiding with group elements
    
    Parameters
    ----------
    word : string   (default "")
        This is the linear symbol written as a word Example: abaa <=> (((a)b)a)a

         
    Example
    -------
    word = EilWord("abaab")
    
    
    Attributes
    ----------
    value    : string
         The word
    weight   : integer
         The weight of the corresponding symbol
    symbol   : string
         The symbol corresponding to the associative eil word
    """
    
    
    def __init__(self,word):
        self.value = word
    
    

    def __mul__(self,other):
        """Multiplication is overloaded to compute pairing with Lie brackets and configuration braiding with group elements"""
        
        #########################
        #
        # Pairing with Lie Brackets recursively using bracket-cobracket compatibility from [SiWa]
        #
        if isinstance(other, LieTree):
            
            if not self.__weakPair(self.value,other):  # check weakpairing
                return 0    
            
            return self.__pair(self.value,other)       # recursively comput pairing
        
       
        #########################
        #
        # Counting configuration braidings in words using algorithm from [GOSW]
        #   (This algorithm is originally due to Aydin Ozbek)
        #
        if isinstance(other, SignedWord):        # Algorithm in [GOSW]:
            
            sum   = [0] * len(self.value)        # s value for each eil position
            delta = [0] * len(self.value)        # Δ value for each eil position
            
            for letter in other:                 # pass across the word
                for i in range(len(self.value)): #  evaluating eil symbol from leaf to root
                    
                    sum[i]  += delta[i]          # 1. add Δ value to s value
                    delta[i] = 0                 #    and set Δ to 0 
                    
                    value = 0                    # 2. get value of branches
                    
                    if self.value[i] == letter.value:   # check if update is needed
                        if i == 0:               #    at first vertex there is no branch
                            value = 1 
                        else:                    #    otherwise look at value above
                            value = sum[i-1]
                            
                    if not letter:               # 3. update s and Δ
                        sum[i]  -= value         #    at inverses, immediately update s
                    else:
                        delta[i] = value         #    at generators, update Δ
                        
            return sum[-1] + delta[-1]           # Braiding value is s + Δ at root
        
        
        return NotImplemented
    
    
    
    def __weakPair(self,word,lie):
        """weakPair is used internally to quickly rule out pairings that will be 0
           It only compares multiplicity of letters appearing in word and Lie bracket
           This is the analog of the & operation in ValueTree (which is used for general symbols)
        """
                
        if len(word) != len(lie):                         # compare length
            return False
        
        for x in list(set(word)):                         # get list of unique letters
            if not word.count(x) == lie.value.count(x):   # compare multiplicity of letters
                return False
        return True

    
    
    def __pair(self,word,other):
        """pair is used internally to recursively compute pairings of eil words with Lie brackets
           Pairing is computed by recursively using bracket-cobracket duality. Cobracket of eil words is given by cutting.
           To speed things up, we compare size and letter grading (weakPair) before recursing.  This immediately eliminates most 0 pairings.
        """
        
        if len(word) == 1:                  # Base case!  Length 1 words are just a single generator
            return int(word == other.value) # Check if generators match!
        
        pairing = 0                         # Otherwise we use cobracket-bracket compatibility with pairing [SiWa]
        
        #       < eil , lie > =  < L(eil) , L(lie) > * < R(eil) , R(lie) >
        #                      - < R(eil) , L(lie) > * < L(eil) , R(lie) >
        #
        # where  ]eil[ = sum L(eil) x R(eil)   and    lie = [ L(lie) , R(lie) ]
        
        if self.__weakPair(word[:len(other.left)], other.left):     # before recursing, weakpair start with left 
            pairing += self.__pair(word[:len(other.left)],other.left) * self.__pair(word[len(other.left):],other.right)

        if self.__weakPair(word[:len(other.right)], other.right):   # before recursing, weakpair start with right 
            pairing -= self.__pair(word[:len(other.right)],other.right) * self.__pair(word[len(other.right):],other.left)            

            
        return pairing
    
    
    #####################
    #
    # maybe we should allow eil(lie) instead of just eil * lie ???
    #
    def __call__(self, other):
        return self * other
    
    
    
    def __str__(self):
        return self.value
    
    
    
    ###################
    #
    # Interesting things that aren't currently used
    #
    @property
    def symbol(self):
        n = len(self.value)-2

        symbol = ['('] * (n+1)
        symbol.append(self.value[0])
        for i in range(1,len(self.value)):
            symbol.extend([')',self.value[i]])
                        
        return ''.join(symbol) 

    def letters(self):
        return ''.join(sorted(self.value))
    
    @property
    def weight(self):
        return len(self.value)-1
       
    
    def __len__(self):
        return len(self.value)

    
    def __repr__(self):
        return f'EilWord("{self.value}")'
    
    
    def __eq__(self,other):
        return self.value == other.value
    
    
    def __lt__(self,other):
        return self.value < other.value
    
    
    def cobracket(self):
        """This returns a generator which yields tuples of the cobracket (cutting the word at each position)"""
        return ( (EilWord(self.value[:n]), EilWord(self.value[n:]))  for n in range(1, len(self.value)) )
    
    
##################################################################
##################################################################

class EilTree(ValueTree):
    """EilTree encodes the tree structure of a coLie symbol
      EilTre objects have multiplication overloaded to perform pairing with Lie brackets and configuration braiding with group elements
    
    Parameters
    ----------
    symbol : string   (default "")
         The symbol to split apart. Use letters for generators, spaces are ignored.
    root   : boolean  (default True)
         This parameter is only used interally when recursively building a tree.  DON'T USE IT!
         
    Example
    -------
    symbol = EilTree("( ((a)(b)b) (b ((a)b)) a)")
    
    
    Attributes
    ----------
    value      : string             (default: "")
         The symbol supported at this node
    decoration : string             (default: "")
         The free variable of the symbol (at the given node)
    weight     : integer            (default: -1)
         The weight (number of parenthesis pairs) of symbol (supported by the given node)
    subsymbols : list of EilTree's  (default: [])
         The immediate subsymbols of the given symbol
    normalValue : string
         A "normalized" version of the symbol -- move free variables to right, etc
    """
    
    def __init__(self, symbol="", root=True):
        super().__init__(root)
        
        self.decoration = ""     # keep track of decoration for each vertex

        if root:                 # on initial call, strip whitespace
            symbol = symbol.translate(str.maketrans('', '', ' \n\t\r'))
            
        if symbol == "":
            return
 
        # read left to right across the symbol expression using the _pos pointer to
        # track where we are looking between recursive calls

        start = ValueTree._pos           # this is the staring position for the subsymbol
        
        while ValueTree._pos < len(symbol) and not symbol[ValueTree._pos] == ")":
            
            if symbol[ValueTree._pos] == "(":            # begin a subsymbol
                ValueTree._pos  += 1                       # advance into subsymbol
                self._branches.append(EilTree(symbol,False))# append new subtree
                
            else:                                        # this is free variable (decoration of vertex)
                self.decoration = symbol[ValueTree._pos]   # record free variable
                ValueTree._pos += 1                        # advance past
                
        end = ValueTree._pos             # this is the ending position for the subsymbol
        
        self.value = symbol[start:end]   # this is the current subsymbol
        
        self.weight = sum([branch.weight + 1 for branch in self.subsymbols])
        # self.weight = self.value.count('(')            # this is equivalent but probably slower?

        ValueTree._pos += 1      # advance past the closing of subsymbol

        

    def __mul__(self, other):
        """Multiplication is overloaded to compute pairing with Lie brackets and configuration braiding with group elements"""
        
        #########################
        #
        # Pairing with Lie Brackets recursively using bracket-cobracket compatibility from [SiWa]
        #   
        if isinstance(other, LieTree):
            
            if not self & other:       # check weakpairing
                return 0    
            
            return self.__pair(other)  # recursively compute pairing
  

        #########################
        #
        # Counting configuration braidings in words using algorithm from [GOSW]
        #
        if isinstance(other, SignedWord):
            counter = CountTree(self)    # analog of sum and delta arrays for EilWord
            
            for letter in other.word:
                counter.evaluate(letter) # evaluate the counter on each letter in the word
                
            return counter.total         # this is s + Δ at root
            
        
        return NotImplemented
    
    
    
    def __pair(self, other):
        """pair is used internally to recursively compute pairings of eil symbols with Lie brackets
           Pairing is computed by recursively using bracket-cobracket duality. 
           Cobracket of symbols is given by cutting out a subtree, yielding sub and excised trees.
           To speed things up, we compare size and letter grading (weakPair) before recursing.  This immediately eliminates most 0 pairings.
        """        
        
        if self.weight == 0:            # Base case! Symbol is a single character 
            return int(self.value == other.value)   # compare vs Lie value
        
        pairing = 0          # Otherwise we use cobracket-bracket compatibility with pairing [SiWa]
        
        #       < eil , lie > =  < L(eil) , L(lie) > * < R(eil) , R(lie) >
        #                      - < R(eil) , L(lie) > * < L(eil) , R(lie) >
        #
        # where  ]eil[ = sum L(eil) x R(eil)   and    lie = [ L(lie) , R(lie) ]
        #    L(eil) is subsymbol
        #    R(eil) is result of excising subsymbol
        
        for subsymbol in self:           # iterate through all subsymbols of symbol
            if subsymbol & other.left:   #   weakpair with subsymbol first, since excised symbol requires computation
                pairing += subsymbol.__pair(other.left) * self.__excise(subsymbol).__pair(other.right)
            
            if subsymbol & other.right:  #   weakpair with subsymbol first, since excised symbol requires computation
                pairing -= subsymbol.__pair(other.right) * self.__excise(subsymbol).__pair(other.left)
            
        return pairing
    
        # Note: this might be sped up by sorting subsymbols by weight initially rather than searching for weights matching other.left and other.right
                
               
        
       
    def __excise(self, subsymbol):  
        """excise is used internally to compute the symbol remaining after a subsymbol is removed
           It recursively copies a tree, skipping the excised subsymbol (and its supported subtree).
        """
        
        #if self is subsymbol:  # This should never happen during internal recursive usage!
        #    return EilTree()   
        
        eil = EilTree()        # Begin with a blank node
        
        eil.decoration = self.decoration # copy the decoration
        
        if self.weight == 0:   # Direct copy if this is a leaf node
            eil.weight = 0
            eil.value  = self.value
            
        else:    
            eil.subsymbols = [symbol.__excise(subsymbol) for symbol in self.subsymbols if not symbol is subsymbol]          
            
        return eil
    
    @property
    def subsymbols(self):
        return self._branches
    
    @subsymbols.setter
    def subsymbols(self, list):
        self._branches = list
        self.value = ''.join([f'({str(branch)})' for branch in self._branches]+[self.decoration])
        self.weight = sum([branch.weight + 1 for branch in self._branches])
       
        # self.weight = self.value.count('(')  # this should be equivalent, but probably slower?
 

    # I like to write free elements last, so append() and extend()  will actually insert at start...
    def append(self, subsymbol):
        """Insert new subsymbol, updating weight and value"""
        self._branches[:0] = [subsymbol]                  # insert subsymbol at start
        self.weight += subsymbol.weight+1                 # add to weight
        self.value   = f'({subsymbol.value}){self.value}' # add to value 
        
    def extend(self, subsymbols):
        """Insert array of subsymbols, updating weight and value"""
        self._branches[:0] = subsymbols
        self.weight += sum([symbol.weight+1 for symbol in subsymbols])
        tmp          = ')('.join([symbol.value for symbol in subsymbols])
        self.value   = f'({tmp}){self.value}'

    def copy(self):
        """Create a deep copy of EilTree"""
        eil = EilTree()
        eil.decoration = self.decoration
        eil.value , eil.weight = self.value , self.weight
                
        if len(self._branches) > 0:
            eil._branches = [subsymbol.copy() for subsymbol in self._branches]
        
        return eil
 

    ###################
    #
    # Interesting things that aren't currently used
    #
    @property
    def normalValue(self):       # the normal Value has free terms written last
        if self.weight == 0:     #  this should probably also sort branches nicely
            return self.value    #  define < used for sorting later....
        
        return ''.join([f'({branch.normalValue})' for branch in sorted(self._branches,reverse=True)]+[self.decoration])
 

    
    def normalize(self):
        """Convert EilTree to 'normalized' form -- sort branches and move free letter to the far right"""
        for symbol in self._branches:    
            symbol.normalize()
            
        #self.value = ''.join([f'({str(branch)})' for branch in sorted(self.branches,reverse=True)]+[self.decoration])
        self.subsymbols = [branch for branch in sorted(self._branches,reverse=True)]
     
    
    def __eq__(self,other):               # compare normalized forms so (a)b == b(a)
        if isinstance(other, EilTree):    #   Note: isn't perfect...
            return self.normalValue == other.normalValue
        
        return False
  

    # < is used when writing in normal form and comparing EilTrees
    def __lt__(self,other):
        if self.value == other.value:     # if values match then these are equal
            return False
        
                                          # next sort by weight and decoration
        if (self.weight,self.decoration) < (other.weight,other.decoration):
            return True
        if (self.weight,self.decoration) > (other.weight,other.decoration):
            return False
        
                                          # next sort by number of branches
        if len(self.subsymbols) < len(other.subsymbols):
            return True
        if len(self.subsymbols) > len(other.subsymbols):
            return False
        
                                           # next look at decorations and weights of branches
        return sorted([(branch.decoration,branch.weight) for branch in self.subsymbols]) < sorted([(branch.decoration,branch.weight) for branch in other.subsymbols])
    
        # note: this may incorrectly sort a(a(b)) and a(a(c))
    
    
        
    def __gt__(self,other):
        return other < self
        
        
    def __repr__(self):
        return f"EilTree('{self.value}')"        
    
    
    
    ################
    #
    # allow eil(lie) instead of just eil * lie
    #
    def __call__(self, other):
        return self * other

    
    def cobracket(self): 
        """returns a generator with tuples of cobracket elements"""
        subsymbols = iter(self)
        next(subsymbols)    # the first term in the iterator is the entire symbol (skip it)
        
        return ((subsymbol,self.__excise(subsymbol)) for subsymbol in subsymbols)
    
##################################################################
##################################################################


class CountTree():
    """CountTree is a helper class for combinatorial braiding of coLie symbols on words.
    This copies the structure of an EilTree and takes the place of the 'sum' and 'delta' arrays that were used in the __mul__ method of EilWord. 
    
    Objects of this class should only be used internally!
    
    Parameters
    ----------
    eil : EilTree
       corresponding node of an EilTree
       
    Attributes
    ----------
    sum      : integer
       current s value for this node (initialized to 0)
    delta    : integer
       current Δ value for this node (initialized to 0)
    branches : list of CountTree's
       list of branches from this node
    eil      : EilTree
       corresponding node of the EilTree
    total    : integer
       sum + delta
    """
    
    
    def __init__(self,eil):
        self.sum   = 0
        self.delta = 0
        self.eil   = eil
        
        self.branches = [CountTree(branch) for branch in eil.subsymbols]
        
        
    @property 
    def total(self):
        return self.sum + self.delta
    
    
    def evaluate(self,letter):
        """evaluate updates values of the counter tree at the given letter following the algorithm outlined in [GOSW]
           Compare to the use of 'sum' and 'delta' arrays in the __mul__() method of EilWord.
        """
        
        
        for branch in self.branches:    # Evaluate leaf to root
            branch.evaluate(letter)     #   (update branch values first)   
            
        self.sum  += self.delta         # 1. add Δ to s
        self.delta = 0                  #    and set Δ = 0
        
        value = 0                       # 2. incorporate values from branches
 
        if letter.value == self.eil.decoration: # check if update is needed
            if len(self.branches) == 0: #    at leaf just copy the value
                value = 1
            else:                       #    otherwise add values from branches
                value = sum([branch.sum for branch in self.branches])
            
            
        if not letter:                  # 3. at inverses, immediately update s
            self.sum   -= value
        else:                           #    otherwise, update Δ
            self.delta  = value
        
 

    ###################
    #
    # Interesting things that aren't currently used
    #
    def __iter__(self):
        for branch in self.branches:
            for twig in branch:
                yield twig          
        yield self



##################################################################
##################################################################


class SignedLetter():
    """SignedLetter is a letter with a sign, intended to represent a generator or an inverse
     * as a boolean it is True for generator and False for inverse
     * as an integer it is 1 for generator and -1 for inverse
     * as a string it looks pretty
    
    Parameters
    ----------
    letter : string
        this should be a single character
    sign   : boolean or integer
    
    Examples: 
      SignedLetter("a",False)
      SignedLetter("a",-1)
    
    Attributes
    ----------
    value : string
        this is the letter
    sign  : boolean
        True corresponds to generator
        False correspnds to inverse
    
    """
    def __init__(self,letter,sign):
        self.value = letter
        self.sign  = True if sign == 1 else False
    
    def __bool__(self):
        return self.sign
    
    def __int__(self):
        return 1 if self.sign else -1
    
    def __str__(self):
        return f'{self.value}' if self.sign else f'{self.value}\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}'


##################################################################


class SignedWord():
    """SignedWord is a list of SignedLetters
    
    Parameters
    ----------
    word : string or list
    
    Examples: 
     SignedWord("aba^{-1}b^{-1}")
     SignedWord("aba-b-")
     SignedWord( [ ("a",1), ("b",1), ("a",-1), ("b",-1) ] )
    
    Attributes
    ----------
    word : list of SignedLetters
    """
    def __init__(self,word):
        self.word = []
        
        if isinstance(word, str):
            i = 0
            while i < len(word):
                if i+1 < len(word) and (word[i+1] == "-" or word[i+1] == "^"):
                    self.word.append(SignedLetter(word[i],-1))
                else:
                    self.word.append(SignedLetter(word[i], 1))
                i += 1
                
                while i < len(word) and not word[i].isalpha():
                    i += 1
        elif isinstance(word, list):
            if isinstance(word[0], SignedLetter):
                self.word = word
            else:    
                self.word = [SignedLetter(x[0],x[1]) for x in word]
        else:
            raise ValueError("Word format not recognized!")
            

    def __len__(self):
        return len(self.word)
            
    def __str__(self):
        return ''.join([str(x) for x in self.word])
        
    def __iter__(self):
        return iter(self.word)      

    def letters(self):
        return ''.join(sorted(set([letter.value for letter in self.word])))
    
##################################################################
