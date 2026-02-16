#FastAPI simple

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class InputML(BaseModel):
    donnees: list


@app.post("/predire")
def predire(data: InputML):
    return {"prediction": len(data.donnees)}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)