# coding=utf8
import random
max_int = 2**100 


class Lack_of_fun(Exception):
    def __init__(self, s):
        self._msg = s 
    def __str__(self):
        return "Lack_of_fun exception : " + self._msg

class WTFexception(Exception):
    def __init__(self, s):
        self._s = s

class InvalidGrammar(Exception):
    def __init__(self, s):
        self._s = s

class AbstractRule:

    def __init__(self):
        self._grammar = dict()

    def set_grammar(self, g):
        self._grammar = g

    def count(self, n):
        raise NotImplementedError

    def list(self, n):
        raise NotImplementedError

    def unrank(self, n, rank):
        raise NotImplementedError
    
    def valuation(self):
        raise NotImplementedError
    
    def random(self, n):
        raise NotImplementedError
    
    def rank(self, n, obj):
        raise NotImplementedError

    
class ConstructorRule(AbstractRule):
    def __init__(self):
        self._parameters = None
        self._fst = None
        self._snd = None 
        self._valuation = None
        self._cache = dict() 

    def valuation(self):
        return self._valuation 
    
    def count(self, n):
        if n in self._cache:
            return self._cache[n]
        else:
            val = self._count(n) 
            self._cache[n] = val 
            return val

    def _count(self, n):
        raise NotImplementedError
    
    def _update_valuation(self):
        raise NotImplementedError

    def random(self, n):
        return self.unrank(n, random.randint(self.count(n)))
    
class UnionRule(ConstructorRule):

    """
        cmp(a, b) < 0 si a < b 
    """
    def __init__(self, fst, snd, cmp = None):
        self._valuation = max_int
        self._fst = fst
        self._snd = snd
        self._parameters = (fst, snd)
        self._cache = dict()
        self._cmp = cmp
  
    
    """ Rend True si la valeur a été mise à jour
        False sinon
    """
    def _update_valuation(self):
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
        self._fst = fst
        self._snd = snd
        self._cons= cons
        self._valuation = max_int
        self._cache = dict() 
        self._dest = None
        self._size = None

    def _update_valuation(self):
        v1 = self._grammar[self._fst].valuation()
        v2 = self._grammar[self._snd].valuation()
        oldv = self._valuation
        self._valuation = min(max_int, v1 + v2)
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
            assert(j + i == n)
            if(i < v1 or j < v2):
                continue
            s += r1.count(i) * r2.count(j)
        return s
    
    def unrank(self, n, rank):
        nb_objets = self.count(n) 
        
        if(rank >= nb_objets):
            raise ValueError("count = " + nb_objets + "\trang = " + rank)
        
        # Grammaires 
        r1 = self._grammar[self._fst]
        r2 = self._grammar[self._snd] 
        
        n_fst = 0 # Dimension du premier objets 
        n_snd = 0 # Dimension du second objet 
        
        somme = 0 # compteur permettant de compter le nombre d'objets déjà vus 
        diff  = 0 # Rang de l'objet cherché si le premier objet est de taille
                  # n_fst et le second de taille n_snd
        count = 0 # Nombre de séquances d'objets pour une taille donnée 
        
        c1 = 0
        c2 = 0 
        
        broke = False
        
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
        
    def valuation (self):
        return self._calc_valuation()

    def _update_valuation(self):
        return False
    
    def _calc_valuation(self):
        pass
    
 
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
        else raise ValueError 
        
    def random(self, n, rank):
        if n == 1 and rank == 0:
            return self._object
        else:
            raise ValueError

class EpsilonRule(ConstantRule):
    def __init__(self, obj):
        self._object = obj

    def _calc_valuation(self):
        return 0
    def count(self, n): 
        if n == 0:
            return 1
        else :
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

            
    # a voir
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
    k = g.keys() 
    def f(r):
        if isinstance(r, CondensedRule) and ((r._fst not in k) or (r._snd not in k)):
            raise Bad_grammar
        else: # rien à faire dans ce cas 
            pass 
    try:
        for r in k:
            f(r) 
        return true 
    except Bad_grammar:
        return false

""" Initialise une grammaire 
    Vérifier qu'aucun des count ne reste à l'infini ? 
"""
def init_grammar(g):
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
            # TODO : vérifier qu'aucune règle n'est à max_int 


#############################
### Grammaires condensées ###
#############################
UNION = 0
PROD = 1 
SINGLETON = 2  
EPSILON = 3
NONTERM = 4

class CondensedRule():
    pass
   
class Union(CondensedRule):
    def __init__(self, r1, r2):
        self._r1 = r1
        self._r2 = r2
        self.type = UNION

class Prod(CondensedRule):
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

class Cpt():
    def __init__(self):
        self.i = 0
    def get(self):
        i = self.i 
        self.i += 1
        return ("rule" + str(i)) 

    
### Ajoute un équivalent de la règle de grammaire "compliquée" 
### donnée en paramètre pour ajouter une ou plusieurs règles équivalentes
### dans le dictionnaire d donné en paramètre
### paramètres  : 
### rule : CondensedRule - La règle à "traduire" 
### - une fonction de création de noms de règles
### d : dict(str -> AbstractRule) - Le dictionnaire où l'on traduit 
### keys_base : set(str) - La liste des règles dans la CondensedRule, pour 
###     ne pas créer de règles avec des noms déjà existants
def simplif_rule(rule, cpt, d, keys_base):
    t = rule.type
    
    if t == NONTERM:
        return rule._nom
    
    new_rule_name = cpt.get()
    while(new_rule_name in d.keys() or new_rule_name in keys_base):
        new_rule_name = cpt.get()   
    
    if t == PROD:
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
    else:
        raise WTFexception
    return new_rule_name


# todo : fonction de substitution
### Simplifie les règles de la grammaire complexe donnée en paramètre 
def simplify_grammar(cond_g):
    new_gram = dict()
    cpt = Cpt()
    base_keys = set(cond_g.keys())
    
    # Simplification des règles 
    for rule_name in base_keys:
        name = simplif_rule(cond_g[rule_name], cpt, new_gram, base_keys)
        rule = new_gram[name] 
        del(new_gram[name])
        new_gram[rule_name] = rule
    return new_gram
 
