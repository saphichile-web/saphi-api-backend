from fastapi import FastAPI
app = FastAPI() 
@app.post("/api/v1/telemetry/ingest/")
@app.get("/api/v1/cuarteles/{id}/health-index/")
@app.get("/api/v1/recommendation/irrigaion/")
