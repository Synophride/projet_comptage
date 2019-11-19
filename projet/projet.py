# coding=utf8
import random
max_int = 2**100 

"""
Exception indiquant que les fonctions n'ont pas été données  en paramètre
aux règles de type UnionRule ou ProdRule, ce qui ne permet pas de calculer 
le rang d'un objet parmi une grammaire donnée. 
"""
class Lack_of_fun(Exception):
    def __init__(self, s):
        self._msg = s 
    def __str__(self):
        return "Lack_of_fun exception : " + self._msg

## Todo : enlever cette exception
class WTFexception(Exception):
    def __init__(self, s):
        self._s = s

# TODO Remplacer ça par une ValueError ? 
class InvalidGrammar(Exception):
    def __init__(self, s):
        self._s = s


# Représente une règle grammaticale abstraite
class AbstractRule:
    """ Représente une règle de la grammaire simple """

    def __init__(self):
        self._grammar = None
        raise NotImplementedError


    def set_grammar(self, g):
        """ Initialise la grammaire, ce qui permet d'avoir accès aux autres règles 
        à partir d'une règle donnée
        """
        self._grammar = g

        
    def count(self, n):
        """ Donne le nombre d'objets de taille n dérivés de la règle de grammaire 
        
        Paramètres :
        ------------
        n : int  La taille des objets
        """
        raise NotImplementedError

    def list(self, n):
        """
        Donne la liste des objets de taille n dérivés de la règle
        
        Paramètres :
        ------------
        n : int  La taille des objets
        """
        raise NotImplementedError

    def unrank(self, n, rank):
        """
        Donne l'objet de rang 'rank' parmi l'ensemble des objets 
        de taille n dérivant de la règle
        
        Paramètres:
        -----------
        n : int  Taille des objets
        rank : int  Rang de l'objet recherché

        Exceptions : 
        -----------
        ValueError si le rang ne correspond à aucun objet
        """
        raise NotImplementedError
    
    def valuation(self):
        """
        Donne la taille du plus petit objet dérivant de la règle courante
        
        """
        raise NotImplementedError
    
    def random(self, n):
        """
        Rend un objet de taille n au hasard
        """
        raise NotImplementedError
    
    def rank(self, n, obj):
        """
        Rend le rang de l'objet obj, qui est de taille n 

        Paramètres:
        -----------
        obj : ?  L'objet auquel on cherche à associer un rang
        n : int  La taille de l'objet
        """
        raise NotImplementedError

    
class ConstructorRule(AbstractRule):
    """
    Va représenter une règle non terminale
    """
    
    def __init__(self):
        self._parameters = None # Je sais pas à quoi sert ce truc
        self._fst = None 
        self._snd = None 
        self._valuation = None
        self._cache = None # Le cache = un dictionnaire 
        raise NotImplementedError 

    # Pas de différence entre UnionRule et ProdRule,
    # donc autant l'implémenter ici 
    def valuation(self):
        return self._valuation 

    # Le cache est un simple dictionnaire python.
    # Cette méthode est commune aux deux
    # sous-classes. 
    def count(self, n):
        if n in self._cache:
            return self._cache[n]
        else:
            val = self._count(n) 
            self._cache[n] = val 
            return val

    
    def _count(self, n):
        """ Fonction calculant le résultat de count(self,n) 
        si ce dernier n'a pas été trouvé dans le cache """ 
        raise NotImplementedError

    def _update_valuation(self):
        raise NotImplementedError

    def random(self, n):
        return self.unrank(n, random.randint(self.count(n)))
    
