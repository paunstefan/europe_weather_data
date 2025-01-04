import netCDF4 as nc
from datetime import date, datetime, timedelta
from calendar import monthrange
import pathlib

LONG_START = -40.375
LAT_START = 25.375
RESOLUTION = 0.25
OFFSET = 0

DAYS_START = (1950, 1, 1)

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

def calculate_new_date(start_date: tuple, days_passed: int) -> tuple:
    """
    Calculate the new date given a start date and the number of days passed.

    Args:
    start_date (tuple): A tuple of (year, month, day) representing the start date.
    days_passed (int): The number of days passed since the start date.

    Returns:
    tuple: A tuple of (year, month, day) for the resulting date.
    """
    # Convert the tuple into a datetime object
    start_date_obj = datetime(start_date[0], start_date[1], start_date[2])
    
    # Add the number of days passed
    new_date_obj = start_date_obj + timedelta(days=days_passed)
    
    # Convert the datetime object back into a tuple
    return (new_date_obj.year, new_date_obj.month, new_date_obj.day)


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