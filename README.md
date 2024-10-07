# Using dagster to analyze NY Taxi Trips with REACT frontend
I've used Dagster's [sample project](https://github.com/dagster-io/project-dagster-university) and added backend and frontend modules to demonstrate how a Dagster ETL pipeline can be extended. 
While there is support for AWS integration in this project, I haven't worked on making it flexible, i.e. allowing the user to choose between local and cloud storage. If we return an object for assets defined in `taxi_trips > assets > trips.py and metrics.py`, they are automatically stored in an S3 bucket initialized by me. 
This project also has a built-in integration with github actions.

# Getting Started 
To get started on this project, after cloning the repo, you should set up a conda environment like so:
```
conda create -n "dagster-taxi-trips" python=3.11.8
conda activate dagster-taxi-trips
pip install dagster 
```
You will notice `setup.py` has names of a number of packages. Install these using
```
pip install -e ".[dev]"
```

Once this is done, you should be able to view the Dagster UI using the line
```
dagster dev
```

### Implementation Gotchas
Before running `dagster dev`, the user should make sure to check environment variables:
* The variables in `.env` file are assigned valid values. Since this project comes in with built-in S3 integration, Dagster will not run the code unless valid AWS access keys and a bucket name are provided. 

# Dagster UI: Assets and Materialization
Once you define variables in `.env` file, you should be able to open the UI and see an _asset lineage chart_ which has the following 7 components:
- taxi_zones_file
- taxi_trips_file
- taxi_zones
- taxi_trips
- manhattan_stats
- trips_by_week
- manhattan_map

Materializing these assets simply means running the functions defined to create these assets. When assets are materialized, data is stored in `taxi_trips > data`. Since these generated data can be large in size, I added paths for `raw` and `staging` folders, which have parquet and duckdb files respectively, to `gitignore`. 

### Implementation Gotchas
* In the file `assets > constants.py`, make sure to check the paths of all constants defined in assets. Asset definitions are in `trips.py` and `metrics.py`. 

Once assets are materialized, the screen should look like this:
![Dagster UI](/Users/eshan23/taxi-trips-dagster/taxi_trips/images/dagster_UI.png)


# Running the backend
The backend code is pretty straightforward. When assets are materialized, data is stored in `data > staging > data.duckdb`. I've calculated simple totals, i.e. `trips per month` and `trips per month per borough` using SQL queries that run on the duckdb table. API endpoints have been provided for these two analyses. 

To run the backend, type
```
uvicorn main:app --reload
```
from the backend folder on your terminal. Doing that should lead to a browser window like this:
![Backend](/Users/eshan23/taxi-trips-dagster/taxi_trips/images/backend.png)

# Running the REACT frontend
Initially, I tried to setup a file system myself, however when that did not work for a couple of hours, I decided to fall back on **Create React App (CRA) package** which provides everything built-in (Webpack, Babel etc.)

While this project comes built in with only 2 visualizations, more can be added with minimal effort. In addition, there is scope to beautiy the pages. My aim of setting up this project was to essentially demonstrate ability to build a functional app end to end. To run the existing frontend visuals, run:
```
PORT=3001 npm start
```
PORT=3001 is optional, but I did not because Dagster UI was already using PORT=3000 (the default). Running this successfully will yield a page like so:
![Frontend](/Users/eshan23/taxi-trips-dagster/taxi_trips/images/frontend.png)
The user can toggle between the two charts. 