class UnionRule(ConstructorRule):
    """
    Représente une règle grammaticale de la forme G = A | B 
    """
    
    def __init__(self, fst, snd, cmp = None):
        """
        Constructeur 

        Paramètres:
        -----------
        fst : str  
          Le nom de la première sous-règle 
        snd : str 
          Le nom de la seconde  sous-règle
        cmp : obj -> obj -> bool  
          Fonction permettant de comparer deux objets générés

        """
        self._valuation = max_int
        self._fst = fst
        self._snd = snd
        self._parameters = (fst, snd)
        self._cache = dict() # Cache
        if cmp is not None:
            self._cmp = cmp
  

    def _update_valuation(self):
        """
        Met à jour la valuation de la règle en fonction des valuations 
        des sous-règles
        
        Retour: booléen
        -------
        True  si la valeur a été mise à jour depuis le dernier appel
        False si la valeur est restée la même depuis le dernier appel
        
        """
        v1 = self._grammar[self._fst].valuation()
        v2 = self._grammar[self._snd].valuation()
        oldv = self._valuation
        self._valuation = min(v1, v2)
        assert(oldv >= self._valuation)
        return (oldv > self._valuation)
    
    def _count(self,n): 
        c1 = self._grammar[self._fst].count(n)
        c2 = self._grammar[self._snd].count(n)
        return c1 + c2


    def unrank(self, n, rank):
        if(rank >= self.count(n)):
            raise ValueError("count = " + str(self.count(n)) +"\t rank = " + str(rank))  
        else: 
            r1 = self._grammar[self._fst]
            c1 = r1.count(n)
            
            r2 = self._grammar[self._snd] 
            c2 = r2.count(n)
            
            if(rank < c1):
                return r1.unrank(n, rank)
            else: 
                return r2.unrank(n, rank - c1)

    def rank(self, n, obj):
        if self._cmp is None:
            raise Lack_of_fun("Union : La fonction de comparaison entre deux objets n'est pas définie") 
        else: 
            if(self._grammar[self._snd].count(n) == 0): 
                return self._grammar[self._fst].rank(n, obj) 
            premier_elt_snd = self._fst.unrank(n, 0)
            if self._cmp(premier_elt_snd, obj) < 0: # obj > premier_elt_snd => Dans le second ensemble => 
                return self._grammar[self._fst].count(n) + self._grammar[self._snd].rank(n, obj)
            else :
                return self._grammar[self._fst].rank(n, obj)
            
    ## Problème : S'il existe un cycle qui revient vers la règle courante, ça peut
    ## boucler indéfiniment
    def list(self, n):
        r1 = self._grammar[self._fst].list(n)
        r2 = self._grammar[self._snd].list(n)
        return r1 + r2 
        
    def __str__(self):
        return "(" + self._fst + " | " + self._snd + " )" 
    

