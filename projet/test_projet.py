# coding=utf8
from projet import * 

print("Création des grammaires") 
class Node: 
    def __init__(self, a, b):
        self.sag = a 
        self.sad = b
    def __str__(self):
        if self.sag == None:
            return "Leaf"
        else:
            return "Node( " + str(self.sag) + ", " + str(self.sad) + " )" 
    
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
             "CasAu": ProductRule("AtomA", "Fib", (lambda a, b : "".join([a,b])) ),
             "AtomA": SingletonRule("A"),
             "AtomB": SingletonRule("B"),
             "CasBAu": ProductRule("AtomB", "CasAu", (lambda a,b : "".join([a,b])) )}

print("initialisation des grammaires") 

init_grammar(treeGram) 
init_grammar(fiboGram)

failed_tests = [] 
print("Test de la valuation des grammaires")
assert(treeGram["Tree"].valuation() == 1)
assert(treeGram["Tree"].valuation() == 1)
    
print("Test des count")
assert(treeGram["Tree"].count(1) == 1)
assert(treeGram["Tree"].count(4) == 5)
assert(fiboGram["Fib"].count(3) == 5)
assert(fiboGram["Fib"].count(6) == 21)



print("Test d'égalité entre la longueur des listes et count") 
for i in range(0, 7):
    for rule_name in treeGram.keys():
        assert( len(treeGram[rule_name].list(i)) == treeGram[rule_name].count(i))
    for rule_name in fiboGram.keys():
        assert( len(fiboGram[rule_name].list(i)) == fiboGram[rule_name].count(i))

print("Test des listes") 
print("Liste pour n = 4")
for t in treeGram["Tree"].list(4):
    print(t) 


print("Comparaison de list et unrank") 
for n in range(10):
    print("n = " , n) 
    g = treeGram 
    rule_name = "Tree" 
    rule = g[rule_name]
    print("liste")
    l = rule.list(n)
    for e in l:
        print(str(e))
    print("fin liste") 
    for rank in range(rule.count(n)):
        print("rang ", rank) 
        print("element de la liste :" , str(l[rank]))
        print("element du unrank   :" , str(rule.unrank(n, rank)))
##############################
### Grammaires compliquées ###
##############################

cg1 = { "Tree" : Union(Singleton(Leaf), 
                 Prod( NonTerm("Tree"), NonTerm("Tree"), 
                 lambda a, b : "".join([a,b]))) } 

simplified_tree = simplify_grammar(cg1)

for rule in simplified_tree.keys():
    print(rule, " :\t" , simplified_tree[rule])
