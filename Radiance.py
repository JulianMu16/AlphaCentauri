import requests
import json
import sqlite3
import matplotlib.pyplot as plt
import sys

# PROJECT: How does solar radiation affect temperature anomalies/global warming?
# Pull from Solar Radiation Database and NOAA website to get data and plot it

# API: National Solar Radiation Database
# API KEY: 5PVQvuLyG48QD6P8MvkWGUUDfJXyyPcOAVaQCIu1
# Location #1: Lat: 40 Lon: -110
# Location #2: Lat: 40 Lon: -100
# Location #3: Lat: 40 Lon: -90
# Location #4: Lat 40: Lon -80

def api_request(url, file_num):
    response = requests.get(url)
    data = response
    response.close()
    json_obj = data.json()
    with open("radiationData" + str(file_num) + ".json", 'w') as of:
        json.dump(json_obj, of)
    of.close()
    

def plot():
    # Take from table and make a matlab plot with all 200 data points
    return
    

def main():
    # Get data from lat 40 and longitutdes -80 through -110 by steps of 10
    #for x in range(4):
    #    num = -110
    #    calc = num + (x * 10)
    #    URL = "https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key=5PVQvuLyG48QD6P8MvkWGUUDfJXyyPcOAVaQCIu1&lat=40&lon=" + str(calc)
    #    api_request(URL, calc)

    # Insert 25 items each run based on constraint.txt file
    of = open("constraint.txt", 'r')
    constraint_str = of.readline()
    of.close()
    constraint_num = int(constraint_str)
    if (constraint_num % 9 != 0):
        constraint_num += 1
        of = open("constraint.txt", 'w')
        of.writelines(str(constraint_num))
        of.close
    else:
        print("hi")
        


main()