## Dest : Détruit un objet en deux sous objets 
## Size : calcule la taille d'un objet
class ProductRule(ConstructorRule):
    
    def __init__(self, fst, snd, cons, dest=None, size=None):
        """
        Initialisation de la classe produit 
        
        Paramètres:
        -----------
        fst : obj 
        snd : obj 
          Les sous-règles permettant de dériver des objets

        cons : obj -> obj -> obj : Fonction permettant de "lier" deux 
          sous-objets pour en créer un troisième
        
        dest : "destructeur", séparant un objet en deux sous-objets engendrés 
          par chacune des sous-rugles
        size : fonction permettant de calculer la taille d'un objet 
        """
        self._fst = fst
        self._snd = snd
        self._cons= cons
        self._valuation = max_int
        self._cache = dict() 
        self._dest = dest
        self._size = size

    def _update_valuation(self):
        v1 = self._grammar[self._fst].valuation()
        v2 = self._grammar[self._snd].valuation()
        oldv = self._valuation
        self._valuation = min(max_int, v1 + v2) # Sinon, si les deux SR sont à max_int, ça peut faire foirer le assert
        assert(oldv >= self._valuation) 
        return(oldv > self._valuation)

    def _count(self, n):
        r1 = self._grammar[self._fst]
        r2 = self._grammar[self._snd]
        v1 = r1.valuation()
        v2 = r2.valuation()
        s = 0
        for i in range(n+1):
            j = n - i 
            if(i < v1 or j < v2):
                continue
            s += r1.count(i) * r2.count(j)
        return s
    
    def unrank(self, n, rank):
        nb_objets = self.count(n) 
        
        if(rank >= nb_objets):
            raise ValueError("count = " + nb_objets + "\trang = " + rank)
        
        # Grammaires / sous-règles 
        r1 = self._grammar[self._fst]
        r2 = self._grammar[self._snd] 
        
        n_fst = 0 # Dimension du premier objets 
        n_snd = 0 # Dimension du second objet 
        
        somme = 0 # compteur permettant de compter le nombre d'objets déjà vus 
        diff  = 0 # Rang de l'objet cherché si le premier objet est de taille
                  #   n_fst et le second de taille n_snd
        count = 0 # Nombre de séquances d'objets pour une taille donnée 
        
        c1 = 0
        c2 = 0 
        
        for i in range(n+1): # on veut avoir les cas i = 0 et i = n, 
        # dans les cas où il y a des objets de taille 0 dans les sous grammaires  
            j = n - i
            c1 = r1.count(i) # Nombre d'objets de la première règle de taille i 
            c2 = r2.count(j) # Nombre d'objets de la secconde règle de taille n - i 
            
            count = c1 * c2 # Nombre d'objets de taille n dans la règle courante, 
                # où les objets dérivant de la première sous règle sont de taille i
                # et où ... seconde sous règle ... taille j 
            
            if(somme + count > rank): # dans ce cas, on a trouvé le bon i 
                n_fst = i # Le premier sous-élément sera de taille i 
                n_snd = j
                assert(c1 > 0)
                assert(c2 > 0)
                diff = rank - somme # rang de l'objet dans le sous ensemble 
                broke = True
                break
            else:
                somme += count 
    
        # |---- count --->| 
        # [ 1 | 2 | 3 | 4 ]
        # |---> . diff
        # |<->  c2
        rank_fst = diff // c2
        rank_snd = diff %  c2
        
        assert(rank_fst < c1), (rank_fst, c1) # cet assert ne passe pas, rank_fst = c1 = 1 
        assert(rank_snd < c2), (rank_snd, c2) 
        
        fst_obj = r1.unrank(n_fst, rank_fst)
        snd_obj = r2.unrank(n_snd, rank_snd)
        
        return self._cons(fst_obj, snd_obj)
    
    def list(self, n):
        r1 = self._grammar[self._fst]
        r2 = self._grammar[self._snd]
        
        v1 = r1.valuation()
        v2 = r2.valuation() 
        ret = []
        
        for i in range(n+1):
            j = n - i 
            if(i < v1 or j < v2):
                continue
            
            l1 = r1.list(i)
            l2 = r2.list(j)
            for e1 in l1:
                for e2 in l2:
                    ret.append(self._cons(e1, e2))
        return ret

    def rank(self, n, obj): 
        if self._dest is None:
            raise Lack_of_fun("Pas de destructeur donc pas de rank") 
        elif self._size is None:
            raise Lack_of_fun("Pas de calculateur de taille de l'objet")
        r1 = self._grammar[self._fst]
        r2 = self._grammar[self._snd] 
        
        
        (obj1, obj2) = self._dest(obj)
        size1 = self._size(obj1)
        size2 = self._size(obj2)
        
        rang1 = r1.rank(size1, obj1)
        rang2 = r2.rank(size2, obj2) 
        
        count1 = r1.count(size1)
        count2 = r2.count(size2) 
        
        final_rank = count2 * rang1 + rang2 
        
        return final_rank 

    def __str__(self):
        return "( " + self._fst + " x " + self._snd + " )" 

class ConstantRule(AbstractRule):
    def __init__(self):
        self._object = None
        raise NotImplementedError
    def valuation (self):
        return self._calc_valuation()

    def _update_valuation(self):
        return False # Pas de mise à jour nécessaire vu que valuation constante
    
    def _calc_valuation(self):
        raise NotImplementedError 
     
