#This file contains utility functions for organizing and parsing data from 
#the excel files that contain the human scored events from the Nicolet
#EEG files

import numpy as np
import pandas as pd
import MySQLdb
import datetime

def returnDataBlock(filename):
    #filename must be a csv file
    f = open(filename, 'r').read().split('\r')
    Header = [f[0].split(','), f[1].split(',')]
    dataBlock = []

    for i in range(3,24):
        dataBlock.append(f[i].split(','))
    
    df_out = pd.DataFrame(dataBlock)
    return df_out
    
    
def getSeizuresFromBlock(DF, filenames):
    #Getting date and filenames for the block
    [month, day, year] = DF.loc[0][0].split('/')
    year = '20' + year
    datenum = datetime.date.toordinal(datetime.date(int(year), int(month), int(day)))
    #Making filename reference for the block
    filenames = []
    fname = DF.loc[0][1]
    for i in range(2,np.shape(DF)[1]):
        if DF.loc[0][i]:
            fname = DF.loc[0][i]
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
        if DF.loc[1][i]:
            chan1.append((datenum, filenames[i-2], DF.loc[start_idx[0]][i], DF.loc[start_idx[0]+1][i]))
        
        if DF.loc[6][i]:
            chan2.append((datenum, filenames[i-2], DF.loc[start_idx[1]][i], DF.loc[start_idx[1]+1][i]))
            
        if DF.loc[11][i]:
            chan3.append((datenum, filenames[i-2], DF.loc[start_idx[2]][i], DF.loc[start_idx[2]+1][i]))
            
        if DF.loc[16][i]:
            chan4.append((datenum, filenames[i-2], DF.loc[start_idx[3]][i], DF.loc[start_idx[3]+1][i]))
    
    return [chan1, chan2, chan3, chan4]    



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
    
    for j in range(np.shape(df)[0]):
        sql = "INSERT INTO nicolet_event_log VALUES ({}, {}, {}, {}, {}, {}, {}, {});".format(*(df.loc[j][i] for i in range(8)))
    
    try:
        handle.execute(sql)
    except:
        print "INSERT statement failed!"
        raise
    
    handle.execute(sql)
    db.close()
