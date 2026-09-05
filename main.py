from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from routes.houblons import router as houblons_router
from routes.relations import router as relations_router
from validations import verify_docs


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


# Documentation Swagger protégée

@app.get("/docs", include_in_schema=False)
def protected_docs(
    _: str = Depends(verify_docs),
):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Carte Houblon - Swagger",
    )


# Documentation ReDoc protégée

@app.get("/redoc", include_in_schema=False)
def protected_redoc(
    _: str = Depends(verify_docs),
):
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Carte Houblon - ReDoc",
    )


# OpenAPI JSON protégé

@app.get("/openapi.json", include_in_schema=False)
def protected_openapi(
    _: str = Depends(verify_docs),
):
    return JSONResponse(
        get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
        )
    )


# Fichiers statiques

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


# Routes API

app.include_router(houblons_router)
app.include_router(relations_router)