class SingletonRule(ConstantRule):
    def __init__(self, obj):
        self._object = obj

    
    def _calc_valuation(self):
        return 1
    
    def count(self, n):
        if n == 1:
            return 1
        else:
            return 0 
   
    def unrank(self, n, rank): 
        if( rank >= self.count(n)):
            raise ValueError("rank = " + str(rank) + "\t count = " + str(self.count(n)))
        else:
            return self._object
            
    def list(self, n):
        if n == 1: 
            return [self._object]
        else:
            return []
        
    def __str__(self):
        return str(self._object)
    
    def rank(self, n, obj):
        if obj == self._obj and n == 1:
            return 0
        else:
            raise ValueError 
        
    def random(self, n, rank):
        if n == 1 and rank == 0:
            return self._object
        else:
            raise ValueError

class EpsilonRule(ConstantRule):
    def __init__(self, obj):
        self._object = obj # objet représentant un objet vide 

    def _calc_valuation(self):
        return 0
    
    def count(self, n): 
        if n == 0:
            return 1
        else:
            return 0
    
    def random(self, n, rank):
        if n == 0 and rank == 0:
            return self._object
        else:
            raise ValueError
            
    def unrank(self, n, rank): 
        if( rank >= self.count(n)):
            raise ValueError("rank = " + str(rank) + "\t count = " + str(self.count(n)))
        else:
            return self._object
    
    def rank(self, n, obj):
        if n == 0 and obj == self._obj : 
            return 0
        else :
            raise ValueError

    def list(self, n):
        if n == 0:
            return [self._object]
        else:
            return []

    def __str__(self):
        return "eps" 

class Bad_grammar(Exception):
    pass


"""
Dit si une grammaire donnée est correcte, id est 
 vérifie que chaque règle référencée existe bien dans la grammaire 
 Rend True si la grammaire est correctement formée dans cette mesure 
 False sinon 
"""
def is_correct(g): 
    """
    Détermine si les règles de la grammaire initialisée sont cohérentes, id est si
    a) les règles qui apparaissent dans les règles existent
    b) la valuation des terminaux n'est pas égale à max_int
    """
    k = g.keys() 
    def f(r):
        
        if (isinstance(r, CondensedRule) and ((r._fst not in k) or (r._snd not in k))) or r.valuation() == max_int :
            raise Bad_grammar
        else: # rien à faire dans le cas de terminaux 
            pass 
    try:
        for r in k:
            f(r)
        return true 
    except Bad_grammar:
        return false

def init_grammar(g):
    """ 
    Initialise une grammaire g

    Si la grammaire n'est pas correctement formée, 
    lance l'exception Bad_grammar
    """ 
    keys = list(g.keys())
    # I. Initialisation de la grammaire
    for key in keys:
        rule = g[key]
        rule.set_grammar(g)

    b = True
    while(b):
        b = False
        for key in keys:
            rule = g[key]
            b = b or rule._update_valuation()

    if(not is_correct(g)):
        raise Bad_grammar


#############################
### Grammaires condensées ###
#############################


UNION = 0
PROD = 1 
SINGLETON = 2  
EPSILON = 3
NONTERM = 4
SEQUENCE = 5 

class CondensedRule():
    """
    Représente une règle "condensée", qui sera simplifiée dans la suite 
    """
    pass

# TODO : définir fonctions additionnelles en param
class Union(CondensedRule):
    def __init__(self, r1, r2):
        self._r1 = r1
        self._r2 = r2
        self.type = UNION

        
class Prod(CondensedRule): # Il faudrait peut-être définir les fonctions additionnelles en param
    def __init__(self, r1, r2, cons):
        self._r1 = r1
        self._r2 = r2
        self._cons = cons 
        self.type = PROD 
        
class Singleton(CondensedRule): 
    def __init__(self, obj):
        self._obj = obj 
        self.type = SINGLETON

class Epsilon(CondensedRule):
    def __init__(self, obj):
        self._obj = obj
        self.type = EPSILON

class NonTerm(CondensedRule):
    def __init__(self, nom_regle):
        self.type = NONTERM
        self._nom = nom_regle

class Sequence(CondensedRule):
    def __init__(self, nonterm, casvide, cons):
        self.nonterm = nonterm
        self.casvide = casvide
        self.cons = cons 
        self.type = SEQUENCE 

