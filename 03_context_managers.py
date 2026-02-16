#Context Managers

class LoggerML:
    def __enter__(self):
        self.file = open("mlops.log", "a")
        self.file.write("\n=== Nouvelle session ===\n")
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.write("=== Fin session ===\n")
        self.file.close()


with LoggerML() as log:
    log.write("Modèle Churn entrainé\n")
    log.write("Pipeline déployé\n")