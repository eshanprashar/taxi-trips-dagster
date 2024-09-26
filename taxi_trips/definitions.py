from dagster import (
    Definitions,
    EnvVar,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
    load_assets_from_modules
)
from .assets import trips, metrics
from .resources import database_resource
from .jobs import trip_update_job, weekly_update_job
from .schedules import trip_update_schedule, weekly_update_schedule
from dagster_aws.s3 import S3PickleIOManager, S3Resource

trip_assets = load_assets_from_modules([trips])
metric_assets = load_assets_from_modules([metrics])

all_schedules = [trip_update_schedule, weekly_update_schedule]
all_jobs = [trip_update_job, weekly_update_job]

my_s3_resource = S3Resource()

defs = Definitions(
    assets=[*trip_assets, *metric_assets],
    # The AWS resources use boto under the hood, so if you are accessing your private
    # buckets, you will need to provide the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    # environment variables or follow one of the other boto authentication methods.
    # Read about using environment variables and secrets in Dagster:
    #   https://docs.dagster.io/guides/dagster/using-environment-variables-and-secrets
    resources={
        "database": database_resource,
        # With this I/O manager in place, your job runs will store data passed between assets
        # on S3 in the location s3://<bucket>/dagster/storage/<asset key>.
        "io_manager": S3PickleIOManager(
            s3_resource=my_s3_resource,
            s3_bucket=EnvVar("S3_BUCKET"),
        ),
        "s3": my_s3_resource,
    },
    jobs=all_jobs,
    schedules=all_schedules,
)
