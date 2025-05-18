from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class HourlyRecord(BaseModel):
    model_config = ConfigDict(
        extra='ignore',           # drop unexpected keys
        populate_by_name=True     # allow .dict(by_alias=True) and name-based population
    )
        
    time: str
    P: float      = Field(..., alias='P')         # production [W]
    G_i: float    = Field(..., alias='G(i)')      # global irradiance [W/m²]
    H_sun: float  = Field(..., alias='H_sun')     # sun hours fraction (or solar elevation?)
    T2m: float    = Field(..., alias='T2m')       # temperature at 2 m [°C]
    WS10m: float  = Field(..., alias='WS10m')     # wind speed at 10 m [m/s]
    Int: float    = Field(..., alias='Int')       # solar incidence angle [°]

class Outputs(BaseModel):
    model_config = ConfigDict(extra='ignore')
    hourly: List[HourlyRecord]

class PVGISResponse(BaseModel):
    model_config = ConfigDict(extra='ignore')
    outputs: Outputs