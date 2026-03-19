import logging
from datetime import date, timedelta

import garminconnect
from fastapi import APIRouter, Depends, HTTPException

from helpers import get_client, parse_date, today_str, get_cached, set_cached
from models import daily_stats

logger = logging.getLogger("garmin_api.stats")
router = APIRouter(prefix="/stats", tags=["Stats quotidiennes"])


def _fetch(target: str, client: garminconnect.Garmin) -> daily_stats.DailyStats:
    email = client.username
    cached = get_cached(email, "stats", target)
    if cached:
        return cached

    try:
        data = client.get_stats(target)
    except Exception as e:
        logger.error("Erreur get_stats(%s) : %s", target, e)
        raise HTTPException(status_code=500, detail=str(e))

    result = daily_stats.DailyStats(
        date=target,
        total_steps=data.get("totalSteps"),
        step_goal=data.get("dailyStepGoal"),
        total_distance_meters=data.get("totalDistanceMeters"),
        total_kilocalories=data.get("totalKilocalories"),
        active_kilocalories=data.get("activeKilocalories"),
        bmr_kilocalories=data.get("bmrKilocalories"),
        wellness_active_kilocalories=data.get("wellnessActiveKilocalories"),
        average_heart_rate=data.get("averageHeartRate") or data.get("restingHeartRate"),
        max_heart_rate=data.get("maxHeartRate"),
        resting_heart_rate=data.get("restingHeartRate"),
        average_stress_level=data.get("averageStressLevel"),
        floor_climbed=data.get("floorsAscended"),
        minutes_sedentary=data.get("sedentaryMinutes"),
        minutes_lightly_active=data.get("lightlyActiveMinutes"),
        minutes_moderately_active=data.get("fairlyActiveMinutes"),
        minutes_highly_active=data.get("veryActiveMinutes"),
    )
    set_cached(email, "stats", target, result)
    return result


@router.get("/today", response_model=daily_stats.DailyStats, summary="Stats d'aujourd'hui")
def get_today(client: garminconnect.Garmin = Depends(get_client)):
    return _fetch(today_str(), client)


@router.get("/{target_date}", response_model=daily_stats.DailyStats, summary="Stats d'une date (YYYY-MM-DD)")
def get_by_date(target_date: str, client: garminconnect.Garmin = Depends(get_client)):
    return _fetch(parse_date(target_date), client)


@router.get("/range/{start_date}/{end_date}", summary="Stats sur une plage (max 31 jours)")
def get_range(
    start_date: str,
    end_date: str,
    client: garminconnect.Garmin = Depends(get_client),
):
    start = date.fromisoformat(parse_date(start_date))
    end = date.fromisoformat(parse_date(end_date))

    if end < start:
        raise HTTPException(status_code=400, detail="end_date doit être >= start_date.")
    if (end - start).days > 31:
        raise HTTPException(status_code=400, detail="Plage maximale : 31 jours.")

    results = []
    current = start
    while current <= end:
        try:
            day = _fetch(current.isoformat(), client)
            results.append(day.model_dump())
        except HTTPException:
            results.append({"date": current.isoformat(), "error": "données indisponibles"})
        current += timedelta(days=1)

    return {"start_date": start_date, "end_date": end_date, "days": len(results), "data": results}
