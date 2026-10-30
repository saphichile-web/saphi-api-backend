from fastapi import FastAPI, HTTPException
import os
import psycopg

app = FastAPI(
    title="SAPHI Chile API",
    description="Plataforma AgTech de agricultura regenerativa",
    version="1.0.0"
)

DEVICE_CONNECTION_STRING = os.getenv("DEVICE_CONNECTION_STRING")


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


@app.get("/db-health")
def db_health():
    try:
        with psycopg.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=int(os.environ.get("DB_PORT", "5432")),
            sslmode=os.environ.get("DB_SSLMODE", "require"),
            connect_timeout=10
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()

        return {
            "status": "healthy",
            "database": "PostgreSQL",
            "platform": "SAPHI Chile"
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar a PostgreSQL"
        )

