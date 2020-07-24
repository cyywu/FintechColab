# MAJOR FOREIGN HOLDERS OF TREASURY SECURITIES

fixed_plot_width = True # set it to False and click Runtime > Run all if you prefer a responsive width
plot_width = 600 # customise plot_width and click Runtime > Run all if you prefer a plot_width other than 600px


import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import urllib.request
import json
import requests
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ssl
import numpy as np
import re
context = ssl._create_unverified_context()

# ---------------------------------------------------------------
url = "https://ticdata.treasury.gov/Publish/mfhhis01.txt"
csv = pd.read_csv("https://ticdata.treasury.gov/Publish/mfhhis01.txt", sep="\t", names=["data"])
df = pd.DataFrame(csv)

startPoints = df["data"].str.startswith("Country").tolist()
endPoints = df["data"].str.startswith("Grand Total").tolist() 

startAts = []
endBefores = []
colsOfYears = []
years = []

for i in range(len(startPoints)):
  if(startPoints[i]):
    startAts += [i+2]
    colsOfThisYear = str(df['data'][i-1]).strip().split(" ")
    toDelete = []
    for k in range(len(colsOfThisYear)):
        if(colsOfThisYear[k] == ''):
            toDelete = [k] + toDelete
    for key in toDelete:
        colsOfThisYear.pop(key)
    colsOfYears += [colsOfThisYear]


    years += [str(df['data'][i][-4:])]
  if(endPoints[i]):
    endBefores += [i]

print('-------')


# trying
for i_table in range(len(startAts)):
  # get the table of the year
  table = df.iloc[startAts[i_table]:endBefores[i_table]]

  # make it a data frame, not sure if it is needed
  df_table = pd.DataFrame(table)
  
  countryNames = []
  datas = []
  # for each row of this table
  for i_row in range(endBefores[i_table] - startAts[i_table]):
    # split it from a string to a list of data, and remove n.a.
    # from 
    #     "Japan                     378.1   374.9   373.1   373.8 ..."
    #     "Luxembourg          23.9  23.7  23.3 ... n.a. n.a. n.a. n.a. n.a."
    # to 
    #     ['Japan', ' ' , ' ' , ' ', '378.1', '374.9', ...]
    #     ['Luxembourg', ' ' , ' ' , ' ', ' 23.9', '23.7', ... , '0', '0', '0', '0', '0', '0']
    r = re.compile("(n.a.)")
    dataRow = df_table['data'][i_row + startAts[i_table]]
    removeNA = r.sub("  0", dataRow)
    r = re.compile("(  )")
    subDataRow = r.sub("\t", removeNA)
    splitDataRow = subDataRow.split("\t")

    # remove empty element
    # from 
    #     ['Japan', ' ' , ' ' , ' ', '378.1', '374.9', ...]
    # to 
    #     ['Japan', '378.1', '374.9', ...]
    toDelete = []
    for key in range(len(splitDataRow)):
        if(splitDataRow[key] == ''):
            toDelete = [key] + toDelete
    for key in toDelete:
        splitDataRow.pop(key)

    print(splitDataRow)    
    
    # deal with special case
    # from 
    #     ['Belgium', '5/', '13.0', '13.2', ... ]
    # to 
    #     ['Belgium 5/', '13.0', '13.2', ... ]
    countryName = splitDataRow[:-len(colsOfYears[i_table])]
    if(len(countryName)>1):
      splitDataRow[0] = ' '.join(splitDataRow[0:len(countryName)])
      splitDataRow = [splitDataRow[0]] + splitDataRow[len(countryName):]
    countryName = splitDataRow[0]
    data = splitDataRow[-len(colsOfYears[i_table]):]

    countryNames.append(countryName)
    datas.append(data)
   
  # for year that have duplicated month, says, 2002 - 2004
  # record only one of them
  # from
  #     [ ..., 'Jul', 'Jun', 'Jun', 'May', ...]
  #     [ ..., ' 675.4', ' 666.6', ' 688.4', ' 666.4', ... ]
  # to
  #     [ ... , 'Jul', 'Jun', 'May', ...]
  #     [ ..., ' 675.4', ' 666.6', ' 651.8', ...]
  toDelete = []
  for key in range(len(colsOfYears[i_table])):
    if(key>=1):
      if(colsOfYears[i_table][key] == colsOfYears[i_table][key-1]):
        toDelete = [key] + toDelete

  for key in toDelete:
    colsOfYears[i_table].pop(key)
    for i_datasLen in range(len(datas)):
      datas[i_datasLen].pop(key)


  for i in range(len(datas)):
    countryName = countryNames[i]
    dataListOfTheCountry = datas[i]

    # for j in range(len(dataListOfTheCountry)):
      # print([countryName, str(colsOfYears[i_table][j] + " " + years[i_table]), float(dataListOfTheCountry[j])])
  
  print('-------')