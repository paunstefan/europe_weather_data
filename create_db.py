import netCDF4 as nc
import sys
sys.path.append("./")
from utils import *
import sqlite3

DATASETS_DIR = pathlib.Path("./datasets")
MAX_TEMPERATURE_DATASET = pathlib.Path("tx_ens_mean_0.25deg_reg_v30.0e.nc")
MIN_TEMPERATURE_DATASET = pathlib.Path("tn_ens_mean_0.25deg_reg_v30.0e.nc")
MEAN_TEMPERATURE_DATASET = pathlib.Path("tg_ens_mean_0.25deg_reg_v30.0e.nc")
PRECIPITATION_DATASET = pathlib.Path("rr_ens_mean_0.25deg_reg_v30.0e.nc")

COORDS = (44.5, 26.0)

INDEXES = coords_pair_indexes(COORDS)

max_ds = WeatherDataset(nc.Dataset(DATASETS_DIR / MAX_TEMPERATURE_DATASET), "tx")
min_ds = WeatherDataset(nc.Dataset(DATASETS_DIR / MIN_TEMPERATURE_DATASET), "tn")
mean_ds = WeatherDataset(nc.Dataset(DATASETS_DIR / MEAN_TEMPERATURE_DATASET), "tg")
pp_ds = WeatherDataset(nc.Dataset(DATASETS_DIR / PRECIPITATION_DATASET), "rr")

size = len(mean_ds.dataset["time"])

get_ds = lambda i, ds: ds.datapoint(i, INDEXES[0],INDEXES[1])

weather_data = []

for i in range(size):
    current_date = calculate_new_date(DAYS_START,i)
    weather_data.append({
        "index_d": i,
        "year": current_date[0],
        "month": current_date[1],
        "day": current_date[2],
        "min_t": float(get_ds(i,min_ds)),
        "max_t": float(get_ds(i,max_ds)),
        "mean_t": float(get_ds(i,mean_ds)),
        "pp": float(get_ds(i,pp_ds))
    }
    )
    # print(f"{i} {date[0]} {date[1]} {date[2]} {get_ds(i,min_ds)} {get_ds(i,max_ds)} {get_ds(i,mean_ds)} {get_ds(i,pp_ds)}")

database_dir = pathlib.Path("databases/")
database_file = pathlib.Path("weather_bucharest.db")
database_filepath = database_dir / database_file

# Create the directory
pathlib.Path.mkdir(database_dir, parents=True, exist_ok=True)

# Establish a connection to the database and set a cursor
db_con = sqlite3.connect(database_filepath)
db_cur = db_con.cursor()

# Create the main table
db_cur.execute(
    "CREATE TABLE IF NOT EXISTS weather(index_d INTEGER PRIMARY KEY, "
    "year INTEGER, "
    "month INTEGER, "
    "day INTEGER, "
    "min_t FLOAT, "
    "max_t FLOAT, "
    "mean_t FLOAT, "
    "pp FLOAT)"
)
db_con.commit()

# Insert the raw data into the database
db_cur.executemany(
    "INSERT OR IGNORE INTO weather(index_d, "
    "year, "
    "month, "
    "day, "
    "min_t, "
    "max_t, "
    "mean_t, "
    "pp) "
    "VALUES (:index_d, "
    ":year, "
    ":month, "
    ":day, "
    ":min_t, "
    ":max_t, "
    ":mean_t, "
    ":pp)",
    weather_data,
)
db_con.commit()

db_con.close()