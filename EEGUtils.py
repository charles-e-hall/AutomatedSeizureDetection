#This file contains utility functions for organizing and parsing data from 
#the excel files that contain the human scored events from the Nicolet
#EEG files

import numpy as np
#import pandas as pd
import MySQLdb
import datetime
from Crypto.Hash import MD5
import math

def returnDataBlock(filename, blocknum):
    #filename must be a csv file
    f = open(filename, 'r').read().split('\r')
    Header = [f[0].split(','), f[1].split(',')]
    dataBlock = []

    assert blocknum in range(7), 'Blocknum is out of range'
    #there are 7 blocks, one for each day of the week.  I am using
    #standard convention of labeling them 0-6

    for i in range(3+blocknum*22,24+blocknum*22):
        dataBlock.append(f[i].split(','))
    
#    df_out = pd.DataFrame(dataBlock)
#    return df_out
    return dataBlock
    
    
def generateKey(fname, start_timestamp, channel):
    #prime = math.factorial(52)/math.factorial(13)**4 + 1
    prime = 1011313133831810181383313131101
    h = MD5.new()
    data = fname + str(start_timestamp) + "channel " + str(channel)
    h.update(data)
    return int(int(h.hexdigest(), 16) / prime)

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
            prkey = generateKey(filenames[i-2], ts1, 1)
            chan1.append((prkey, filenames[i-2], datenum, 1, DF[start_idx[0]][i], DF[start_idx[0]+1][i], ts1, ts2))
        
        if DF[6][i]:
            ts1 = (datenum+float(DF[start_idx[1]][i].split(':')[0])+float(DF[start_idx[1]][i].split(':')[1])/60.+float(DF[start_idx[1]][i].split(':')[2])/3600.)/24.
            ts2 = (datenum+float(DF[start_idx[1]+1][i].split(':')[0])+float(DF[start_idx[1]+1][i].split(':')[1])/60.+float(DF[start_idx[1]+1][i].split(':')[2])/3600.)/24.
            prkey = generateKey(filenames[i-2], ts1, 2)
            chan2.append((prkey, filenames[i-2], datenum, 2, DF[start_idx[1]][i], DF[start_idx[1]+1][i], ts1, ts2))
            
        if DF[11][i]:
            ts1 = (datenum+float(DF[start_idx[2]][i].split(':')[0])+float(DF[start_idx[2]][i].split(':')[1])/60.+float(DF[start_idx[2]][i].split(':')[2])/3600.)/24.
            ts2 = (datenum+float(DF[start_idx[2]+1][i].split(':')[0])+float(DF[start_idx[2]+1][i].split(':')[1])/60.+float(DF[start_idx[2]+1][i].split(':')[2])/3600.)/24.
            prkey = generateKey(filenames[i-2], ts1, 3)
            chan3.append((prkey, filenames[i-2], datenum, 3, DF[start_idx[2]][i], DF[start_idx[2]+1][i], ts1, ts2))
            
        if DF[16][i]:
            ts1 = (datenum+float(DF[start_idx[3]][i].split(':')[0])+float(DF[start_idx[3]][i].split(':')[1])/60.+float(DF[start_idx[3]][i].split(':')[2])/3600.)/24.
            ts2 = (datenum+float(DF[start_idx[3]+1][i].split(':')[0])+float(DF[start_idx[3]+1][i].split(':')[1])/60.+float(DF[start_idx[3]+1][i].split(':')[2])/3600.)/24.
            prkey = generateKey(filenames[i-2], ts1, 4)
            chan4.append((prkey, filenames[i-2], datenum, 4, DF[start_idx[3]][i], DF[start_idx[3]+1][i], ts1, ts2))
    
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
 
    for j in range(np.shape(df)[1]):
        sql = "INSERT INTO nicolet_event_log VALUES ({}, '{}', {}, {}, '{}', '{}', {}, {});".format(*(df[0][j][i] for i in range(8)))

        try:
            handle.execute(sql)
        except:
            print "INSERT statement failed!\n"
            print sql


    handle.execute("COMMIT;")

    
    db.close()
