from fastapi import FastAPI
import uvicorn  # usamos para escolher a porta
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# no front usamos o axios para conectar back e front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL do front-end em desenvolvimento
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/get_data")
async def get_data():
    return {"body": 'Hello World'}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)