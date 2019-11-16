# coding=utf8
max_int = 2**100 

class WTFexception(Exception):
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
    
    
class ConstructorRule(AbstractRule):
    def __init__(self):
        self._parameters = None
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


# parameters ?= (fst snd) 
class UnionRule(ConstructorRule):


    def __init__(self, fst, snd):
        self._valuation = max_int
        self._fst = fst
        self._snd = snd
        self._parameters = (fst, snd)
        self._cache = dict()
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


    ## Problème : Si une règle union s'auto référence, ça peut
    ## boucler indéfiniment (enfin peut-être, je suis pas vraiment sûr) 
    def list(self, n):
        r1 = self._grammar[self._fst].list(n)
        r2 = self._grammar[self._snd].list(n)
        return r1 + r2 
    
    
class ProductRule(ConstructorRule):
    def __init__(self, fst, snd, cons):
        self._fst = fst
        self._snd = snd
        self._cons= cons
        self._valuation = max_int
        self._cache = dict() 
        

    def _update_valuation(self):
        v1 = self._grammar[self._fst].valuation()
        v2 = self._grammar[self._snd].valuation()
        oldv = self._valuation
        self._valuation = v1 + v2
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
        
        r1 = self._grammar[self._fst]
        r2 = self._grammar[self._snd] 
        
        n_fst = 0
        n_snd = 0
        
        somme = 0
        diff  = 0
        count = 0
        
        c1 = 0
        c2 = 0 
        
        broke = False
        i = 0 
        for i in range(n+1):
            if(broke):
                raise WTFexception
            j = n - i
            c1 = r1.count(i)
            c2 = r2.count(j)
            count = c1 * c2 # nombre d'objets où les objets de r1 ont une taille i, et les objets de r2 ont une taille j 
            
            if(somme + count > rank):
                n_fst = i
                n_snd = j
                assert(c1 > 0)
                assert(c2 > 0)
                print("c", c1, "\t", c2) 
                diff = rank - somme
                broke = True
                break
            
            else:
                somme += count 
                assert(somme <= rank)         
        assert(broke)
        print(rank, "\tz\t", somme, "\t", count) 
        print("op = ", diff, "/", c1)  
        rank_fst = diff // c1 
        rank_snd = diff % c1
        
        assert(rank_fst < c1), (rank_fst, c1)
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
    
    def unrank(self, n, rank): 
        if( rank >= self.count(n)):
            raise ValueError("rank = " + str(rank) + "\t count = " + str(self.count(n)))
        else:
            return self._object
    
    # a voir
    def list(self, n):
        if n == 0:
            return [self._object]
        else:
            return []
        

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

def simplif_rule(rule, mk_var, d, keys_base):
    t = rule.type
    
    # switch du pauvre 
    if t == UNION:

        nom_sous_regle_1 = mk_var() 
        while(nom_sous_regle_1 in d.keys() or nom_sous_regle_1 in keys_base):
            nom_sous_regle_1 = mk_var() 
        
        nom_sous_regle_2 = mk_var() 
        while(nom_sous_regle_2 in d.keys() or nom_sous_regle_2 in keys_base):
            nom_sous_regle_2 = mk_var() 
        
        d[nom_sous_regle_1] = simplif_rule(rule._r1, mk_var, d)
        d[nom_sous_regle_2] = simplif_rule(rule._r2, mk_var, d) 
        return UnionRule(nom_sous_regle_1, nom_sous_regle_2)
   
    elif t == PROD:
          nom_sous_regle_1 = mk_var() 
        while(nom_sous_regle_1 in d.keys() or nom_sous_regle_1 in keys_base):
            nom_sous_regle_1 = mk_var() 
        
        nom_sous_regle_2 = mk_var() 
        while(nom_sous_regle_2 in d.keys() or nom_sous_regle_1 in keys_base):
            nom_sous_regle_2 = mk_var() 
        
        d[nom_sous_regle_1] = simplif_rule(rule._r1, mk_var, d)
        d[nom_sous_regle_2] = simplif_rule(rule._r2, mk_var, d) 
        return UnionRule(nom_sous_regle_1, nom_sous_regle_2, rule._cons)
    elif t == SINGLETON:
        return SingletonRule(rule._obj)
    elif t == EPSILON:
        return EpsilonRule(rule._obj) 

#TODO : Vérifier le non-écrasage de nouvelles règles 
def simplify_grammar(cond_g):
    new_gram = dict()
    cpt_regle = 0
    
    def mk_str_rule():
        x = cpt_regle
        cpt_regle += 1
        return str(x) 
    
    base_keys = set(cond_g.keys())
    
    for rule_name in base_keys:
        new_gram[rule_name] = simplif_rule(cond_g[rule_name], mk_str_rule, new_gram, base_keys)
    
    return new_gram