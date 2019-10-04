#################precip_to_sheets.py

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 05 11:46:02 2017

@author: Yaayu_Sulay
"""
import os
import gspread
import time
import pandas as pd
import datetime as dt
import numpy as np
#import matplotlib.pyplot as plt
#import glob
from oauth2client.service_account import ServiceAccountCredentials
from shutil import copyfile

t0 = time.time()

precip_file= "/home/user1/MODEL/p52fc05/output/icprb/MASP_MARFC_PRC.csv"
precip_file2= "/home/user1/MODEL/p52fc05_sa/output/icprb/archived_masp_marfc_prc/masp_marfc_weight_ave.csv" + time.strftime("%Y%m%d")
precip_file3= "/mnt/SSD2/LFFS_archives/archived_masp_marfc_prc/masp_marfc_weight_ave.csv" + time.strftime("_%Y%m%d_%H")
#f1 = os.path.join(directory1,precip_file)
weight_file = "/home/user1/MODEL/ICPRBextras/ExtrasV1.0/csv_to_sheets/weight1.csv"
#f1 = os.path.join(directory1,precip_file)
list_ = []
df = pd.read_csv(precip_file, index_col=0, header=0, skiprows=[1],  sep=',', parse_dates=[0],  date_parser= pd.datetools.to_datetime)
list_.append(df)
frame = pd.concat(list_)
frame[frame == -999] = np.nan
test1 = frame
test1.to_csv('/home/user1/MODEL/ICPRBextras/ExtrasV1.0/csv_to_sheets/out.csv')
weight= pd.read_csv(weight_file, header=0,  skiprows=[1], sep=',')
test2=pd.DataFrame(test1.values*weight.values, columns=test1.columns, index=test1.index)
#print test2
test3 = test1
test3['weight_avg'] = test2.sum(skipna=False,axis=1)
test3['avg'] = test1.mean(axis=1)
#alima=test2['weight_avg']
test3.to_csv('/home/user1/MODEL/ICPRBextras/ExtrasV1.0/csv_to_sheets/out3.csv')
#print alima


#directory1= "H:\ICPRB2\USERS2\COOP\Drought Exercise-Operations\lffs_interface\lffs_output\precip"
#precip_file = "MARFC_PRC.csv"
#f1 = os.path.join(directory1,precip_file)
precip_file1 = "/home/user1/MODEL/ICPRBextras/ExtrasV1.0/csv_to_sheets/out3.csv"
copyfile(precip_file1, precip_file2)
copyfile(precip_file1, precip_file3)
f1 = precip_file1
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/user1/MODEL/ICPRBextras/ExtrasV1.0/csv_to_sheets/client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("marfc_precip_test").sheet1
range_of_cells = sheet.range('A1:S100')
for cell in range_of_cells:
    cell.value = ''
sheet.update_cells(range_of_cells)

# Extract and print all of the values
#list_of_hashes = sheet.get_all_records()
#print(list_of_hashes)

fi = open(f1)

row = 1
column = 1

for li in fi:
    items = li.strip().split(',')
    #print items
    for item in items:
        #print item
        sheet.update_cell(row, column, item)
        column += 1

    row += 1
    column = 1



#worksheet.update_cells(cell_list)

fi.close()

#print(list_of_hashes)

t1 = time.time()

total = t1-t0

print "finished in how many seconds?"
print total













##############sa_global.properties
IMPORT_FOLDER_ROOT=%REGION_HOME%/Import
BACKUP_FOLDER_ROOT=%REGION_HOME%/Import/backup
FAILED_FOLDER_ROOT=%REGION_HOME%/Import/failed
EXPORT_FOLDER_ROOT=%REGION_HOME%/Export
GA_DUMPFILEDIR=%REGION_HOME%/DumpFiles
DEFAULT_EXPIRY_DAYS=30
MODELDIR=%REGION_HOME%/Models
alwaysAllowDummyModuleInstanceRuns=false
alwaysAllowWriteSimulatedBelongingToAlreadyRunnedModuleInstance=false
timeSeriesDefaultCacheSizeMB=50
TEMP_DIR=/tmp
INFORMATION_PANEL_FOLDER=%REGION_HOME%/E19
docking=true
PYTHON_EXE=/usr/bin/python
#LANGUAGE=es
#runInLoopParallelProcessorCount
localDatastoreFormat=firebird
BACKUP_FOLDER_ROOT=$IMPORT_FOLDER_ROOT$/backup


#testing paths to update in sa_global properties file
FM_INPUT_DIR=/home/user1/MODEL/p52fc05_sa/input/icprb/
FORTRAN_TXT_DIR=/home/user1/MODEL/p52fc05_sa/input/forecast/
CSHELL_DIR=/home/user1/MODEL/p52fc05_sa/run/datascripts/forecast/
CONTROL_DIR=/home/user1/MODEL/p52fc05_sa/config/control/
PLTGEN_RIV_DIR=/home/user1/MODEL/p52fc05_sa/output/pltgen/river/p52Luke/
PLTGEN_LAND_DIR=/home/user1/MODEL/p52fc05_sa/output/pltgen/land/p52Luke/

#FEWS IP Address Server
#FEWSSERVER=192.168.1.208:8110
#FEWSSERVER=192.168.1.219:8110
FEWSSERVER=192.168.1.223:8110
#FEWSSERVER=192.168.1.222:8110

#testing running executables
CSHELL_EXE=/usr/bin/csh
WDM_PRAD=/home/user1/MODEL/p52fc05_sa/run/datascripts/forecast/insert_prad_wdms.csh
WDM_MET=/home/user1/MODEL/p52fc05_sa/run/datascripts/forecast/insert_met_wdms.csh
WDM_PS=/home/user1/MODEL/p52fc05_sa/run/datascripts/forecast/insert_ps_wdms.csh
WDM_DIV=/home/user1/MODEL/p52fc05_sa/run/datascripts/forecast/insert_div_wdms.csh
RUN_HSPF=/home/user1/MODEL/p52fc05_sa/run/standard/run_all.csh
#ICPRB, Dec 2015: adding next 3 lines to report P5 failure notification:
BASH_EXE=/usr/bin/bash
RUN_FAILNOTIF=/home/user1/MODEL/ICPRBextras/ExtrasV1.0/notif_email/lffs_notif.sh
ICPRB_OUTPUT=/home/user1/MODEL/p52fc05_sa/output/icprb/
NOTIF_DIR=/home/user1/MODEL/p52fc05_sa/output/pltgen/river/p52Luke
#ICPRB, November 2017: add line to pubish csv precip to google sheet
PUBLISH_PRECIP=/home/user1/MODEL/ICPRBextras/ExtrasV1.0/csv_to_sheets/precip_csv_to_sheets.py
PUBLISH_WMA_MET=/home/user1/MODEL/ICPRBextras/ExtrasV1.0/csv_to_sheets/met_wma/daily_met_wma_to_sheets.py
#Archive Directory
ARCHIVE_DIR=//mnt/SSD2/LFFS_archives
#ARCHIVE_DIR=/home/user1/archivedir_temp









