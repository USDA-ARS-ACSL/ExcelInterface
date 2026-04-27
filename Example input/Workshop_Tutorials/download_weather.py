"""
Download hourly weather for Workshop NE_site from PSA API (NLDAS-2 + MRMS).
Output: NE_weather.csv (format matches CalibTool write_wea expectations).

Columns: climateID, weatherID, date, jday, hour, temperature, rh, wind, rain, srad
  - date: 'YYYY-MM-DD'
  - temperature: Celcius
  - rh: percent (0-100)
  - wind: m/s
  - rain: mm/hr
  - srad: MJ/m^2/hr
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent


# NE_site location + date range (matches Workshop Exercise_01 .tim)
#*** SYNCHRONIZER INFORMATION *****************************
#@ Initial time       dt            dtMin   DMul1         DMul2                 tFin #
#@ '05/01/2024'   0.0001        0.0000001     1.3           0.3          '10/31/2024'#

###NOTE to CHANGE###

LAT, LON = 41.0872, -100.7702
START = "2024-04-30" #(Initial Time)-1
END   = "2024-11-01" #(tFin)+1
CLIMATE_ID = "Proj_NE_Weather"
WEATHER_ID = "Proj_NE_weather"

EMAIL = "ARS-CLASSIM-Help@usda.gov"
ATTRS = "air_temperature,relative_humidity,wind_speed,shortwave_radiation,precipitation"


def fetch():
    url = (
        f"https://weather.covercrop-data.org/hourly?"
        f"email={EMAIL}&lat={LAT}&lon={LON}"
        f"&start={START}&end={END}&attributes={ATTRS}&output=csv"
    )
    print(f"Fetching PSA hourly @ ({LAT}, {LON}) [{START} -> {END}]...")
    df = pd.read_csv(url, storage_options={'User-Agent': 'CLASSIM'})
    print(f"  {len(df)} rows received")
    return df


def process(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['datetime'] = pd.to_datetime(df['date'])
    df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
    df['jday'] = df['datetime'].dt.dayofyear
    df['hour'] = df['datetime'].dt.hour

    df['temperature'] = df['air_temperature'].round(2)
    df['rh']   = (df['relative_humidity'] * 100.0).round(1)
    df['wind'] = df['wind_speed'].round(2)
    df['rain'] = df['precipitation'].round(4)
    df['srad'] = (df['shortwave_radiation'] * 3600.0 / 1e6).round(4)

    df['climateID'] = CLIMATE_ID
    df['weatherID'] = WEATHER_ID

    return df[['climateID', 'weatherID', 'date', 'jday', 'hour',
               'temperature', 'rh', 'wind', 'rain', 'srad']]


def main():
    df = fetch()
    out = process(df)
    out_path = HERE / "Proj_NE_Weather.csv"
    out.to_csv(out_path, index=False)
    print(f"\nWrote: {out_path}")
    print(f"  {len(out)} rows, {out['date'].iloc[0]} -> {out['date'].iloc[-1]}")
    print(f"  total_rain = {out['rain'].sum():.1f} mm")
    print(f"  mean_temp  = {out['temperature'].mean():.2f} degC")


if __name__ == "__main__":
    main()
