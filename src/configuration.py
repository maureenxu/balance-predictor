from sklearn.ensemble import RandomForestRegressor

# pylint: disable=too-few-public-methods
class Config:
    # Define the tier for training. There are 3 options: 'passive', 'medium', 'aggressive'
    TIER = "medium"

    TARGET: str = "balanceAfterBooking_value_corr"

    # the column name for the datetime object
    DT_OBJ: str = "date"

    # the column name for the booking datetime
    BOOKING_DT: str = "bookingDateTimeGMT"

    MODEL = RandomForestRegressor(n_jobs=-1)

    PARAMS = {
        "n_estimators": 50,
        "max_depth": 3,
    }

    RESOURCES_FOLDER = "data"

    # the columns that contains nested data structure
    NESTED_COLS = ["accountIdentification", "category", "balanceAfterBooking"]

    # the number for how many days to shift for the data preprocessing
    SHIFT_NUM = 21

    # the granularity for aggregation in data preprocessing step
    # aggregate data by, 'D' by day, '1W' by week, 'M' by month, 'Y' by year
    AGG_BY = "D"
