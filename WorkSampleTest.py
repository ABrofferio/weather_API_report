#!/usr/bin/python
__author__  = 'Aja Brofferio'

import forecastio
import datetime
import webbrowser
import HTML
import os.path

apikey = [api key] #enter user issued apikey from Forecast.io

#latitude and longitude for the Portland International Airport
lat = 45.5898
long = -122.5951

#var day is initially set to 1464764400 the unix timestamp for for June 1, 2016 @12am from http://www.unixtimestampconverter.com/
day = 1464764400

def dateIterate():
    #definining table_data variable as global so it can be used to generate/populate html table below the dateIterate() function
    global table_data 
    table_data = []

    #the below global variables represent the total number of days that the air or heat was used at least once
    global Air_total
    global Heat_total

    Air_total = 0
    Heat_total = 0

    #range starts at unix timestamp for for June 1, stops at unix timestamp for June 30 and steps by 86400 seconds to represent the difference of a day in unix timestamp
    for day in range (1464764400, 1467356340, 86400):

        #the entry variable will hold the data (defined below) for each day
        entry = []
        
        #converting time from unix using method from datetime module, in order to comply with the methods from the forecastio module
        timeframe = datetime.datetime.fromtimestamp(day)
        
        #method from forecastio Python API wrapper to pull data from API
        forecast = forecastio.load_forecast(apikey, lat, long, time=timeframe)
        
        date = timeframe.strftime('%Y-%m-%d')
        print('Date:', date)
        entry.append(date)

        #method from forecastio Python API wrapper to pull hourly data
        byHour = forecast.hourly()
        
        #variables ac and h will represent the number of times the temp is high enough or low enough to trigger the HVAC system
        ac = 0
        h = 0
        for hourlyData in byHour.data:
            if hourlyData.temperature >75.00:
                ac += 1
            if hourlyData.temperature < 62.00:
                h += 1
        print('air:', ac, 'heat:', h)
        entry.append(ac)
        entry.append(h)

        #variables AC and H will represent whether or not the air conditioning or heating has been turned on at least once that day
        if ac > 0:
            AC = "True"
            Air_total += 1
        else:
            AC = "False"
        if h > 0:
            H = "True"
            Heat_total += 1
        else:
            H = "False"
        print('air used:', AC, 'heat used:', H)
        entry.append(AC)
        entry.append(H)

        #the daily data from the entry variable is aggregated into the table_data variable for the entire month of June which will be output in a web report below
        table_data.append(entry)
    print("Air Total:", Air_total, "Heat:", Heat_total)

dateIterate()

#create and write to html file so the table_data can be viewed in a web report
filename = 'HVACsystem.html'
webreport = open(filename, 'w')

#method from the imported HTML module that allows the table_data to be output into an html table
tablecode = HTML.table(table_data,
        header_row = ['Date', 'Air Usage (hrs)', 'Heat Usage (hrs)', 'Air Used', 'Heat Used'])

htmlcode = """<html>
    <head>
    <title>
    June HVAC Report
    </title>
    </head>
    <body>
    <h1 style = "text-align: center" >June HVAC Summary Report</h1>
    <p>The below table shows the days during the month of June, in which the air conditioning and heating were used at least once. Additionally, the table summarizes the number of hours per day that the temperature would have triggered the air conditioning and heating systems to be employed.</p> 
    {}
    <p>During the month of June there were {} days in which the air conditioning was used at least once and {} days in which the heating was used at least once.</p>
    </body>
    </html>""".format(tablecode, Air_total, Heat_total)

webreport.write(htmlcode)
webreport.close()

webbrowser.open_new_tab("file:///" + os.path.abspath(filename))
