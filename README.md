# solar-production-calc

A command-line tool to fetch and plot average hourly solar production profiles from PVGIS.

## Features

- Fetches PVGIS data for a given latitude, longitude, month, and tracking type
- Computes average hourly production for the specified month
- Plots the profile interactively or saves it to file
- Supports fixed tilt, single-axis (vertical or horizontal), and dual-axis tracking

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/oscols/solar-production-calc.git
   cd solar-production-calc
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate     # macOS/Linux
   venv\Scripts\activate        # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   # or for editable / development install:
   pip install -e .
   ```

## Usage

```bash
solar-calc LAT LON MONTH TRACKERTYPE PEAKPOWER [--angle ANGLE] [--aspect AZIMUTH] [-o OUTPUT]
```

- `<LAT>`: latitude in decimal degrees (e.g. `45.0`)
- `<LON>`: longitude in decimal degrees (e.g. `8.0`)
- `<MONTH>`: month number (`1`–`12`)
- `<TRACKERTYPE>`:
  - `0` = Fixed tilt
  - `1` = Vertical single-axis tracking
  - `2` = Horizontal single-axis tracking
  - `3` = Dual-axis tracking
- `<PEAKPOWER>`: panel peak power (e.g. `450` W)

### Optional Arguments

- `--angle ANGLE`  Tilt angle in degrees (0–90); **required** for fixed or single-axis tracking
- `--aspect AZIMUTH`  Azimuth angle in degrees (–180 to 180); **required** for fixed tilt
- `-o, --output OUTPUT`  Filename or directory to save the plot. If omitted, the plot displays interactively.

### Examples

**Fixed tilt** (angle = 25°, azimuth = 0°), display:
```bash
solar-calc 45.0 8.0 6 0 450 --angle 25 --aspect 0
```

**Vertical single-axis** (angle = 30°), save to `plots/`:
```bash
solar-calc 45.0 8.0 6 1 450 --angle 30 -o plots/
```

**Dual-axis** (no angle or aspect):
```bash
solar-calc 45.0 8.0 6 3 450
```

## Requirements

- Python >= 3.8
- requests >= 2.0
- pydantic >= 2.0
- matplotlib >= 3.0

_No additional dependencies are required beyond what’s listed above._

## PVGIS Configuration

By default, this tool computes **unshaded production** using the following PVGIS settings:

- **loss**: 14 (%)
- **pvtechchoice**: `crystSi`
- **raddatabase**: `PVGIS-SARAH3`
- **Time span**: based on the past 5 years of meteorological data

## Contributing

Contributions, issues, and feature requests are welcome! Please open an issue or submit a pull request.

## License

MIT © Oscar Olsson
