"""
Script MLOps pédagogique complet
- Fonctions Python
- Gestion des erreurs (try / except)
- Classes en POO + héritage
- Décorateurs (simples + cache)
- Context manager (logger)
- FastAPI (routes simples + API ML fake)
- Gestion erreurs FastAPI (HTTPException)
- Tests pytest (dans le même fichier pour l'exemple)
- Packaging Poetry (expliqué à la fin, pas dans ce fichier)
"""

# =========================
# 1. FONCTIONS PYTHON
# =========================

# Une fonction prend des paramètres et renvoie une valeur.
def somme(a, b):
    return a + b

resultat_somme = somme(2, 3)  # 5


# =========================
# 2. GESTION DES ERREURS (try / except)
# =========================

def to_int_safely(value):
    """
    Essaie de convertir value en int.
    Si ça échoue, retourne 0 au lieu de crasher.
    """
    try:
        return int(value)
    except ValueError:
        return 0

x1 = to_int_safely("42")     # 42
x2 = to_int_safely("abc")    # 0, car ValueError capturée


# =========================
# 3. DÉCORATEUR SIMPLE + CACHE
# =========================

from functools import wraps

def debug(func):
    """
    Décorateur simple : affiche le nom de la fonction appelée.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[DEBUG] Appel de {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def cache(func):
    """
    Décorateur de cache très simple pour des fonctions qui prennent une liste de nombres.
    Clé = tuple(données).
    """
    cache_dict = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # On suppose que la vraie donnée est dans args[1] (self est args[0] si méthode d'instance)
        donnees = tuple(args[1]) if len(args) > 1 else ()
        key = donnees

        if key in cache_dict:
            print("[CACHE] Hit!")
            return cache_dict[key]

        result = func(*args, **kwargs)
        cache_dict[key] = result
        return result

    return wrapper


# =========================
# 4. CLASSES EN POO + HÉRITAGE
# =========================

class ModeleML:
    """
    Classe de base pour un "modèle ML" très simple.
    """

    def __init__(self, nom):
        # Attributs d'instance
        self.nom = nom
        self.version = 1.0

    @debug          # Décorateur debug : log chaque appel
    @cache          # Décorateur cache : évite de recalculer pour les mêmes données
    def predire(self, donnees):
        """
        Simule une "prédiction" en retournant somme + longueur.
        En vrai, ici tu mettrais ton vrai modèle ML.
        """
        print("[CALCUL] Prédiction en cours...")
        return f"{self.nom}: somme={sum(donnees)}, len={len(donnees)}"


class PipelineML(ModeleML):
    """
    PipelineML hérite de ModeleML.
    On réutilise predire(), on ajoute des attributs & une méthode.
    """

    def __init__(self, nom):
        super().__init__(nom)  # Appelle __init__ du parent (ModeleML)
        self.etapes = 3

    def deployer(self):
        """
        Simule un déploiement de pipeline.
        """
        return f"Pipeline {self.nom} (v{self.version}) déployé avec {self.etapes} étapes"


# Petit test rapide des classes (POO)
modele = ModeleML("ChurnModel")
print(modele.predire([1, 2, 3]))
print(modele.predire([1, 2, 3]))  # 2e appel → devrait passer par le cache

pipeline = PipelineML("ChurnPipeline")
print(pipeline.predire([10, 20]))
print(pipeline.deployer())


# =========================
# 5. CONTEXT MANAGER (LOGGER)
# =========================

class LoggerML:
    """
    Context manager qui ouvre un fichier de log au début
    et le referme proprement à la fin.
    """

    def __enter__(self):
        self.file = open("mlops.log", "a", encoding="utf-8")
        self.file.write("\n=== Début session MLOps ===\n")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.write("=== Fin session MLOps ===\n")
        self.file.close()


# Utilisation du context manager
with LoggerML() as log:
    log.write("Modèle ChurnModel entraîné.\n")
    log.write("Pipeline ChurnPipeline déployé.\n")


# =========================
# 6. FASTAPI - API ML SIMPLE
# =========================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Création de l'application FastAPI
app = FastAPI(title="Mini API MLOps")

# Schéma de données d'entrée pour l'API
class InputPrediction(BaseModel):
    donnees: list[float]


# Instance globale de PipelineML utilisée par l'API
pipeline_global = PipelineML("ChurnAPI")


@app.get("/ping")
def ping():
    """
    Route FastAPI minimale de santé (healthcheck).
    """
    return {"message": "pong"}


@app.post("/predire")
def predire_api(data: InputPrediction):
    """
    Endpoint /predire (API ML simple).
    - Valide les données
    - Utilise pipeline_global.predire
    - Gère les erreurs avec HTTPException
    """

    # =========================
    # 7. GESTION ERREURS FASTAPI
    # =========================

    # Vérifications simples sur les données
    if len(data.donnees) == 0:
        raise HTTPException(status_code=422, detail="Liste de données vide")
    if min(data.donnees) < 0:
        raise HTTPException(status_code=422, detail="Valeurs négatives interdites")

    # Appel de la méthode de prédiction de PipelineML
    prediction = pipeline_global.predire(data.donnees)

    return {
        "pipeline": pipeline_global.nom,
        "prediction": prediction,
        "status": "ok"
    }


# =========================
# 8. TESTS PYTEST (DANS LE MÊME FICHIER POUR L’EXEMPLE)
# =========================

# En pratique, ce bloc irait dans un fichier séparé : test_main.py
from fastapi.testclient import TestClient

client = TestClient(app)


def test_ping():
    """
    Test de la route GET /ping
    """
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_predire_ok():
    """
    Test d'une prédiction valide.
    """
    response = client.post("/predire", json={"donnees": [1, 2, 3]})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "somme=6" in body["prediction"]


def test_predire_liste_vide():
    """
    Test d'une entrée invalide : liste vide.
    """
    response = client.post("/predire", json={"donnees": []})
    assert response.status_code == 422
    assert response.json()["detail"] == "Liste de données vide"


def test_predire_valeur_negative():
    """
    Test d'une entrée invalide : valeur négative.
    """
    response = client.post("/predire", json={"donnees": [-1, 2, 3]})
    assert response.status_code == 422
    assert response.json()["detail"] == "Valeurs négatives interdites"


# =========================
# 9. POINT D’ENTRÉE (LANCEMENT LOCAL)
# =========================

if __name__ == "__main__":
    # Petit test manuel en lançant l’API
    import uvicorn

    print("Lancement de l'API sur http://127.0.0.1:8000 ...")
    # uvicorn va utiliser l'objet 'app' défini plus haut
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
