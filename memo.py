#Classes POO : Une classe crée des objets avec des données (self.nom) 
# et fonctions (predire).

class ModeleML:
    def __init__(self, nom):
        self.nom = nom

# Héritage : Une classe fille récupère tout du parent 
# + ajoute ses propres trucs.

class PipelineML(ModeleML):
    def deployer(self):
        return "Déployer"

# Méthode d'instance : Une méthode utilise self pour accéder 
# aux données de l'objet.

def predire(self, donnees):
    return f"{self.nom}: {len(donnees)}"

# Décorateur : @debug entoure une fonction pour ajouter du comportement.

@debug
def predire(self, donnees):
    return "resultat"

# Context manager : Gère auto l'ouverture/fermeture de fichiers (avec with).

class LoggerML:
    def __enter__(self): return self.file
    def __exit__(self, *args) self.file.close()

#FastAPI route : @app.post("/predire") expose une fonction en API HTTP.

@app.post("/predire")
def predire(data): return {"result": data}

#Pydantic : Valide les données d'entrée automatiquement.

class Input(BaseModel):
    donnees: list

# HTTPException : Renvoie une erreur HTTP propre (ex: 422).

raise HTTPException(422, "Donnees invalides")

#pytest TestClient : Teste ton API comme un vrai client HTTP.

response = client.post("/predire", json="donnees": [1,2])
assert response.status_code == 200

# pyproject.toml 
# Liste les dépendances du projet (remplace requirements.txt).

#[tool.poetry.dependencies]
# fastapi = "^0.115"
