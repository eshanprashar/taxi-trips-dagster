from dagster import ScheduleDefinition
from taxi_trips.jobs import trip_update_job, weekly_update_job

trip_update_schedule = ScheduleDefinition(
    job=trip_update_job,
    cron_schedule="0 0 * * *", # Run at midnight every day
)

weekly_update_schedule = ScheduleDefinition(
    job=weekly_update_job,
    cron_schedule="0 0 * * 1", # Run at midnight on Mondays
)