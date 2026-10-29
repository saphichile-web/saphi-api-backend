from fastapi import FastAPI
app = FastAPI() 
@app.post("/api/v1/telemetry/ingest/")
@app.get("/api/v1/cuarteles/{id}/health-index/")
@app.get("/api/v1/recommendation/irrigaion/")
def ingest_telemetry(data:TelemetryData):
pass
pass
def health_index (id):
pass
def get_recommendation_irrigacion():
pass
