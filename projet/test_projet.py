# coding=utf8

from projet import * 

N = 100


class Node:
    """
    Classe représentant un arbre. 
    On part du principê que chaque noeud possède zéro ou deux sous-arbres.
    """
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
        if self.sag is None: 
            return 1 
        else:
            return self.sag.size() + self.sad.size() 

Leaf = Node(None, None)


def compare_trees(t1, t2):
    """ Fonction de comparaison entre deux arbres t1 et t2
    
    Paramètres:
    -----------
    t1, t2 : Node 
        Les deux arbres à comparer. Les arbres sont complets, c'est à dire
      qu'ils ont soit zéro fils, soit deux fils.
    
    Retour:
    -------
    Un nombre négatif quelconque si t1 < t2. 
    0 si t1 = t2
    Un nombre positif si t1 > t2 
    
    """
    if t1.sad == None: # Si c'est une feuille, l'autre sous-arbre est une feuille 
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


print("Déclaration des grammaires") 

treeGram = {"Tree" : UnionRule("Node", "Leaf", cmp = compare_trees) , 
            "Node" : ProductRule("Tree",
                                 "Tree",
                                 lambda a, b : Node(a, b),
                                 dest = lambda t : (t.sag, t.sad),
                                 size = lambda t : t.size() ),
            "Leaf" : SingletonRule(Leaf)}


fiboGram = { "Fib" : UnionRule("Vide", "Cas1"), 
             "Cas1": UnionRule("CasAu", "Cas2"),
             "Cas2": UnionRule("AtomB", "CasBAu"),
             "Vide": EpsilonRule(""),
             "CasAu": ProductRule("AtomA", "Fib", (lambda a, b : "".join([a,b])) ),
             "AtomA": SingletonRule("A"),
             "AtomB": SingletonRule("B"),
             "CasBAu": ProductRule("AtomB", "CasAu", (lambda a,b : "".join([a,b])) )}

print("Initialisation des grammaires") 

init_grammar(treeGram)
init_grammar(fiboGram)


print("Test de la valuation des grammaires")
assert(treeGram["Tree"].valuation() == 1)
assert(fiboGram["Fib"].valuation() == 0)


print("Test des count")
assert(treeGram["Tree"].count(1) == 1)
assert(treeGram["Tree"].count(4) == 5)
assert(fiboGram["Fib"].count(3) == 5)
assert(fiboGram["Fib"].count(6) == 21)

def write_fibogram():
    """ 
    Fonction écrivant le nombre de mots de taille 'n'
    dérivant de chaque non-terminal 
    de fiboGram, de sorte à pouvoir copier-coller le résultat 
    dans un tableau LaTeX
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


def write_treeGram():
    """ 
    Fonction écrivant le nombre de mots de taille 'n'
    dérivant de chaque non-terminal 
    de treeGram, de sorte à pouvoir copier-coller le résultat 
    dans un tableau LaTeX
    """
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
for i in range(11):
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
#####  Tests «complets»  #####
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

for n in range(12):
    l = treeGram["Tree"].list(n)
    for i in range(len(l)):       
        rk = treeGram["Tree"].rank(n, l[i]) # Pas énormément de tests sur la fonction rank() car fonctions assez contraignantes 
        assert(i == rk) 
##############################
### Grammaires compliquées ###
##############################

print("Tests de simplification de grammaires compliquées") 

cg1 = { "Tree" : Union(Singleton(Leaf),
                 Prod( NonTerm("Tree"), NonTerm("Tree"), 
                 lambda a, b : Node(a,b)))} 


simplified_treeGram = simplify_grammar(cg1)

print("Affichage de la grammaire simplifiée")

for k in simplified_treeGram.keys():
    r = simplified_treeGram[k]
    print(k, '\t', str(r))


init_grammar(simplified_treeGram)

r = treeGram["Tree"]
rsimp = simplified_treeGram["Tree"] 

raise Exception("La suite du programme a une boucle infinie, donc je l'arrête là pour l'instant")
for n in range(6):
    print(n) 
    print("Count")
    assert(r.count(n) == rsimp.count(n))
    print("Génération des listes")
    lsimp = rsimp.list(i) # <<< Cette ligne là boucle indéfiniment. 
    l = r.list(i)
    assert (len(l) == len(lsimp))
    print("Test sur les listes") 
    for i in range(len(l)):
        assert(l[i] == lsimp[i]) 
        assert(l[i] == rsimp.unrank(n, i))
        
