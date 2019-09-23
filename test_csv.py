import pandas as pd
import numpy as np
#import datetime as dt

precip_file = r"/Users/lukevawter/Desktop/Python_ICPRB/FEWS_sheets_auto/input/Reservoir_intake_retweaked.csv"

df = pd.read_csv(precip_file) #, index_col=0, header=0, skiprows=[1],  sep=',', parse_dates=[0],  date_parser= pd.datetools.to_datetime)

list_ = []
list_.append(df)
frame = pd.concat(list_)
frame[frame == -999] = np.nan
test1 = frame
test1.to_csv('/Users/lukevawter/Desktop/Python_ICPRB/FEWS_sheets_auto/output/out_Reservoir_intake_retweaked.csv')
