import serial
import time
import sys
import os.path

fileName = "output.csv"
logFile = "logging.log"

#Set COM port config
ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyUSB0"

def getMeterResults():
    timePoint = int(time.time())
    stack = [ ]

    #Open COM port
    try:
        ser.open()
    except:
        with open(logFile, "a") as myfile:
            myfile.write("Fout bij het openen van verbinding."  % timePoint)

    try:
        for x in range(26):
            stack.append(ser.readline())
    except:
        with open(logFile, "a") as myfile:
            myfile.write("%s - Seriele poort kan niet gelezen worden." % timePoint)

    try:
        ser.close()
    except:
        with open(logFile, "a") as myfile:
            myfile.write("%s - Could not close connection" % timePoint)
                
    tarief = 0
    vermogenAfgenomen = 0
    T1afgenomen = 0
    T2afgenomen = 0
    gasAfgenomen = ""

    for row in stack:
        row = row.decode("UTF-8")
        if row[0:9] == "1-0:1.8.1":
            T1afgenomen = int(row[10:16])
        if row[0:9] == "1-0:1.8.2":
            T2afgenomen = int(row[10:16])
        if row[0:9] == "1-0:2.8.1":
            T1terug = int(row[10:16])
        if row[0:9] == "1-0:2.8.2":
            T2terug = int(row[10:16])
        if row[0:9] == "1-0:1.7.0":
            vermogenAfgenomen = int(float(row[10:16])*1000) #watts
        if row[0:10] == "1-0:32.7.0":
            voltage = float(row[11:16])
        if row[0:10] == "1-0:31.7.0":
            ampere = float(row[11:14])
        if row[0:9] == "1-0:2.7.0":
            vermogenTerug = int(float(row[10:16])*1000) #watts
        if row[0:9] == "0-0:96.14":
            tarief = int(row[12:16]) #1=hoog, 2=laag
        if row[0:10] == "0-1:24.2.1":
            gasAfgenomen = float(row[26:35]) #m3

    return {"timeStamp": timePoint,
            "tariff": tarief,
            "power": vermogenAfgenomen,
            "current": voltage,
            "flow": ampere,
            "T1": T1afgenomen,
            "T2": T2afgenomen,
            "gas": gasAfgenomen}

# Create file if not exists
if not os.path.exists(fileName):
    with open(fileName, "w") as myfile:
        myfile.write("time,tariff,power,current,flow,T1,T2,gas\n")

# Enter main loop
while 1==1:
    meterStats = getMeterResults()
    outputString = "%s,%s,%s,%s,%s,%s,%s,%s\n" % (meterStats["timeStamp"],meterStats["tariff"],meterStats["power"],meterStats["current"],meterStats["flow"],meterStats["T1"],meterStats["T2"],meterStats["gas"])
    with open("output.csv", "a") as myfile:
        myfile.write(outputString)

    time.sleep(5)

