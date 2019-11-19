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
"""
print("Ecriture des count de fiboGram") 
l = list(fiboGram.keys())
print((" & ".join(l)) + r" \\ " + '\n') 
s = ""
for i in range(11):
    s = s + str(i)
    for key in l:
        r = fiboGram[key]
        if not isinstance(r, ConstructorRule):
            continue 
        s = s + ' & ' + str(r.count(i)) 
    s = s + r' \\' + ' \n ' 
print(s) 

print("Test des count de Tree")
print("Ecriture des count de treeGram") 
l = list(treeGram.keys())
for i in l:
    if not isinstance(treeGram[i], ConstructorRule):
        l.remove(i) 

        
print(" n & " +(" & ".join(l)) + r" \\ \hline " + '\n') 
s = ""
for i in range(11):
    s = s + str(i)
    for key in l:
        r = treeGram[key]
        if not isinstance(r, ConstructorRule):
            continue 
        s = s + ' & ' + str(r.count(i)) 
    s = s + r' \\' + ' \n ' 
print(s) 
raise WTFexception
"""

        
print("Test d'égalité entre la longueur des listes et count") 
for i in range(10):
    for rule_name in treeGram.keys():
        assert( len(treeGram[rule_name].list(i)) == treeGram[rule_name].count(i))
    for rule_name in fiboGram.keys():
        assert( len(fiboGram[rule_name].list(i)) == fiboGram[rule_name].count(i))

print("Test des listes") 
for n in range(6):
    print("  pour n = ", n) 
    for t in treeGram["Tree"].list(n):
        print('\t', str(t)) 


print("Comparaison des list et unrank") 
for n in range(10):
    tab =  [treeGram, fiboGram]
    for g in tab:
        nom_regles = g.keys()
        for rule_name in nom_regles:
            rule = g[rule_name]
            l = rule.list(n)
            for rank in range(rule.count(n)):
                assert(str(l[rank]) == str(rule.unrank(n, rank)))
        

##############################
### Grammaires compliquées ###
##############################

print("Tests de simplification de grammaires compliquées") 

cg1 = { "Tree" : Union(Singleton(Leaf), 
                 Prod( NonTerm("Tree"), NonTerm("Tree"), 
                 lambda a, b : "".join([a,b]))) } 

simplified_tree = simplify_grammar(cg1)

print("--- Simplification de la grammaire des arbres ---") 
for rule in simplified_tree.keys():    
    print('"', rule,'"', " :\t" , simplified_tree[rule])
