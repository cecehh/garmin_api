import logging

import garminconnect
from fastapi import APIRouter, Depends, HTTPException

from helpers import get_client, parse_date, today_str, get_cached, set_cached
from models import heart_rate

logger = logging.getLogger("garmin_api.heart_rate")
router = APIRouter(prefix="/heart-rate", tags=["Fréquence cardiaque"])


def _fetch(target: str, client: garminconnect.Garmin) -> heart_rate.HeartRateData:
    email = client.username
    cached = get_cached(email, "heart_rate", target)
    if cached:
        return cached

    try:
        data = client.get_stats(target)
        rhr_data = client.get_rhr_day(target)
    except Exception as e:
        logger.error("Erreur heart_rate(%s) : %s", target, e)
        raise HTTPException(status_code=500, detail=str(e))

    resting = None
    if isinstance(rhr_data, list) and rhr_data:
        resting = rhr_data[0].get("value")
    elif isinstance(rhr_data, dict):
        resting = rhr_data.get("restingHeartRate")

    result = heart_rate.HeartRateData(
        date=target,
        average_heart_rate=data.get("averageHeartRate"),
        max_heart_rate=data.get("maxHeartRate"),
        resting_heart_rate=resting or data.get("restingHeartRate"),
    )
    set_cached(email, "heart_rate", target, result)
    return result


@router.get("/today", response_model=heart_rate.HeartRateData, summary="FC d'aujourd'hui")
def get_today(client: garminconnect.Garmin = Depends(get_client)):
    return _fetch(today_str(), client)


@router.get("/{target_date}", response_model=heart_rate.HeartRateData, summary="FC d'une date (YYYY-MM-DD)")
def get_by_date(target_date: str, client: garminconnect.Garmin = Depends(get_client)):
    return _fetch(parse_date(target_date), client)
