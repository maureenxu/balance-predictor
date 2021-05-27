from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

MODEL = RandomForestRegressor(n_jobs=-1)

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
