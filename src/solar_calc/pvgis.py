#!/usr/bin/env python3
import requests
import sys

def fetch_pvgis_hourly(
    lat,
    lon,
    trackingtype,
    angle,
    aspect,
    start_year,
    end_year,
    peakpower,
    loss,
    pvtech,
    raddatabase,
    ):
    """
    Fetch an hourly time series from the PVGIS 'seriescalc' endpoint with desired parameters,
    returning JSON output.
    """
    url = "https://re.jrc.ec.europa.eu/api/seriescalc"

    params = {
        'lat': lat,
        'lon': lon,
        'trackingtype': trackingtype,
        'angle': angle,
        'aspect': aspect,
        'startyear': start_year,
        'endyear': end_year,
        'pvcalculation': 1,
        'peakpower': peakpower,
        'loss': loss,
        'pvtechchoice': pvtech,
        'raddatabase': raddatabase,
        'outputformat': 'json',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def main():
    try:
        data = fetch_pvgis_hourly(
                lat=45,
                lon=8,
                trackingtype=None,
                angle=25,
                aspect=0,
                start_year=2023,
                end_year=2023,
                peakpower=1.0,
                loss=14,
                pvtech='crystSi',
                raddatabase='PVGIS-SARAH3',
        )
    except requests.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

    # The hourly data lives under data['outputs']['hourly'], which is a list of dicts.
    hourly = data.get("outputs", {}).get("hourly", [])
    if not hourly:
        print("No hourly data found.", file=sys.stderr)
        sys.exit(1)

    # Print a header
    print(f"{'Time':>20} | {'P [W]':>10}")
    print("-" * 33)

    # Print the first 10 entries
    for entry in hourly[:10]:
        time = entry.get("time")
        prod = entry.get("P")
        print(f"{time:>20} | {prod:>10}")

if __name__ == "__main__":
    main()
