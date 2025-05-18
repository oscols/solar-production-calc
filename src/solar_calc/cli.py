#!/usr/bin/env python3
import sys
import argparse
from solar_calc.pvgis import fetch_hourly_profile
from solar_calc.processor import average_monthly_profile
from solar_calc.plotter import plot_profile
from pathlib import Path


USER_TO_PVGIS_TRACKER = {
    0: 0,  # user 0=fixed  → API 0=fixed
    1: 3,  # user 1=vertical → API 3=vertical
    2: 5,  # user 2=horizontal → API 5=horizontal
    3: 2,  # user 3=dual-axis → API 2=dual-axis
}

TRACKER_NAMES = {
    0: "Fixed",
    1: "Vertical Single-Axis",
    2: "Horizontal Single-Axis",
    3: "Dual-Axis",
}

MONTHS = {
    1: "January",   2: "February",  3: "March",     4: "April",
    5: "May",       6: "June",      7: "July",      8: "August",
    9: "September", 10: "October",  11: "November", 12: "December",
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
        "peakpower",
        type=int,
        choices=range(1,1001),
        help="Peak power in W (1-1000)"
    )
    parser.add_argument(
        "--angle",
        type=int,
        choices=range(0,91),
        help="Tilt angle in degrees (0-90)"
    )
    parser.add_argument(
        "--aspect",
        type=int,
        choices=range(-180,181),
        help="Azimuth angle in degrees (-180 to 180)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Where to save the plot (filename or directory). If not set, shows interactively.",
        default=None,
    )

    args = parser.parse_args()

    # Validate conditional requirements
    t = args.trackertype
    if t == 0:
        if args.angle is None or args.aspect is None:
            parser.error("Fixed tilt requires --angle and --aspect to be set.")
    elif t in (1, 2):
        if args.aspect is None:
            parser.error("Single-axis tracking requires --aspect to be set.")
        args.angle = None  # single-axis tracking does not require aspect
    elif t == 3:
        args.angle = None  # dual-axis tracking does not require aspect
        args.aspect = None  # dual-axis tracking does not require angle

    api_tracker = USER_TO_PVGIS_TRACKER[args.trackertype]

    # Build API params
    params = {
        "lat": args.latitude,
        "lon": args.longitude,
        "trackingtype": api_tracker,
        "startyear": 2019,
        "endyear": 2023,
        "pvcalculation": 1,
        "peakpower": 1.0,
        "loss": 14,
        "pvtechchoice": "crystSi",
        "raddatabase": "PVGIS-SARAH3",
    }
    if args.angle is not None:
        params["angle"] = args.angle
    if args.aspect is not None:
        params["aspect"] = args.aspect

    # Fetch and validate data
    try:
        pv_model = fetch_hourly_profile(**params)
    except Exception as e:
        print(f"Error fetching PVGIS profile: {e}", file=sys.stderr)
        sys.exit(1)

    # Process data
    hourly_records = pv_model.outputs.hourly
    profile = average_monthly_profile(hourly_records, args.month, args.peakpower)

    # Prepare title components
    tracker_name = TRACKER_NAMES.get(args.trackertype, f"Type {args.trackertype}")
    month_name = MONTHS.get(args.month, f"Month {args.month}")

    # Generate a default filename
    filename = (
        f"solar_{args.latitude}_{args.longitude}_"
        f"{args.month:02d}_{tracker_name.replace(' ', '')}.png"
    )

    # Decide output path: save or show
    if args.output:
        out = Path(args.output)
        if out.is_dir():
            out.mkdir(parents=True, exist_ok=True)
            output_path = out / filename
        else:
            output_path = out
    else:
        output_path = None

    # Plot or save
    plot_profile(
        profile,
        title=f"Average Hourly Production",
        subtitle=(
            f"Latitude {args.latitude}°, Longitude {args.longitude}° - {month_name} - "
            f"{tracker_name}"
        ),
        tilt=args.angle,
        azimuth=args.aspect,
        output_path=str(output_path) if output_path else None,
    )


if __name__ == "__main__":
    main()
