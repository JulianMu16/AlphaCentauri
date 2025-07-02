import requests
import json
import sqlite3
import matplotlib.pyplot as plt
import sys
import os

from WebScrape import *
from CalcPlot import *


# PROJECT: How does solar radiation affect temperature anomalies/global warming?
# Pull from Solar Radiation Database and NOAA website to get data and plot it

# API: National Solar Radiation Database
# API KEY: 5PVQvuLyG48QD6P8MvkWGUUDfJXyyPcOAVaQCIu1
# Location #1: Lat: 40 Lon: -110
# Location #2: Lat: 40 Lon: -100
# Location #3: Lat: 40 Lon: -90
# Location #4: Lat 40: Lon -80

def api_request(url, cur_dict, dict_list):
    response = requests.get(url)
    data = response
    response.close()
    cur_dict = data.json()
    dict_list.append(cur_dict)
    

# Insert radiation data into ghi/dni tables
def radiation_insert(cur, conn, curr_dict):
    lon = curr_dict["inputs"]["lon"]
    dni_annual = curr_dict["outputs"]["avg_dni"]["annual"]
    
    # Insert annual values
    if (int(lon) == -80):
        cur.execute("INSERT OR IGNORE INTO dni80 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, "2012", dni_annual))
        for keys in curr_dict["outputs"]["avg_dni"]["monthly"]:
            radiance = curr_dict["outputs"]["avg_dni"]["monthly"][keys]
            cur.execute("INSERT OR IGNORE INTO dni80 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, keys, radiance))
        for keys in curr_dict["outputs"]["avg_ghi"]["monthly"]:
            radiance = curr_dict["outputs"]["avg_ghi"]["monthly"][keys]
            cur.execute("INSERT OR IGNORE INTO ghi80 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, keys, radiance))
            conn.commit()
    elif (int(lon) == -90):
        cur.execute("INSERT OR IGNORE INTO dni90 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, "2012", dni_annual))
        for keys in curr_dict["outputs"]["avg_dni"]["monthly"]:
            radiance = curr_dict["outputs"]["avg_dni"]["monthly"][keys]
            cur.execute("INSERT OR IGNORE INTO dni90 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, keys, radiance))
        for keys in curr_dict["outputs"]["avg_ghi"]["monthly"]:
            radiance = curr_dict["outputs"]["avg_ghi"]["monthly"][keys]
            cur.execute("INSERT OR IGNORE INTO ghi90 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, keys, radiance))
            conn.commit()
    elif (int(lon) == -100):
        cur.execute("INSERT OR IGNORE INTO dni100 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, "2012", dni_annual))
        for keys in curr_dict["outputs"]["avg_dni"]["monthly"]:
            radiance = curr_dict["outputs"]["avg_dni"]["monthly"][keys]
            cur.execute("INSERT OR IGNORE INTO dni100 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, keys, radiance))
        for keys in curr_dict["outputs"]["avg_ghi"]["monthly"]:
            radiance = curr_dict["outputs"]["avg_ghi"]["monthly"][keys]
            cur.execute("INSERT OR IGNORE INTO ghi100 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, keys, radiance))
            conn.commit()
    elif (int(lon) == -110):
        cur.execute("INSERT OR IGNORE INTO dni110 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, "2012", dni_annual))
        for keys in curr_dict["outputs"]["avg_dni"]["monthly"]:
            radiance = curr_dict["outputs"]["avg_dni"]["monthly"][keys]
            cur.execute("INSERT OR IGNORE INTO dni110 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, keys, radiance))
        for keys in curr_dict["outputs"]["avg_ghi"]["monthly"]:
            radiance = curr_dict["outputs"]["avg_ghi"]["monthly"][keys]
            cur.execute("INSERT OR IGNORE INTO ghi110 (longitude, date, radiation) VALUES (?, ?, ?)", (lon, keys, radiance))
            conn.commit()
    return


# Insert anomaly data into a table
def anomaly_insert(cur, conn, lon, tup_list):
    if (lon == -80):
        for tup in tup_list:
            date = tup[0]
            anomaly = tup[1]
            cur.execute("INSERT OR IGNORE INTO anomaly80 (longitude, date, anomalyTemp) VALUES (?, ?, ?)", (lon, date, anomaly))
    if (lon == -90):
        for tup in tup_list:
            date = tup[0]
            anomaly = tup[1]
            cur.execute("INSERT OR IGNORE INTO anomaly90 (longitude, date, anomalyTemp) VALUES (?, ?, ?)", (lon, date, anomaly))
    if (lon == -100):
        for tup in tup_list:
            date = tup[0]
            anomaly = tup[1]
            cur.execute("INSERT OR IGNORE INTO anomaly100 (longitude, date, anomalyTemp) VALUES (?, ?, ?)", (lon, date, anomaly))
    if (lon == -110):
        for tup in tup_list:
            date = tup[0]
            anomaly = tup[1]
            cur.execute("INSERT OR IGNORE INTO anomaly110 (longitude, date, anomalyTemp) VALUES (?, ?, ?)", (lon, date, anomaly))
    conn.commit()
    return
    
    
def main():
    # Initialize dictionaries and put them in a list
    dict_list = []
    radiation_dict_list = []

    lon80dict = {}
    lon90dict = {}
    lon100dict = {}
    lon110dict = {}
    anom80 = []
    anom90 = []
    anom100 = []
    anom110 = []

    dict_list.append(lon110dict)
    dict_list.append(lon100dict)
    dict_list.append(lon90dict)
    dict_list.append(lon80dict)

    # Get data from lat 40 and longitutdes -80 through -110 by steps of 10
    for x in range(4):
         num = -110
         calc = num + (x * 10)
         URL = "https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key=5PVQvuLyG48QD6P8MvkWGUUDfJXyyPcOAVaQCIu1&lat=40&lon=" + str(calc)
         curr_dict = dict_list[x]
         api_request(URL, curr_dict, radiation_dict_list)

    # Open database
    path = os.path.join(os.path.dirname(__file__))
    conn = sqlite3.connect(path + '/' + "Radiation.db")
    cur = conn.cursor()

    # Insert 25 items each run based on constraint.txt file
    of = open("constraint.txt", 'r')
    constraint_str = of.readline()
    of.close()
    constraint_num = int(constraint_str)
    if (constraint_num % 9 != 0):
        if (constraint_num % 9 == 1):
            # Create average DNI table (Direct Normal Irradiance)
            cur.execute("CREATE TABLE IF NOT EXISTS dni80 (longitude INTEGER KEY, date TEXT, radiation NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS dni90 (longitude INTEGER KEY, date TEXT, radiation NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS dni100 (longitude INTEGER KEY, date TEXT, radiation NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS dni110 (longitude INTEGER KEY, date TEXT, radiation NUMERIC)")

            # Create average GHI table (Global Horizontal Irradiance)
            cur.execute("CREATE TABLE IF NOT EXISTS ghi80 (longitude INTEGER KEY, date TEXT, radiation NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS ghi90 (longitude INTEGER KEY, date TEXT, radiation NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS ghi100 (longitude INTEGER KEY, date TEXT, radiation NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS ghi110 (longitude INTEGER KEY, date TEXT, radiation NUMERIC)")

            # Create temperature anomaly table
            cur.execute("CREATE TABLE IF NOT EXISTS anomaly80 (longitude INTEGER KEY, date TEXT, anomalyTemp NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS anomaly90 (longitude INTEGER KEY, date TEXT, anomalyTemp NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS anomaly100 (longitude INTEGER KEY, date TEXT, anomalyTemp NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS anomaly110 (longitude INTEGER KEY, date TEXT, anomalyTemp NUMERIC)")
            conn.commit()

            radiation_insert(cur, conn, radiation_dict_list[0])
        elif (constraint_num % 9 == 2):
            radiation_insert(cur, conn, radiation_dict_list[1])
        elif (constraint_num % 9 == 3):
            radiation_insert(cur, conn, radiation_dict_list[2])
        elif (constraint_num % 9 == 4):
            radiation_insert(cur, conn, radiation_dict_list[3])
        elif (constraint_num % 9 == 5):
            anom80 = DataPull(str(-80))
            anomaly_insert(cur, conn, -80, anom80)
        elif (constraint_num % 9 == 6):
            anom90 = DataPull(str(-90))
            anomaly_insert(cur, conn, -90, anom90)
        elif (constraint_num % 9 == 7):
            anom100 = DataPull(str(-100))
            anomaly_insert(cur, conn, -100, anom100)
        elif (constraint_num % 9 == 8):
            anom110 = DataPull(str(-110))
            anomaly_insert(cur, conn, -110, anom110)

        # Increment constraint
        constraint_num += 1
        of = open("constraint.txt", 'w')
        of.writelines(str(constraint_num))
        of.close
        return
    else:
        # Call from CalcPlot to calculate and plot data
        calc_avg_anomaly_per_annual_rad(cur)


        # Increment constraint to continue cycle
        constraint_num += 1
        of = open("constraint.txt", 'w')
        of.writelines(str(constraint_num))
        of.close
        return
        
main()
