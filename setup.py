from setuptools import find_packages, setup

setup(
    name="taxi_trips",
    packages=find_packages(exclude=["taxi_trips_tests"]),
    install_requires=[
        "dagster",
        "dagster-aws",
        "dagster-cloud",
        "pandas",
        "matplotlib"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
