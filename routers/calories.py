import logging

import garminconnect
from fastapi import APIRouter, Depends, HTTPException

from helpers import get_client, parse_date, today_str, get_cached, set_cached
from models import calories

logger = logging.getLogger("garmin_api.calories")
router = APIRouter(prefix="/calories", tags=["Calories"])


def _fetch(target: str, client: garminconnect.Garmin) -> calories.CaloriesData:
    email = client.username
    cached = get_cached(email, "calories", target)
    if cached:
        return cached

    try:
        data = client.get_stats(target)
    except Exception as e:
        logger.error("Erreur get_stats(%s) : %s", target, e)
        raise HTTPException(status_code=500, detail=str(e))

    result = calories.CaloriesData(
        date=target,
        total_kilocalories=data.get("totalKilocalories"),
        active_kilocalories=data.get("activeKilocalories"),
        bmr_kilocalories=data.get("bmrKilocalories"),
        wellness_active_kilocalories=data.get("wellnessActiveKilocalories"),
    )
    set_cached(email, "calories", target, result)
    return result


@router.get("/today", response_model=calories.CaloriesData, summary="Calories d'aujourd'hui")
def get_today(client: garminconnect.Garmin = Depends(get_client)):
    return _fetch(today_str(), client)


@router.get("/{target_date}", response_model=calories.CaloriesData, summary="Calories d'une date (YYYY-MM-DD)")
def get_by_date(target_date: str, client: garminconnect.Garmin = Depends(get_client)):
    return _fetch(parse_date(target_date), client)
