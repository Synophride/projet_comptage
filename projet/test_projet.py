# coding=utf8
from projet import * 

class Node: 
    def __init__(self, a, b):
        self.sag = a 
        self.sad = b

Leaf = Node(None, None)        

## Todo : ajouter la bonne définition d'arbre binaire, 
# comme vu au dernier tp 

treeGram = {"Tree" : UnionRule("Node", "Leaf"),
            "Node" : ProductRule("Tree", "Tree", lambda a, b : Node(a, b)),
            "Leaf" : SingletonRule(Leaf)}

fiboGram = { "Fib" : UnionRule("Vide", "Cas1"), 
             "Cas1": UnionRule("CasAu", "Cas2"),
             "Cas2": UnionRule("AtomB", "CasBAu"),
             "Vide": EpsilonRule(""),
             "CasAu": ProductRule("AtomA", "Fib", "".join),
             "AtomA": SingletonRule("A"),
             "AtomB": SingletonRule("B"),
             "CasBAu": ProductRule("AtomB", "CasAu", "".join)}


init_grammar(treeGram) 
init_grammar(fiboGram)

for r in fiboGram.keys():
    print(r, "\t", fiboGram[r].valuation())
    
assert(treeGram["Tree"].valuation() == 1)
assert(treeGram["Tree"].valuation() == 1)
    

assert(treeGram["Tree"].count(1) == 1)
assert(treeGram["Tree"].count(4) == 5)
assert(fiboGram["Fib"].count(3) == 5)
print(fiboGram["Fib"].count(7))
assert(fiboGram["Fib"].count(6) == 21)



