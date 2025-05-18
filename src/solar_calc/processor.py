from datetime import datetime
from typing import List
from solar_calc.pvgis_models import HourlyRecord


def average_monthly_profile(hourly_records: List[HourlyRecord], month: int) -> List[float]:
    """
    Given a list of HourlyRecord and a month (1-12),
    returns a list of 24 average production values per hour for that month.
    """
    # Initialize sums and counts for each hour 0-23
    sums = [0.0] * 24
    counts = [0] * 24

    for rec in hourly_records:
        # Parse timestamp string 'YYYYMMDD:HHMM'
        try:
            dt = datetime.strptime(rec.time, '%Y%m%d:%H%M')
        except ValueError:
            continue  # skip malformed entries

        # Filter by requested month
        if dt.month == month and rec.P is not None:
            hour = dt.hour
            sums[hour] += rec.P
            counts[hour] += 1

    # Compute average for each hour
    avg_profile: List[float] = []
    for hour in range(24):
        if counts[hour] > 0:
            avg_profile.append(sums[hour] / counts[hour])
        else:
            avg_profile.append(0.0)

    return avg_profile
