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
        if i <= len(f):
            dataBlock.append(f[i].split(','))
        else:
            pass            
    
#    df_out = pd.DataFrame(dataBlock)
#    return df_out
    return dataBlock
    
    
def generateKey(fname, start_timestamp, channel):
    #prime = math.factorial(52)/math.factorial(13)**4 + 1
    #prime = 1011313133831810181383313131101
    h = MD5.new()
    data = fname + str(start_timestamp) + "channel " + str(channel)
    h.update(data)
    return h.hexdigest()

def getSeizuresFromBlock(DF):
    #Getting date and filenames for the block

    [month, day, year] = DF[0][0].split('/')
    year = '20' + year
    datenum = datetime.date.toordinal(datetime.date(int(year), int(month), int(day)))
    #datenum = int(DF[0][0][2:-3])

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
    
    noDataStr = 'data'
    for i in range(2,np.shape(DF)[1]):
        if DF[1][i] and DF[1][i].find(noDataStr) == -1:
            #Convert decimal created by csv conversion to 'hh:mm:ss'
            #start_time = convertTime(DF[start_idx[0]][i])
            #stop_time = convertTime(DF[start_idx[0]+1][i])
            start_time = DF[start_idx[0]][i]
            stop_time = DF[start_idx[0]+1][i]
            ts1 = (datenum+float(start_time.split(':')[0])+float(start_time.split(':')[1])/60.+float(start_time.split(':')[2])/3600.)/24.
            ts2 = (datenum+float(stop_time.split(':')[0])+float(stop_time.split(':')[1])/60.+float(stop_time.split(':')[2])/3600.)/24.
            ID = generateKey(filenames[i-2], ts1, 1)
            #Removing primary key and opting instead for auto-incrementing key.
            #May return to this idea, but with a hash to use as some kind of event ID.
            chan1.append((ID, filenames[i-2], datenum, 1, DF[start_idx[0]][i], DF[start_idx[0]+1][i], ts1, ts2))
        
        if DF[6][i] and DF[6][i].find(noDataStr) == -1:
            #start_time = convertTime(DF[start_idx[1]][i])
            #stop_time = convertTime(DF[start_idx[1]+1][i])
            start_time = DF[start_idx[1]][i]
            stop_time = DF[start_idx[1]+1][i]
            ts1 = (datenum+float(start_time.split(':')[0])+float(start_time.split(':')[1])/60.+float(start_time.split(':')[2])/3600.)/24.
            ts2 = (datenum+float(stop_time.split(':')[0])+float(stop_time.split(':')[1])/60.+float(stop_time.split(':')[2])/3600.)/24.
            ID = generateKey(filenames[i-2], ts1, 2)
            chan2.append((ID, filenames[i-2], datenum, 2, DF[start_idx[1]][i], DF[start_idx[1]+1][i], ts1, ts2))
            
        if DF[11][i] and DF[11][i].find(noDataStr) == -1:
            #start_time = convertTime(DF[start_idx[2]][i])
            #stop_time = convertTime(DF[start_idx[2]+1][i])
            start_time = DF[start_idx[2]][i]
            stop_time = DF[start_idx[2]+1][i]
            ts1 = (datenum+float(start_time.split(':')[0])+float(start_time.split(':')[1])/60.+float(start_time.split(':')[2])/3600.)/24.
            ts2 = (datenum+float(stop_time.split(':')[0])+float(stop_time.split(':')[1])/60.+float(stop_time.split(':')[2])/3600.)/24.
            ID = generateKey(filenames[i-2], ts1, 3)
            chan3.append((ID, filenames[i-2], datenum, 3, DF[start_idx[2]][i], DF[start_idx[2]+1][i], ts1, ts2))
            
        if DF[16][i] and DF[16][i].find(noDataStr) == -1:
            #start_time = convertTime(DF[start_idx[3]][i])
            #stop_time = convertTime(DF[start_idx[3]+1][i])
            start_time = DF[start_idx[3]][i]
            stop_time = DF[start_idx[3]+1][i]
            ts1 = (datenum+float(start_time.split(':')[0])+float(start_time.split(':')[1])/60.+float(start_time.split(':')[2])/3600.)/24.
            ts2 = (datenum+float(stop_time.split(':')[0])+float(stop_time.split(':')[1])/60.+float(stop_time.split(':')[2])/3600.)/24.
            ID = generateKey(filenames[i-2], ts1, 4)
            chan4.append((ID, filenames[i-2], datenum, 4, DF[start_idx[3]][i], DF[start_idx[3]+1][i], ts1, ts2))
    
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


def makeEventTable(Host, Port, Uname, Pwd, DB):
    # db = MySQLdb.connect(host=Host, port=Port, user=Uname, passwd=Pwd, db=DB)
    # handle = db.cursor()
    # sql = "DROP TABLE nicolet_event_log; COMMIT;"
    # handle.execute(sql)
    # db.close()

    db = MySQLdb.connect(host=Host, port=Port, user=Uname, passwd=Pwd, db=DB)
    handle = db.cursor()
    sql = "CREATE TABLE nicolet_event_log (ID VARCHAR(255) NOT NULL, filename VARCHAR(255), datenum INT, channel INT, event_start VARCHAR(40), event_stop VARCHAR(40), event_start_tmstmp FLOAT, event_stop_tmstmp FLOAT, PRIMARY KEY (ID)); COMMIT;"
    handle.execute(sql)
    db.close()

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
    if df:    
        for j in range(np.shape(df)[1]):
            sql = "INSERT INTO nicolet_event_log VALUES ('{}', '{}', {}, {}, '{}', '{}', {}, {});".format(*(df[0][j][i] for i in range(8)))
            print "INSERT statement no: {}\n".format(j)
            print sql, "\n"
        

            # try:
            #     handle.execute(sql)
            # except:
            #     print "INSERT statement failed!\n"
            #     print sql
            handle.execute(sql)


    handle.execute("COMMIT;")
    db.close()


def convertTime(input):
    input = float(input)
    hh = int(24*input)
    mm = int(60*((24*input)%1))
    ss = int(round(60*((60*((24*input)%1))%1)))
    return "{}:{}:{}".format(hh, mm, ss)