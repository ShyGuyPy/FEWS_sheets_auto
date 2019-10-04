# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 14:39:03 2018

@author: Yaayu_Sulay
aseck@icprb.org

"""

# ---------------------------------------------------------------------------#
# ------------Import Python Modules------------------------------------------#
import gspread
import time
import pandas as pd
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
from shutil import copyfile

# ---------------------------------------------------------------------------#
# ---Define input/output files-----------------------------------------------#

# CS test, Oct 3, 2019 - want this to work when FEWS_Live runs
# maindirectory = "/home/user1/MODEL/p52fc05_sa/output/icprb//archived_daily_met_wma"
maindirectory = "/home/user1/MODEL/p52fc05/output/icprb//archived_daily_met_wma"

maindirectory2 = "/mnt/SSD2/LFFS_archives/archived_daily_met_wma"
maindirectory3 = "/home/user1/MODEL/ICPRBextras/ExtrasV1.0/csv_to_sheets/met_wma"
csvfilename1 = maindirectory + '/precip_temp.csv' + time.strftime("_%Y%m%d_%H")
csvfilename2 = maindirectory2 + '/precip_temp.csv' + time.strftime("_%Y%m%d_%H")
print
"Archiving the following files"
print
csvfilename1
print
csvfilename2
csvfilename = maindirectory3 + '/precip_temp.csv'
# name of google spreadsheet
gsheetname = 'precip_temp_ls'
# name .json file containing the google credentials
jsonfilename = maindirectory3 + '/client_secret.json'

# ---------------------------------------------------------------------------#
# ---Daily average of precip  -----------------------------------------------#

print
"Averaging precip data for A11001, A24031, A51059 "

# CS test, Oct 3, 2019 - want this to work when FEWS_Live runs
# file1= "/home/user1/FEWS/client/config_sa/Export/HSPF_TS/PRC.csv"
file1 = "/home/user1/FEWS_Live/data/fromFSS/HSPF_TS/PRC.csv"

frame = pd.DataFrame()
list_ = []
df = pd.read_csv(file1, index_col=0, header=0, skiprows=[1], sep=',',
                 parse_dates=[0], date_parser=pd.datetools.to_datetime)
list_.append(df)
frame = pd.concat(list_)
frame[frame == -999] = np.nan
df1 = frame.groupby(pd.TimeGrouper('D'))
df2 = df1.aggregate(np.nansum)
test1 = df2[['A11001', 'A24031', 'A51059']]
test1.columns = ['A11001- prc (in)', 'A24031 - prc (in)', 'A51059 - prc (in)']
test1.to_csv(csvfilename)

# ---------------------------------------------------------------------------#
# ---Daily average of temp  -------------------------------------------------#
print
"Averaging temp data for A11001"

# CS test, Oct 3, 2019 - want this to work when FEWS_Live runs
# file2 = "/home/user1/FEWS/client/config_sa/Export/HSPF_TS/TMP.csv"
file2 = "/home/user1/FEWS_Live/data/fromFSS/HSPF_TS/TMP.csv"

frame = pd.DataFrame()
list_ = []
df = pd.read_csv(file2, index_col=0, header=0, skiprows=[1], sep=',',
                 parse_dates=[0], date_parser=pd.datetools.to_datetime)
list_.append(df)
frame = pd.concat(list_)
frame[frame == -999] = np.nan
df1 = frame.groupby(pd.TimeGrouper('D'))
df2 = df1.aggregate(np.nanmean)
test2 = df2[['A11001']]
test2.columns = ['A11001- tmp (F)']
test1.to_csv(csvfilename)
test4 = pd.concat([test1, test2], axis=1)
test4.to_csv(csvfilename)
copyfile(csvfilename, csvfilename1)
copyfile(csvfilename, csvfilename2)

# ---------------------------------------------------------------------------#
# ---Copy contents of csv file to google spreadsheet-------------------------#
## use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(jsonfilename, scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
print
"Editing google sheet"
sheet = client.open(gsheetname).sheet1

# clear spreadsheet
range_of_cells = sheet.range('A1:F100')
for cell in range_of_cells:
    cell.value = ''
sheet.update_cells(range_of_cells)

# copy contents
fi = open(csvfilename)

row = 1
column = 1

for li in fi:
    items = li.strip().split(',')
    # print items
    for item in items:
        # print item
        sheet.update_cell(row, column, item)
        column += 1

    row += 1
    column = 1

fi.close

print
"Finished uploading wma met data "












