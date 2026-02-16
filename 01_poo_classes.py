#Classes et héritage

class ModeleML:
    def __init__(self, nom):
        self.nom = nom
    
    def predire(self, donnees):
        return f"Prédiction {self.nom}: {len(donnees)}"
    

class PipelineML(ModeleML):
    def __init__(self, nom):
        super().__init__(nom)
        self.etapes = 3
    
    def deployer(self):
        return f"Pipeline {self.nom} deployé {self.etapes} étapes"
    
#Tests
modele = ModeleML("Churn")
print(modele.predire([1, 2, 3]))

pipeline = PipelineML("ChurnPipeline")
print(pipeline.predire([10, 20]))
print(pipeline.deployer())