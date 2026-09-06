import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv

load_dotenv()

DOCS_USER = os.environ.get("DOCS_USER")
DOCS_PASSWORD = os.environ.get("DOCS_PASSWORD")

security = HTTPBasic()

def verify_docs(credentials: HTTPBasicCredentials = Depends(security)):
     """
     Vérifie les identifiants permettant d'accéder
     à Swagger, Redoc et OpenAPI.
     """

     # Si les variables ne sont pas configurées,
     # on refuse l'accès.
     if not DOCS_USER or not DOCS_PASSWORD:
         raise HTTPException(
             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
             detail="Documentation non configurée."
         )

     correct_username = secrets.compare_digest(
         credentials.username,
         DOCS_USER
     )

     correct_password = secrets.compare_digest(
         credentials.password,
         DOCS_PASSWORD
     )

     if not (correct_username and correct_password):
         raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Identifiants incorrects",
             headers={"WWW-Authenticate": "Basic"},
         )

     return credentials.username
