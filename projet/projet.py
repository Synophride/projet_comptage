# coding=utf8
max_int = 2**100 

class AbstractRule:
    def __init__(self):
        self._grammar = dict()

    def set_grammar(self, g):
        self._grammar = g
    def count(self, n):
        pass
    def list(self, n):
        pass
    
    def valuation(self):
        return None

    
class ConstructorRule(AbstractRule):
    def __init__(self):
        self._parameters = None
        self._valuation = None

    def valuation(self):
        return self._valuation 
    
    def _update_valuation(self):
        pass


# parameters ?= (fst snd) 
class UnionRule(ConstructorRule):


    def __init__(self, fst, snd):
        self._valuation = max_int
        self._fst = fst
        self._snd = snd
        
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
    
    def count(self,n): 
        c1 = self._grammar[self._fst].count(n)
        c2 = self._grammar[self._snd].count(n)
        return c1 + c2
    
    ## Problème : Si une règle union s'auto référence, ça peut
    ## boucler indéfiniment 
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

    def _update_valuation(self):
        v1 = self._grammar[self._fst].valuation()
        v2 = self._grammar[self._snd].valuation()
        oldv = self._valuation
        self._valuation = v1 + v2
        assert(oldv >= self._valuation)
        return(oldv > self._valuation)

    def count(self, n):
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
    
    def list(self, n):
        r1 = self._grammar[self._fst]
        r2 = self._grammar[self._snd]
        
        v1 = r1.valuation()
        v2 = r2.valuation() 
        ret = []
        
        for i in range(n):
            j = n - i 
            if(i <= v1 or j <= v2):
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
    
    # a voir
    def list(self, n):
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
