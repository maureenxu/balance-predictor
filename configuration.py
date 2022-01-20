from sklearn.ensemble import RandomForestRegressor


MODEL = RandomForestRegressor(n_jobs=-1)

PARAMS = {
        'n_estimators': 50,
        'max_depth': 3,
        'min_impurity_decrease': 0
}

TARGET = 'balanceAfterBooking_value_corr'

# Define the tier for training. There are 3 options: 'passive', 'medium', 'aggressive'
TIER = 'medium'

# the columns that contains nested data structure
NESTED_COLS = ['accountIdentification', 'category', 'balanceAfterBooking']

# the column name for the booking datetime
BOOKING_DT = 'bookingDateTimeGMT'

# the column name for the datetime object
DT_OBJ = 'date'

# the number for how many days to shift for the data preprocessing
SHIFT_NUM = 21

# the granularity for aggregation in data preprocessing step
# aggregate data by, 'D' by day, '1W' by week, 'M' by month, 'Y' by year
AGG_BY = 'D'

INPUT_OUTPUT_FILENAMES = {
    "preprocessor": {
        "input": "input.json",
        "output": "preprocessed_data.pickle"
    },
    "spliter":{
        "input": "preprocessed_data.pickle",
        "output_train": "training_data.pickle",
        "output_test": "testing_data.pickle"
    },
    "trainer":{
        "input": "training_data.pickle",
        "output": "model.pickle"
    },
    "validator":{
        "input_test": "testing_data.pickle",
        "input_model": "model.pickle",
        "output_metrics": "metrics_dict.pickle",
        "output_plot": "hist_vs_pred.png" 
    }
}
