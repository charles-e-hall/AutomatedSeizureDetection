#This file contains utility functions for organizing and parsing data from 
#the excel files that contain the human scored events from the Nicolet
#EEG files

import numpy as np
#import pandas as pd
import MySQLdb
import datetime

def returnDataBlock(filename):
    #filename must be a csv file
    f = open(filename, 'r').read().split('\r')
    Header = [f[0].split(','), f[1].split(',')]
    dataBlock = []

    for i in range(3,24):
        dataBlock.append(f[i].split(','))
    
#    df_out = pd.DataFrame(dataBlock)
#    return df_out
    return dataBlock
    
    
def getSeizuresFromBlock(DF):
    #Getting date and filenames for the block
    [month, day, year] = DF[0][0].split('/')
    year = '20' + year
    datenum = datetime.date.toordinal(datetime.date(int(year), int(month), int(day)))
    #Making filename reference for the block
    filenames = []
    fname = DF[0][1]
    for i in range(2,np.shape(DF)[1]):
        if DF[0][i]:
            fname = DF[0][i]
            filenames.append(fname)
        else:
            filenames.append(fname)
    
    #Channel starting indices (1,6,11,16)
    start_idx = [1, 6, 11, 16]
    chan1 = []
    chan2 = []
    chan3 = []
    chan4 = []

    for i in range(2,np.shape(DF)[1]):
        if DF[1][i]:
            ts1 = (datenum+float(DF[start_idx[0]][i].split(':')[0])+float(DF[start_idx[0]][i].split(':')[1])/60+float(DF[start_idx[0]][i].split(':')[2])/3600)/24.
            ts2 = (datenum+float(DF[start_idx[0]+1][i].split(':')[0])+float(DF[start_idx[0]+1][i].split(':')[1])/60.+float(DF[start_idx[0]+1][i].split(':')[2])/3600.)/24.
            chan1.append((filenames[i-2], datenum, 1, DF[start_idx[0]][i], DF[start_idx[0]+1][i], ts1, ts2))
        
        if DF[6][i]:
            ts1 = (datenum+float(DF[start_idx[1]][i].split(':')[0])+float(DF[start_idx[1]][i].split(':')[1])/60.+float(DF[start_idx[1]][i].split(':')[2])/3600.)/24.
            ts2 = (datenum+float(DF[start_idx[1]+1][i].split(':')[0])+float(DF[start_idx[1]+1][i].split(':')[1])/60.+float(DF[start_idx[1]+1][i].split(':')[2])/3600.)/24.
            chan2.append((filenames[i-2], datenum, 2, DF[start_idx[1]][i], DF[start_idx[1]+1][i], ts1, ts2))
            
        if DF[11][i]:
            ts1 = (datenum+float(DF[start_idx[2]][i].split(':')[0])+float(DF[start_idx[2]][i].split(':')[1])/60.+float(DF[start_idx[2]][i].split(':')[2])/3600.)/24.
            ts2 = (datenum+float(DF[start_idx[2]+1][i].split(':')[0])+float(DF[start_idx[2]+1][i].split(':')[1])/60.+float(DF[start_idx[2]+1][i].split(':')[2])/3600.)/24.
            chan3.append((filenames[i-2], datenum, 3, DF[start_idx[2]][i], DF[start_idx[2]+1][i], ts1, ts2))
            
        if DF[16][i]:
            ts1 = (datenum+float(DF[start_idx[3]][i].split(':')[0])+float(DF[start_idx[3]][i].split(':')[1])/60.+float(DF[start_idx[3]][i].split(':')[2])/3600.)/24.
            ts2 = (datenum+float(DF[start_idx[3]+1][i].split(':')[0])+float(DF[start_idx[3]+1][i].split(':')[1])/60.+float(DF[start_idx[3]+1][i].split(':')[2])/3600.)/24.
            chan4.append((filenames[i-2], datenum, 4, DF[start_idx[3]][i], DF[start_idx[3]+1][i], ts1, ts2))
    
    SeizureDF = []

    if chan1:
        SeizureDF.append(chan1)
    elif chan2:
        SeizureDF.append(chan2)
    elif chan3:
        SeizureDF.append(chan3)
    elif chan4:
        SeizureDF.append(chan4)

    return SeizureDF




def insertEvents(df, Host, Port, DB, uname, pwd):
    db = MySQLdb.connect(host=Host, port=Port, user=uname, passwd=pwd, db=DB)
    handle = db.cursor()
#    Assumes following table layout
#    sql = "CREATE TABLE nicolet_event_log (
#                prkey INT, 
#                filename VARCHAR(40), 
#                datenum INT, 
#                channel INT, 
#                event_start VARCHAR(40), 
#                event_stop VARCHAR(40), 
#                event_start_tmstmp FLOAT, 
#                event_stop_tmstmp FLOAT);"
    
#    for j in range(np.shape(df)[0]):
#        sql = "INSERT INTO nicolet_event_log VALUES ({}, {}, {}, {}, {}, {}, {}, {});".format(*(df.loc[j][i] for i in range(8)))
 
    for j in range(np.shape(df)[0]):
        sql = "INSERT INTO nicolet_event_log VALUES ({}, {}, {}, {}, {}, {}, )"

    try:
        handle.execute(sql)
    except:
        print "INSERT statement failed!"

    
    handle.execute(sql)
    db.close()
