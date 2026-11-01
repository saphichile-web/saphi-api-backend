
from fastapi import FastAPI, HTTPException
import os
import logging
import psycopg

# ==================================================
# SAPHI CHILE - PLATAFORMA AGTECH
# Backend FastAPI + PostgreSQL + Microsoft Azure
# Versión 1.0.0
# ==================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("saphi-api")

app = FastAPI(
    title="SAPHI Chile API",
    description="Plataforma AgTech de agricultura regenerativa",
    version="1.0.0"
)

# Configuración de Azure IoT Hub
DEVICE_CONNECTION_STRING = os.getenv("DEVICE_CONNECTION_STRING")


# ==================================================
# CONEXIÓN A POSTGRESQL
# ==================================================

def conectar_postgresql():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=int(os.environ.get("DB_PORT", "5432")),
        sslmode=os.environ.get("DB_SSLMODE", "require"),
        connect_timeout=10
    )


# ==================================================
# 1. PÁGINA PRINCIPAL
# ==================================================

@app.get("/")
async def root():
    return {
        "plataforma": "SAPHI Chile",
        "estado": "operativa",
        "version": "1.0.0"
    }


# ==================================================
# 2. ESTADO DE LA API
# ==================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "saphi-api-backend"
    }


# ==================================================
# 3. ESTADO DE POSTGRESQL
# ==================================================

@app.get("/db-health")
def db_health():
    try:
        with conectar_postgresql() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()

        return {
            "status": "healthy",
            "database": "PostgreSQL",
            "platform": "SAPHI Chile"
        }

    except psycopg.OperationalError:
        logger.exception("Error de conexión con PostgreSQL")
        raise HTTPException(
            status_code=503,
            detail="Error de conexión con PostgreSQL"
        )

    except Exception:
        logger.exception("Error al verificar PostgreSQL")
        raise HTTPException(
            status_code=503,
            detail="Error interno al verificar PostgreSQL"
        )


# ==================================================
# 4. MÓDULO DE EMPRESAS
# ==================================================

@app.get("/empresas")
def listar_empresas():
    try:
        with conectar_postgresql() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, nombre
                    FROM public.empresas
                    ORDER BY id
                """)
                registros = cur.fetchall()

        return {
            "plataforma": "SAPHI Chile",
            "total_empresas": len(registros),
            "empresas": [
                {
                    "id": fila[0],
                    "nombre": fila[1]
                }
                for fila in registros
            ]
        }

    except Exception:
        logger.exception("Error al consultar empresas")
        raise HTTPException(
            status_code=503,
            detail="No fue posible consultar las empresas"
        )


# ==================================================
# 5. MÓDULO DE PREDIOS AGRÍCOLAS
# ==================================================

@app.get("/predios")
def listar_predios():
    try:
        with conectar_postgresql() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        p.id,
                        p.nombre,
                        p.empresa_id,
                        e.nombre AS empresa
                    FROM public.predios AS p
                    LEFT JOIN public.empresas AS e
                        ON p.empresa_id = e.id
                    ORDER BY p.id
                """)
                registros = cur.fetchall()

        return {
            "plataforma": "SAPHI Chile",
            "total_predios": len(registros),
            "predios": [
                {
                    "id": fila[0],
                    "nombre": fila[1],
                    "empresa_id": fila[2],
                    "empresa": fila[3]
                }
                for fila in registros
            ]
        }

    except Exception:
        logger.exception("Error al consultar predios")
        raise HTTPException(
            status_code=503,
            detail="No fue posible consultar los predios"
        )
