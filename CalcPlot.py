import requests
import json
import sqlite3
import matplotlib.pyplot as plt
import sys
import os

# This file does calculations and plots the data


def calc_avg_anomaly_per_annual_rad(cur):
    cur.execute("SELECT dni80.radiation, dni110.radiation FROM dni80 JOIN dni110 ON dni80.date = dni110.date WHERE dni80.date = 2012")
    results = cur.fetchall()
    dni80ann = results[0][0]
    dni110ann = results[0][1]

    cur.execute("SELECT anomaly80.anomalyTemp FROM anomaly80 WHERE anomalyTemp > 0.85 OR anomalyTemp < -0.85")
    results = cur.fetchall()
    considerable80 = results

    cur.execute("SELECT anomaly110.anomalyTemp FROM anomaly110 WHERE anomalyTemp > 0.85 OR anomalyTemp < -0.85")
    results = cur.fetchall()
    considerable110 = results

    avg80temp = 0
    avg110temp = 0

    # Calculate considerable average for lon -80
    for anomalies in considerable80:
        avg80temp += anomalies[0]

    # Calculate considerable average for lon -110
    for anomalies in considerable110:
        avg110temp += anomalies[0]

    avg80temp = avg80temp / len(considerable80)
    avg110temp = avg110temp / len(considerable110)
    avg80temp = round(avg80temp, 3)
    avg110temp = round(avg110temp, 3)

    of = open("AnomalyCalculation.txt", 'w')
    of.writelines("Considerable Anomalies at lattitude 40, longitude -80:\n")
    of.writelines(str(considerable80))
    of.writelines("\n")
    of.writelines("Average DNI at latitude 40, longitude -80:\n")
    of.writelines(str(dni80ann))
    of.writelines("\n")
    of.writelines("Average Considerable Anomaly at latitude 40, longitude -80:\n")
    of.writelines(str(avg80temp))
    of.writelines("\n")
    of.writelines("\n")
    of.writelines("Conisderable Anomalies at latitude 40, longitude -110:\n")
    of.writelines(str(considerable110))
    of.writelines("\n")
    of.writelines("Average DNI at latitude 40, longitude -110:\n")
    of.writelines(str(dni110ann))
    of.writelines("\n")
    of.writelines("Average Considerable Anomaly at latitude 40, longitude -110:\n")
    of.writelines(str(avg110temp))
    of.close
    
    # Left plot
    plt.subplot(1, 2, 1)
    plt.title("Temperature Anomaly VS GHI Radation (lat:40, lon: -80)")
    x = []
    y = []
    cur.execute("SELECT anomaly80.anomalyTemp FROM anomaly80 WHERE date = 'January 2012' OR date = 'February 2012' OR date = 'March 2012' OR date = 'April 2012' OR date = 'May 2012' OR date = 'June 2012' OR date = 'July 2012' OR date = 'August 2012' OR date = 'September 2012' OR date = 'October 2012' OR date = 'November 2012' OR date = 'December 2012'")
    results = cur.fetchall()
    for temps in results:
        y.append(temps[0])

    cur.execute("SELECT ghi80.radiation FROM ghi80 WHERE radiation < 100")
    results = cur.fetchall()
    for ghi in results:
        x.append(ghi[0])

    plt.xlabel("GHI Radiation (W/m^2)")
    plt.ylabel("Temperature Anomaly (C)")
    plt.scatter(x, y, color='r')

    # Right plot
    plt.subplot(1, 2, 2)
    plt.title("Temperature Anomaly VS GHI Radation (lat:40, lon: -110)")
    x = []
    y = []
    cur.execute("SELECT anomaly110.anomalyTemp FROM anomaly110 WHERE date = 'January 2012' OR date = 'February 2012' OR date = 'March 2012' OR date = 'April 2012' OR date = 'May 2012' OR date = 'June 2012' OR date = 'July 2012' OR date = 'August 2012' OR date = 'September 2012' OR date = 'October 2012' OR date = 'November 2012' OR date = 'December 2012'")
    results = cur.fetchall()
    for temps in results:
        y.append(temps[0])

    cur.execute("SELECT ghi110.radiation FROM ghi110 WHERE radiation < 100")
    results = cur.fetchall()
    for ghi in results:
        x.append(ghi[0])

    plt.xlabel("GHI Radiation (W/m^2)")
    plt.ylabel("Temperature Anomaly (C)")
    plt.scatter(x, y, color='b')

    # Show all plots
    plt.show()
    return