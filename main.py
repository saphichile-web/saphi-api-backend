
from fastapi import FastAPI

app = FastAPI(
    title="SAPHI Chile API",
    description="Plataforma AgTech de agricultura regenerativa",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "plataforma": "SAPHI Chile",
        "estado": "operativa",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "saphi-api-backend"
    }

