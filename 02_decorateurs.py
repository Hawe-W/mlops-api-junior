#Méthode et décorateur

from functools import wraps

def cache(func):
    cache_dict = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # On ignore 'self' (args[0]) et on hash seulement les données
        donnees = tuple(args[1]) if len(args) > 1 else ()
        key = donnees
        
        if key in cache_dict:
            print("→ Cache hit!")
            return cache_dict[key]
        result = func(*args, **kwargs)
        cache_dict[key] = result
        return result
    return wrapper


class ModeleML:
    def __init__(self, nom):
        self.nom = nom
    
    @cache
    def predire(self, donnees):
        print("-> Calcul de prédiction...")
        return f"Prediction {self.nom}: {sum(donnees)}"
    

modele = ModeleML("Churn")
print(modele.predire([1, 2, 3])) #Calcul
print(modele.predire([1, 2, 3])) #Cache