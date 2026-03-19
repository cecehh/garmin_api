import logging
from datetime import date, datetime
from functools import lru_cache
from typing import Optional

import garminconnect
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config import settings

# --------------------------------------------------------------------------- #
#  Logging                                                                     #
# --------------------------------------------------------------------------- #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("garmin_api")

# --------------------------------------------------------------------------- #
#  Auth                                                                        #
# --------------------------------------------------------------------------- #

security = HTTPBasic(auto_error=True)


def get_client(credentials: HTTPBasicCredentials = Depends(security)) -> garminconnect.Garmin:
    """
    Crée et authentifie un client Garmin via Basic Auth.
    Si GARMIN_EMAIL / GARMIN_PASSWORD sont définis dans .env, les credentials
    HTTP sont ignorés et ceux du .env sont utilisés.
    """
    email = settings.garmin_email or credentials.username
    password = settings.garmin_password or credentials.password

    logger.info("Tentative de connexion Garmin pour : %s", email)
    try:
        client = garminconnect.Garmin(email, password)
        client.login()
        logger.info("Connexion Garmin réussie pour : %s", email)
        return client
    except garminconnect.GarminConnectAuthenticationError:
        logger.warning("Échec d'authentification Garmin pour : %s", email)
        raise HTTPException(status_code=401, detail="Identifiants Garmin invalides.")
    except garminconnect.GarminConnectConnectionError:
        logger.error("Impossible de joindre Garmin Connect.")
        raise HTTPException(status_code=503, detail="Impossible de contacter Garmin Connect.")
    except Exception as e:
        logger.exception("Erreur inattendue lors de la connexion Garmin.")
        raise HTTPException(status_code=500, detail=f"Erreur inattendue : {str(e)}")


# --------------------------------------------------------------------------- #
#  Date                                                                        #
# --------------------------------------------------------------------------- #

def today_str() -> str:
    return date.today().isoformat()


def parse_date(d: str) -> str:
    """Valide et retourne la date au format YYYY-MM-DD."""
    try:
        date.fromisoformat(d)
        return d
    except ValueError:
        raise HTTPException(status_code=422, detail="Format de date invalide. Utilisez YYYY-MM-DD.")


# --------------------------------------------------------------------------- #
#  Cache                                                                       #
# --------------------------------------------------------------------------- #

# Clé de cache = (email, date, minute) → expire automatiquement à la minute suivante
_cache: dict = {}


def _cache_key(email: str, endpoint: str, target_date: str) -> str:
    minute = datetime.now().strftime("%Y%m%d%H%M")
    return f"{email}:{endpoint}:{target_date}:{minute}"


def get_cached(email: str, endpoint: str, target_date: str):
    key = _cache_key(email, endpoint, target_date)
    if key in _cache:
        logger.info("Cache HIT  — %s / %s", endpoint, target_date)
        return _cache[key]
    return None


def set_cached(email: str, endpoint: str, target_date: str, value) -> None:
    key = _cache_key(email, endpoint, target_date)
    _cache[key] = value
    logger.info("Cache MISS — %s / %s (mis en cache)", endpoint, target_date)
