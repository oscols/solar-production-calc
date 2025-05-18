#!/usr/bin/env python3
import sys
import argparse
from solar_calc.pvgis import fetch_hourly_profile
from solar_calc.processor import average_monthly_profile

USER_TO_PVGIS_TRACKER = {
    0: 0,  # user 0=fixed  → API 0=fixed
    1: 3,  # user 1=vertical → API 3=vertical
    2: 5,  # user 2=horizontal → API 5=horizontal
    3: 2,  # user 3=dual-axis → API 2=dual-axis
}

def main():
    parser = argparse.ArgumentParser(
        description="Plot average hourly solar production via PVGIS"
    )
    parser.add_argument(
        "latitude",
        type=float,
        help="Latitude in decimal degrees"
    )
    parser.add_argument(
        "longitude",
        type=float,
        help="Longitude in decimal degrees"
    )
    parser.add_argument(
        "month",
        type=int,
        choices=range(1,13),
        help="Month (1-12) to average over"
    )
    parser.add_argument(
        "trackertype",
        type=int,
        choices=USER_TO_PVGIS_TRACKER.keys(),
        help=(
            "0=fixed, "
            "1=vertical single-axis tracking, "
            "2=horizontal single-axis tracking, "
            "3=dual-axis tracking"
        )
    )
    parser.add_argument(
        "angle",
        type=int,
        choices=range(0,91),
        help="Tilt angle in degrees (0-90)"
    )
    parser.add_argument(
        "aspect",
        type=int,
        choices=range(-180,181),
        help="Azimuth angle in degrees (-180 to 180)"
    )

    args = parser.parse_args()

    api_tracker = USER_TO_PVGIS_TRACKER[args.trackertype]

    try:
        pv_model = fetch_hourly_profile(
            lat=args.latitude,
            lon=args.longitude,
            trackingtype=api_tracker,
            angle=args.angle,
            aspect=args.aspect,
            startyear=2023,
            endyear=2023,
            pvcalculation=1,
            peakpower=1.0,
            loss=14,
            pvtechchoice="crystSi",
            raddatabase="PVGIS-SARAH3"
        )
    except Exception as e:
        print(f"Error fetching PVGIS profile: {e}", file=sys.stderr)
        sys.exit(1)

    hourly_records = pv_model.outputs.hourly
    profile = average_monthly_profile(hourly_records, month=args.month)

    print(profile)

if __name__ == "__main__":
    main()
