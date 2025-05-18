#!/usr/bin/env python3
import sys
import requests
from pvgis_models import PVGISResponse

def fetch_pvgis_hourly(**params):
    """
    Fetch an hourly time series from the PVGIS 'seriescalc' endpoint.
    Returns raw JSON.
    """
    url = "https://re.jrc.ec.europa.eu/api/seriescalc"
    response = requests.get(url, params={**params, "outputformat": "json"})
    response.raise_for_status()
    return response.json()

def main():
    params = {
        "lat": 45,
        "lon": 8,
        "trackingtype": None,
        "angle": 25,
        "aspect": 0,
        "startyear": 2023,
        "endyear": 2023,
        'pvcalculation': 1,
        "peakpower": 1.0,
        "loss": 14,
        "pvtechchoice": "crystSi",
        "raddatabase": "PVGIS-SARAH3",
    }

    try:
        raw = fetch_pvgis_hourly(**params)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

    # parse + validate into our Pydantic models
    pv = PVGISResponse.model_validate(raw)

    # now you have fully typed access:
    for rec in pv.outputs.hourly[:10]:
        print(f"{rec.time} → P={rec.P:.2f} W, G={rec.G_i:.1f} W/m², T2m={rec.T2m:.1f}°C")

if __name__ == "__main__":
    main()