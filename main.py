import netCDF4 as nc
from datetime import date, datetime
from calendar import monthrange
import matplotlib.pyplot as plt

DATASETS_DIR = "/home/paunstefan/Downloads/weather-data/"
MAX_TEMPERATURE_DATASET = DATASETS_DIR + "tx_ens_mean_0.25deg_reg_v25.0e.nc"
MIN_TEMPERATURE_DATASET = DATASETS_DIR + "tn_ens_mean_0.25deg_reg_v25.0e.nc"
PRECIPITATION_DATASET = DATASETS_DIR + "rr_ens_mean_0.25deg_reg_v25.0e.nc"

LONG_START = -40.375
LAT_START = 25.375
RESOLUTION = 0.25
OFFSET = 0.125

DAYS_START = (1950, 1, 1)

BUCHAREST_COORDS = (44.5, 26.034)  # lat, lon

# Variables parameters: (time, latitude, longitude)


def coords_pair_indexes(coords):
    return (coords_to_index(coords[0], RESOLUTION, OFFSET, LAT_START),
            coords_to_index(coords[1], RESOLUTION, OFFSET, LONG_START))


def round_nearest(x, mult):
    return round(x / mult) * mult


def coords_to_index(coord, resolution, offset, start):
    return ((round_nearest(coord, resolution) + offset) - start) / resolution


def date_to_index(date_obj):
    d0 = date(DAYS_START[0], DAYS_START[1], DAYS_START[2])
    delta = date_obj - d0
    return delta.days


def datestr_to_index(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    return date_to_index(date_obj)


class WeatherDataset():
    def __init__(self, dataset, variable_name):
        self.dataset = dataset
        self.variable_name = variable_name

    def datapoint(self, day, lat, lon):
        return self.dataset[self.variable_name][day, lat, lon]

    def monthly_data(self, year, month, lat, lon):
        days_range = monthrange(year, month)
        start_day = date_to_index(date(year, month, 1))
        end_day = date_to_index(date(year, month, days_range[1]))

        return (self.dataset[self.variable_name][start_day:(end_day+1), lat, lon]).data


max_ds = WeatherDataset(nc.Dataset(MAX_TEMPERATURE_DATASET), "tx")
min_ds = WeatherDataset(nc.Dataset(MIN_TEMPERATURE_DATASET), "tn")
pp_ds = WeatherDataset(nc.Dataset(PRECIPITATION_DATASET), "rr")


def plot_month(year, month, lat, lon):
    days = range(1, monthrange(year, month)[1] + 1)
    y1 = max_ds.monthly_data(year, month, lat, lon)
    y2 = min_ds.monthly_data(year, month, lat, lon)

    fig, ax = plt.subplots(figsize=(14, 7))

    ax.bar(days, y1, tick_label=days, width=1,
           edgecolor="white", color="red", linewidth=0.7)
    ax.bar(days, y2, tick_label=days, width=1,
           edgecolor="white", color="lightblue", linewidth=0.7)

    plt.show()


def main():
    pass


if __name__ == "__main__":
    main()