class Cpt():
    """ Classe permettant de générer de nouveaux noms de règles pour une grammaire donnée.
    Les règles auront un nom de la forme "rule<n>", avec n:int 
    """
    def __init__(self):
        self.i = 0
    def get(self):
        i = self.i 
        self.i += 1
        return ("rule" + str(i)) 

def simplif_rule(rule:CondensedRule, cpt:Cpt, d, keys_base):
    """
    Convertit récursivement une règle 'rule' en un ensemble de règles qui sont ajoutées
    au dictionnaire d (qui représente une grammaire simplifiée)


    Paramètres: 
    -----------
    rule : CondensedRule  La règle à convertir
    cpt : Cpt  Compteur permettant de génerer des noms de règles
    d : dict(str -> AbstractRule)  Dictionnaire représentant la nouvelle grammaire
    keys_base : str set  Ensemble contenant l'ensemble des règles de la grammaire 
      condensée donnée en entrée. Utile pour éviter l'utilisation d'un nom de règle déjà existant

    Retour : 
    --------
    Une chaîne de caractères représentant la règle rule dans la nouvelle grammaire
    """
    
    t = rule.type # Type de la règle (peut-être qu'utiliser isinstance() est plus approprié)
    
    if t == NONTERM:
        return rule._nom

    # Génération d'un nouveau nom pour la règle courante. On génère "naïvement" des nouveaux
    # noms de règles jusqu'à ce que le nom de variable ne soie plus choisi. 
    new_rule_name = cpt.get()
    while(new_rule_name in d.keys() or new_rule_name in keys_base):
        new_rule_name = cpt.get()
    
    if t == PROD:
        # Ajout des sous-règles au dictionnaire, puis du produit associé
        nom_sr1 = simplif_rule(rule._r1, cpt, d, keys_base) 
        nom_sr2 = simplif_rule(rule._r2, cpt, d, keys_base) 
        d[new_rule_name] = ProductRule(nom_sr1, nom_sr2, rule._cons)
        
    elif t == UNION:
        nom_sr1 = simplif_rule(rule._r1, cpt, d, keys_base)
        nom_sr2 = simplif_rule(rule._r2, cpt, d, keys_base)
        d[new_rule_name] = UnionRule(nom_sr1, nom_sr2)

    elif t == SINGLETON:
        d[new_rule_name] = SingletonRule(rule._obj)

    elif t == EPSILON: 
        d[new_rule_name] = EpsilonRule(rule._obj)

    elif t == SEQUENCE:
        # Sequence = union (sr1, sr2) 
        sr1 = Epsilon(rule.casvide)
        sr2 = Prod(new_rule_name, rule.nonterm , rule.cons)
        
        d[new_rule_name] = UnionRule(simplif_rule(sr1, cpt, d, keys_base), simplif_rule(sr2, cpt, d, keys_base))
    else:
        raise NotImplementedError
    ## Donner à l'appelant quel nom de règle citer 
    return new_rule_name



def simplify_grammar(cond_g):
    """
    Simplifie la grammaire complexe en paramètre en une grammaire simple 
    """
    new_gram = dict() # Dictionnaire retour : str -> AbstractRule
    cpt = Cpt() # Génération de noms de règles
    base_keys = set(cond_g.keys()) 
    
    # Simplification des règles 
    for rule_name in base_keys:
        # Principe (assez sale par ailleurs) : Lancer l'appel récursif sur chaque règle.
        # Ensuite, renommer la règle qui vient d'être créée dans le dictionnaire
        # (qui représente une règle «compliquée») en le nom de la règle de base.
        

        # Création des entrées liées à chaque règle. La règle que l'on cherche à obtenir
        # possède un mauvais nom, on va donc le renommer 
        name = simplif_rule(cond_g[rule_name], cpt, new_gram, base_keys)

        # Renommage de l'entrée name en rule_name 
        rule = new_gram[name] 
        del(new_gram[name])
        new_gram[rule_name] = rule        
    return new_gram
 
