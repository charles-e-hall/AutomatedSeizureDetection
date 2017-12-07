#This file contains utility functions for organizing and parsing data from 
#the excel files that contain the human scored events from the Nicolet
#EEG files

import numpy as np
import pandas as pd
import MySQLdb
from datetime import date

def returnDataFrame(filename):
    #filename must be a csv file
    f = open(filename, 'r').read().split('\r')
    
    
    
def insertEvents(df, db, uname, pwd, commit=True):
    cursor = db.connect()
    