from flask import Flask, Response, request, render_template
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import io
import base64

app = Flask('MeterStats')

def readStats():
    meterStats = pd.read_csv("output.csv")
    meterStats['time'] = pd.to_datetime(meterStats['time'], unit='s')
    meterStats['time'] = meterStats['time']+pd.DateOffset(hours=1)
    return meterStats

@app.route('/')
def index():
    meterStats = readStats()
    #convert unix timestamp to datetime object
    meterStats = meterStats.tail(1)
    
    return render_template("index.html",
        powerLow = str(meterStats.T1.values[0]),
        powerHigh=str(meterStats.T2.values[0]),
        gas=str(meterStats.gas.values[0]))

@app.route('/figure/power/<int:myHours>.png')
def plotPowerFigure(myHours):
    meterStats = readStats()
    oneDayAgo = pd.datetime.now()-pd.DateOffset(hours=myHours)
    mySubSet = meterStats[meterStats['time'] >= oneDayAgo]
   
    if (mySubSet.time.count() > 2):
        fig = Figure()
        mySubSet.plot.line(x='time', y='power')
        
        pngOutputBytes = io.BytesIO()
        plt.savefig(pngOutputBytes, format="png")
        pngOutputBytes.seek(0)
        return Response(pngOutputBytes.read(), mimetype='image/png')

app.run(debug=True, host='0.0.0.0', port=5000)
