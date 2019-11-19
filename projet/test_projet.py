# coding=utf8
from projet import * 
N = 1000
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
    def __eq__(self, other):
        return str(self) == str(other)
    def size(self):
        if sag is None: 
            return 1 
        else:
            return sag.size() + sad.size() 


Leaf = Node(None, None)        

## Les deux arbres sont de même taille
def compare_trees(t1, t2): 
    if t1.sad == None: # Si c'est une feuille, l'autre est une feuille 
        return 0
    size_sag1 = t1.sag.size()
    size_sag2 = t2.sag.size() 
    if(size_sag1 - size_sag2 != 0):
        return size_sag1 - size_sag2 
    comp_sag = compare_trees(t1.sag, t2.sag)
    if(comp_sag != 0):
        return comp_sag 
    else:
        return compare_trees(t1.sad, t2.sad) 
    
treeGram = {"Tree" : UnionRule("Node", "Leaf", cmp = compare_trees) , # A
            "Node" : ProductRule("Tree", "Tree", lambda a, b : Node(a, b), dest = lambda t : (t.sag, t.sad), size = lambda t : t.size() ),
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

def write_fibogram():
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
def write_treeGram():
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


        
print("Test d'égalité entre la longueur des listes et count") 
i = 0
for i in range(10):
    for rule_name in treeGram.keys():
        assert( len(treeGram[rule_name].list(i)) == treeGram[rule_name].count(i))
    i += 1 
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
#####  "Tests complets"  #####
##############################


print("Tests complets")

grams = [(treeGram,"Tree"),(fiboGram, "Fib")]
for g, rn in grams : 
    print(rn) 
    n = 0
    r = g[rn] 
    while(r.count(n) < N): 
        print(n)
        l = r.list(n)
        for i in range(len(l)):
            ur = r.unrank(n, i)
            assert(ur == l[i])
        assert(len(l) == r.count(n))
        n += 1

##############################
### Grammaires compliquées ###
##############################
print("Tests de simplification de grammaires compliquées") 
raise Exception("La suite du programme a une boucle infinie, donc je l'arrête là")
cg1 = { "Tree" : Union(Singleton(Leaf),
                 Prod( NonTerm("Tree"), NonTerm("Tree"), 
                 lambda a, b : Node(a,b)))} 


simplified_treeGram = simplify_grammar(cg1)
print("##Grammaire simplifiée##")
for k in simplified_treeGram.keys():
    r = simplified_treeGram[k]
    print(k, '\t', str(r))


init_grammar(simplified_treeGram)

r = treeGram["Tree"]
rsimp = simplified_treeGram["Tree"] 

for n in range(6):
    print(n) 
    print("Count")
    assert(r.count(n) == rsimp.count(n))
    print("Génération des listes")
    lsimp = rsimp.list(i)
    l = r.list(i)
    assert (len(l) == len(lsimp))
    print("Test sur les listes") 
    for i in range(len(l)):
        assert(l[i] == lsimp[i]) 
        assert(l[i] == rsimp.unrank(n, i))
        