from setuptools import find_packages, setup

setup(
    name="taxi_trips",
    packages=find_packages(exclude=["taxi_trips_tests"]),
    install_requires=[
        "dagster==1.7.*",
        "dagster-aws",
        "dagster-cloud",
        "dagster-duckdb",
        "pandas",
        "matplotlib",
        "geopandas",
        "kaleido",
        "plotly",
        "shapely",
        "fastapi",
        "uvicorn",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
