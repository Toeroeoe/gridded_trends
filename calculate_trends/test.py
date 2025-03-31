
from datarie import time, templates
from custom_funcs import baseline_anomalies, mannkendall
from data_config import ESACCI_SM

import numpy as np

baseline_y0 = 2003
baseline_y1 = 2016
y0 = 2002
y1 = 2022
m0 = 4
m1 = 7
time_res = 'MS'
leapday = False
test = 'seasonal_test'
period = 12

data_ = templates.gridded_data(**ESACCI_SM)

arrays = data_.get_values('SM',
                          y0 = y0,
                          y1 = y1,
                          m0 = m0,
                          m1 = 7)['SM'][:, 1158, 773]

time_index = time.index(y0 = y0,
                        y1 = y1,
                        month0 = m0,
                        month1 = m1,
                        t_res = time_res,
                        leapday = leapday)

anomalies = baseline_anomalies(arrays = {'SM': arrays},
                               baseline_y0 = baseline_y0,
                               baseline_y1 = baseline_y1,
                               time_index = time_index)


trend = mannkendall(anomalies,
                    test = test,
                    period = period)



print(arrays)
print(anomalies['SM'])
print(len(arrays))
print(len(anomalies['SM']))

print(np.count_nonzero(~np.isnan(arrays)), np.count_nonzero(~np.isnan(anomalies['SM'])))

print(trend)

