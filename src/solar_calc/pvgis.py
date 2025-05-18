#!/usr/bin/env python3
import sys
import requests
from solar_calc.pvgis_models import PVGISResponse

def fetch_pvgis_raw(**params) -> dict:
    """
    Fetch an hourly time series from the PVGIS 'seriescalc' endpoint.
    Returns raw JSON.
    """
    url = "https://re.jrc.ec.europa.eu/api/seriescalc"
    response = requests.get(url, params={**params, "outputformat": "json"})
    response.raise_for_status()
    return response.json()

def fetch_hourly_profile(**params) -> PVGISResponse:
    """
    Fetch and parse into a PVGISResponse model.
    """
    raw = fetch_pvgis_raw(**params)
    return PVGISResponse.model_validate(raw)