# E-OBS dataset processing and visualization

This repo contains Python code used to process and visualize
weather data from the E-OBS dataset (<https://cds.climate.copernicus.eu/cdsapp#!/dataset/insitu-gridded-observations-europe>).

The E-OBS dataset contains weather data starting from 1950 for the whole of Europe, with a grid resolution of 0.1 or 0.25 degrees.
The variables I used are: maximum temperature, minimum temperature and precipitation, with a grid resolution of 0.25 degrees.

The netCDF files stores data based on some dimensions. In this case the temperature/precipitation variables are indexed by:

* Time: days since 1950-01-01
* Latitude: increments of 0.25 degrees starting from 25.375
* Longitude: increments of 0.25 degrees starting from -40.375

## Usage

The `main.py` file contains some utility Python code for reading the data and
presenting it in a useful fashion. What you should modify there are the file paths
for the datasets. And additionally, new datasets.

The main focus is the `notebook.ipynb` file, which contains a Jupyter Notebook where
you can play with the data.

## References

* <https://towardsdatascience.com/read-netcdf-data-with-python-901f7ff61648>
* <https://www.giss.nasa.gov/tools/panoply/>
  