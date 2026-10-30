from pydantic import BaseModel
from fastapi import FastAPI
app = FastAPI() 
class TelemetryData(BaseModel)
pass
@app.post("/api/v1/telemetry/ingest/")
def ingest_telemetry(data:TelemetryData):
  pass
@app.get("/api/v1/cuarteles/{id}/health-index/")
def health_index(id: str):
  pass
@app.get("/api/v1/recommendation/irrigaion/")
def get_recommendation_irrigacion():
  pass
def get_recommendation_irrigacion():
  pass
