from dagster import MonthlyPartitionsDefinition
from dagster import WeeklyPartitionsDefinition
from taxi_trips.assets.constants import START_DATE, END_DATE

start_date = START_DATE
end_date = END_DATE

monthly_partition = MonthlyPartitionsDefinition(
    start_date = start_date,
    end_date = end_date
)

weekly_partition = WeeklyPartitionsDefinition(
    start_date = start_date,
    end_date = end_date
)