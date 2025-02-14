from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


from pydantic import ValidationError

from .routers import tasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # autorise les requêtes HTTP en provenance de toutes les origines
    allow_origins=["*"],
    # autorise les headers HTTP Authorization
    allow_credentials=True,
    # autorise tous les verbes HTTP
    allow_methods=["*"],
    # autorise tous les headers HTTP
    allow_headers=["*"],
)


app.include_router(tasks.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    masque les détails de l'erreur et retourne une erreur générique
    intercepte toutes les erreurs de validation générées par Pydantic
    """
    return JSONResponse({"detail": "Bad Request"}, status_code=400)


@app.get("/")
def read_root():
    """
    Racine de l'API
    """
    return {"message": "Todolist API"}
