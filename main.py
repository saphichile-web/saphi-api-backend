from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import os
import logging
import psycopg

# ==================================================
# SAPHI CHILE - PLATAFORMA AGTECH
# Backend FastAPI + PostgreSQL + Microsoft Azure
# ==================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("saphi-api")

app = FastAPI(
    title="SAPHI Chile API",
    description="Plataforma AgTech de agricultura regenerativa",
    version="1.0.0"
)

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
# 2. SALUD DE LA API
# ==================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "saphi-api-backend"
    }


# ==================================================
# 3. CONEXIÓN CON POSTGRESQL
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

    except Exception:
        logger.exception("Error al verificar PostgreSQL")
        raise HTTPException(
            status_code=503,
            detail="Error de conexión con PostgreSQL"
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


# ==================================================
# 6. MÓDULO DE TELEMETRÍA DEL SUELO
# ==================================================

@app.get("/telemetria")
def listar_telemetria():
    try:
        with conectar_postgresql() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        "timestamp",
                        sensor_id,
                        cuartel_id,
                        humedad_10cm,
                        humedad_30cm,
                        humedad_60cm,
                        temperatura_suelo,
                        conductividad_electrica
                    FROM public."telemetria suelo"
                    ORDER BY "timestamp" DESC
                    LIMIT 10
                """)
                registros = cur.fetchall()

        mediciones = [
            {
                "timestamp": fila[0].isoformat()
                if fila[0] is not None else None,
                "sensor_id": fila[1],
                "cuartel_id": fila[2],
                "humedad_10cm": float(fila[3])
                if fila[3] is not None else None,
                "humedad_30cm": float(fila[4])
                if fila[4] is not None else None,
                "humedad_60cm": float(fila[5])
                if fila[5] is not None else None,
                "temperatura_suelo": float(fila[6])
                if fila[6] is not None else None,
                "conductividad_electrica": float(fila[7])
                if fila[7] is not None else None
            }
            for fila in registros
        ]

        return {
            "plataforma": "SAPHI Chile",
            "modulo": "Telemetría del suelo",
            "total_mediciones": len(mediciones),
            "mediciones": mediciones
        }

    except Exception:
        logger.exception("Error al consultar telemetría")
        raise HTTPException(
            status_code=503,
            detail="No fue posible consultar la telemetría del suelo"
        )


# ==================================================
# 7. MÓDULO DE SENSORES IoT
# ==================================================

@app.get("/sensores")
def listar_sensores():
    try:
        with conectar_postgresql() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        id,
                        codigo_sensor,
                        tipo_sensor,
                        fabricante,
                        modelo,
                        cuartel_id,
                        profundidad_cm,
                        fecha_instalacion,
                        estado
                    FROM public.sensores
                    ORDER BY id
                """)
                registros = cur.fetchall()

        sensores = [
            {
                "id": fila[0],
                "codigo_sensor": fila[1],
                "tipo_sensor": fila[2],
                "fabricante": fila[3],
                "modelo": fila[4],
                "cuartel_id": fila[5],
                "profundidad_cm": float(fila[6])
                if fila[6] is not None else None,
                "fecha_instalacion": fila[7].isoformat()
                if fila[7] is not None else None,
                "estado": fila[8]
            }
            for fila in registros
        ]

        return {
            "plataforma": "SAPHI Chile",
            "modulo": "Sensores IoT",
            "total_sensores": len(sensores),
            "sensores": sensores
        }

    except Exception:
        logger.exception("Error al consultar sensores")
        raise HTTPException(
            status_code=503,
            detail="No fue posible consultar los sensores"
        )


# ==================================================
# 8. DASHBOARD AGRONÓMICO SAPHI CHILE
# ==================================================

@app.get("/dashboard", include_in_schema=False)
def dashboard():
    archivo = Path(__file__).resolve().parent / "dashboard.html"

    if not archivo.is_file():
        logger.error("No se encontró dashboard.html")
        raise HTTPException(
            status_code=404,
            detail="Dashboard no disponible"
        )

    return FileResponse(
        archivo,
        media_type="text/html"
    )

# ==================================================
# 9. HISTORIAL DE TELEMETRÍA DEL SUELO
# ==================================================

@app.get("/telemetria/historial")
def historial_telemetria():
    """Últimas 100 mediciones, ordenadas cronológicamente."""
    try:
        with conectar_postgresql() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        "timestamp",
                        sensor_id,
                        cuartel_id,
                        humedad_10cm,
                        humedad_30cm,
                        humedad_60cm,
                        temperatura_suelo,
                        conductividad_electrica
                    FROM public."telemetria suelo"
                    ORDER BY "timestamp" DESC
                    LIMIT 100
                """)
                registros = cur.fetchall()

        mediciones = []
        for fila in reversed(registros):
            mediciones.append({
                "timestamp": fila[0].isoformat() if fila[0] is not None else None,
                "sensor_id": fila[1],
                "cuartel_id": fila[2],
                "humedad_10cm": float(fila[3]) if fila[3] is not None else None,
                "humedad_30cm": float(fila[4]) if fila[4] is not None else None,
                "humedad_60cm": float(fila[5]) if fila[5] is not None else None,
                "temperatura_suelo": float(fila[6]) if fila[6] is not None else None,
                "conductividad_electrica": float(fila[7]) if fila[7] is not None else None
            })

        return {
            "plataforma": "SAPHI Chile",
            "modulo": "Historial de telemetría del suelo",
            "tipo_datos": "demostrativos",
            "total_mediciones": len(mediciones),
            "mediciones": mediciones
        }

    except Exception:
        logger.exception("Error consultando historial de telemetría")
        raise HTTPException(
            status_code=503,
            detail="No fue posible consultar el historial de telemetría"
        )

# ============================================================
# SAPHI CHILE SpA
# MÓDULO DE DIAGNÓSTICO AGRONÓMICO
# ============================================================

@app.get("/diagnostico-agronomico")
def obtener_diagnostico_agronomico():

    try:
        conexion = conectar_postgresql()

        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT
                    d.id,
                    d.predio_id,
                    p.nombre AS nombre_predio,
                    d.nombre_cuartel,
                    d.cultivo,
                    d.variedad,
                    d.textura_suelo,
                    d.profundidad_efectiva_cm,
                    d.observaciones,
                    d.fecha_registro
                FROM public.diagnostico_agronomico AS d
                LEFT JOIN public.predios AS p
                    ON p.id = d.predio_id
                ORDER BY d.fecha_registro DESC, d.id DESC;
            """)

            filas = cursor.fetchall()

        conexion.close()

        diagnosticos = []

        for fila in filas:

            diagnosticos.append({
                "id": fila[0],
                "predio_id": fila[1],
                "nombre_predio": fila[2],
                "nombre_cuartel": fila[3],
                "cultivo": fila[4],
                "variedad": fila[5],
                "textura_suelo": fila[6],
                "profundidad_efectiva_cm": (
                    float(fila[7]) if fila[7] is not None else None
                ),
                "observaciones": fila[8],
                "fecha_registro": (
                    fila[9].isoformat() if fila[9] is not None else None
                )
            })

        return {
            "plataforma": "SAPHI Chile",
            "modulo": "Diagnóstico agronómico",
            "tipo_datos": "demostrativos",
            "total_diagnosticos": len(diagnosticos),
            "diagnosticos": diagnosticos
        }

    except Exception:

        logger.exception(
            "Error consultando diagnósticos agronómicos"
        )

        raise HTTPException(
            status_code=503,
            detail="No fue posible consultar los diagnósticos agronómicos"
        )
