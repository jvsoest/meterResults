import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

meterStats = pd.read_csv("output.csv")
#convert unix timestamp to datetime object
meterStats['time'] = pd.to_datetime(meterStats['time'], unit='s')

def plotPowerLast(hours=24):
    oneDayAgo = pd.datetime.now()-pd.DateOffset(hours=hours)
    mySubSet = meterStats[meterStats['time'] >= oneDayAgo]
   
    if (mySubSet.time.count() > 2):
        mySubSet.plot.line(x='time', y='power')
        plt.savefig('output_%s.png' % hours)

plotPowerLast(1)
