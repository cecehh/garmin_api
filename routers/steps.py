import logging

import garminconnect
from fastapi import APIRouter, Depends, HTTPException

from helpers import get_client, parse_date, today_str, get_cached, set_cached
from models import steps

logger = logging.getLogger("garmin_api.steps")
router = APIRouter(prefix="/steps", tags=["Pas"])


def _fetch(target: str, client: garminconnect.Garmin) -> steps.StepsData:
    email = client.username
    cached = get_cached(email, "steps", target)
    if cached:
        return cached

    try:
        data = client.get_stats(target)
    except Exception as e:
        logger.error("Erreur get_stats(%s) : %s", target, e)
        raise HTTPException(status_code=500, detail=str(e))

    result = steps.StepsData(
        date=target,
        total_steps=data.get("totalSteps"),
        step_goal=data.get("dailyStepGoal"),
        total_distance_meters=data.get("totalDistanceMeters"),
    )
    set_cached(email, "steps", target, result)
    return result


@router.get("/today", response_model=steps.StepsData, summary="Pas d'aujourd'hui")
def get_today(client: garminconnect.Garmin = Depends(get_client)):
    return _fetch(today_str(), client)


@router.get("/{target_date}", response_model=steps.StepsData, summary="Pas d'une date (YYYY-MM-DD)")
def get_by_date(target_date: str, client: garminconnect.Garmin = Depends(get_client)):
    return _fetch(parse_date(target_date), client)
