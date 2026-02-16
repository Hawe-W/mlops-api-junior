#FastAPI + Erreurs

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class InputML(BaseModel):
    donnees: list

@app.post("/predire")
def predire(data: InputML):
    if len(data.donnees) == 0:
        raise HTTPExeption(422, "Donnees vides")
    if min(data.donnees) < 0:
        raise HTTPExeption(422, "Valeurs négatives")
    
    return {"prédiction": sum(data.donnees)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)