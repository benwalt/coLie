This code is dedicated to the memory of Aydin Ozbek.

--------------------------------------------------------------------------------

This project contains Python / Sage code for working with Lie coalgebras and algebras.  

Code is present both as python .py files and as jupyter notebook .ipynb files.
The jupyter notebooks give explanations and small examples using included objects 
and functions to make computations.

--------------------------------------------------------------------------------

Some of the algebra-coalgebra algorithms present were first coded by me in javascript 
(see included pairing.html file from 2015).  

The letter braiding computations in EilWord and EilTree are based off work by Aydin Ozbek 
 -  https://github.com/AydinOzbek/Hopf_Invariants

The Lyndon word generation algorithm I use is based off of C code by Joe Sawada 
 -   http://combos.org/necklace

---------------------------------------------------------------------------------

File listing:
-------------
git files:
  CITATION.cff -- git citation information
  LICENSE      -- GPL v2.0
  README.md    -- this file

Jupyter Python Notebooks:
  coLie.ipynb     -- objects for Lie brackets, coLie symbols, signed words
  lieBasis.ipynb  -- functions creating LS words, making Lie bracket bases, 
                     and coLie symbol bases

Python:
  coLie.py        -- Python code from coLie.ipynb
  lieBasis.py     -- Python code from lieBasis.ipynb

Javascript (HTML):
  pairing.html    -- javascript code from 2015 making LS words, Lie bracket bases,
                     computing pairing matrices, and checking for invertibility


---------------------------------------------------------------------------------

These algorithms are based off of theory present in:

Lie algebra - coalgebra pairings:
  * D. Sinha and B. Walter. Lie coalgebras and rational homotopy theory, I: Graph coalgebras
     -  https://arxiv.org/abs/math/0610437
  * D. Sinha and B. Walter. Lie coalgebras and rational homotopy theory II: Hopf invariants
     -  https://arxiv.org/abs/0809.5084

Bases of Lie coalgebras / Lie algebras
   * B. Walter and A. Shiri. The left-greedy Lie algebra basis and star graphs
     -   https://arxiv.org/abs/1510.06984
   * B. Walter.  The configuration basis of a Lie algebra and its dual
     -   https://arxiv.org/abs/1010.4765
   * B. Walter.  The Lie algebra configuration pairing
     -   https://arxiv.org/abs/1010.4732
   * E.S. Chibrikov.  A right normed basis for free Lie algebras and Lyndon–Shirshov words
     -   https://core.ac.uk/download/pdf/82357333.pdf 

Letter braiding and group elements
   * N. Gadish, A. Ozbek, D. Sinha, B. Walter. Infinitesimal calculations in fundamental groups
     -   https://arxiv.org/abs/2403.20264


Further reading:

   * N. Gadish. Letter-braiding: a universal bridge between combinatorial group theory and topology
     -   https://arxiv.org/abs/2308.13635
 
