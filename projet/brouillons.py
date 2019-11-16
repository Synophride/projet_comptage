
        nb_objets = self.count(n) 
        r1 = self._grammar[self._fst]
        r2 = self._grammar[self._snd]
        if rank >= nb_objets:
            raise ValueError
        else:
            s = 0
            n_fst = 0
            n_snd = 0 
            diff = 0  
            nb_objects = 0
            for i in range(n+1):
                j = n - i 
                nb_objects = r1.count(i) * r2.count(j)
                    if(s + nb_objects > rank):
                        n_fst = i
                        n_snd = j 
                        diff = n - s
                        break
                    else:
                        s += nb_objects
            fst_rank = diff // nb_objects 
            snd_rank = diff % nb_objects 
            