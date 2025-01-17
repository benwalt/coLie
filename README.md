Description:
------------
This project contains Python / Sage code for working with Lie coalgebras and algebras.  

Code is present both as python .py files and as jupyter notebook .ipynb files.
The jupyter notebooks give explanations and small examples using included objects 
and functions to make computations.

TODO: Implement code for non-free Lie algebras and groups.

--------------------------------------------------------------------------------

File listing: 
-------------
**github files:**
* **CITATION.cff** -- git citation information
* **LICENSE**      -- GPL v2.0
* **README.md**    -- this file

**Jupyter Python Notebooks:**  (Links to [CoCalc](https://cocalc.com/) jupyter notebooks)
* [**coLie.ipynb**](https://cocalc.com/share/public_paths/f04fa33762daab5f18dd3d064d9cce9a184a9a49)     -- objects for Lie brackets, coLie symbols, signed words
* [**lieBasis.ipynb**](https://cocalc.com/share/public_paths/ccde0bda31c37b3eef778f4b384d30f93cc45b5d)  -- functions creating LS words, making Lie bracket bases, 
                     and coLie symbol bases

**Python:** 
* **coLie.py**        -- Python code from coLie.ipynb
* **lieBasis.py**     -- Python code from lieBasis.ipynb

**Javascript (HTML):**
* **pairing.html**    -- javascript code from 2015 making LS words, Lie bracket bases,
                     computing pairing matrices, and checking for invertibility

---------------------------------------------------------------------------------

Acknowledgments:
---------------
*Dedicated to the memory of Aydin Ozbek*

Some of the algebra-coalgebra algorithms present were first coded by me in javascript 
(see included pairing.html file from 2015).  

The letter braiding computations in EilWord and EilTree are based off work by Aydin Ozbek 
 -  https://github.com/AydinOzbek/Hopf_Invariants

The Lyndon word generation algorithm I use is based off of C code by Joe Sawada 
 -   http://combos.org/necklace

---------------------------------------------------------------------------------

References:
-----------
These algorithms are based off of theory present in the following papers.

**Lie algebra - coalgebra pairings.**  *(using graphs for coLie)*
  * D. Sinha and B. Walter. Lie coalgebras and rational homotopy theory, I: Graph coalgebras
     -  https://arxiv.org/abs/math/0610437
  * D. Sinha and B. Walter. Lie coalgebras and rational homotopy theory II: Hopf invariants
     -  https://arxiv.org/abs/0809.5084
  * B. Walter.  The Lie algebra configuration pairing
     -   https://arxiv.org/abs/1010.4732

**Letter braiding and group elements.**  *(introduces symbols for coLie!)*
   * N. Gadish, A. Ozbek, D. Sinha, B. Walter. Infinitesimal calculations in fundamental groups
     -   https://arxiv.org/abs/2403.20264
   * B. Walter. AlgTopPR2024 [conference presentation slides](https://drive.google.com/file/d/1-WLMc-cmm1w-P_ho8z-kwnvECii2lLib/view)
    
**Bases of Lie coalgebras / Lie algebras.**
   * B. Walter and A. Shiri. The left-greedy Lie algebra basis and star graphs
     -   https://arxiv.org/abs/1510.06984
   * B. Walter.  The configuration basis of a Lie algebra and its dual
     -   https://arxiv.org/abs/1010.4765
   * E.S. Chibrikov.  A right normed basis for free Lie algebras and Lyndon–Shirshov words
     -   https://core.ac.uk/download/pdf/82357333.pdf 

**Further reading.**
   * N. Gadish. Letter-braiding: a universal bridge between combinatorial group theory and topology
     -   https://arxiv.org/abs/2308.13635
 
