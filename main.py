import logging
import time

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi

from routers import stats, steps, calories, heart_rate

# --------------------------------------------------------------------------- #
#  App                                                                         #
# --------------------------------------------------------------------------- #

app = FastAPI(
    title="Garmin Connect API",
    description="API pour récupérer vos stats quotidiennes Garmin Connect.",
    version="1.0.0",
)

logger = logging.getLogger("garmin_api")

# --------------------------------------------------------------------------- #
#  Middleware — log chaque requête avec son temps de réponse                   #
# --------------------------------------------------------------------------- #

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s → %d (%.0fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response

# --------------------------------------------------------------------------- #
#  Routers                                                                     #
# --------------------------------------------------------------------------- #

app.include_router(stats.router)
app.include_router(steps.router)
app.include_router(calories.router)
app.include_router(heart_rate.router)

# --------------------------------------------------------------------------- #
#  Swagger — inject Basic Auth                                                 #
# --------------------------------------------------------------------------- #

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BasicAuth": {"type": "http", "scheme": "basic"}
    }
    for path in schema.get("paths", {}).values():
        for operation in path.values():
            operation["security"] = [{"BasicAuth": []}]
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi

# --------------------------------------------------------------------------- #
#  Root                                                                        #
# --------------------------------------------------------------------------- #

@app.get("/", tags=["Info"])
def root():
    return {"message": "Garmin Connect API opérationnelle 🏃", "docs": "/docs"}
