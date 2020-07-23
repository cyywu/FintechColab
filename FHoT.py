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
# url = "https://ticdata.treasury.gov/Publish/mfhhis01.txt"
# req = requests.get(url).content
# print(req)
# csv = pd.read_csv(io.StringIO(req.decode('utf8')), names =["data"])
# df = pd.DataFrame(csv)

url = "https://ticdata.treasury.gov/Publish/mfhhis01.txt"
csv = pd.read_csv("https://ticdata.treasury.gov/Publish/mfhhis01.txt", sep="\t", names=["data"])
df = pd.DataFrame(csv)

startPoints = df["data"].str.startswith("Country").tolist()
endPoints = df["data"].str.startswith("Grand Total").tolist() 

years = []
startAts = []
endBefores = []

for i in range(len(startPoints)):
  if(startPoints[i]):
    years += [str(df['data'][i][-4:])]
    startAts += [i+2]
  if(endPoints[i]):
    endBefores += [i]

print(years)
print(startAts)
print(endBefores)
print('-------')


# # trying
r = re.compile("(  )")
for i in range(len(startAts)):
  # get the year table
  table = df.iloc[startAts[i]:endBefores[i]]

  # make it a data frame, not sure if it is needed
  df_table = pd.DataFrame(table)

  # for each row, just a long string, research on how to get the data out, like country name, and all 12 number
  for j in range(endBefores[i] - startAts[i]):
    line = df_table['data'][j + startAts[i]]
    subLine = r.sub("\t", line)
    splitLine = subLine.split("\t")

    toDelete = []
    for k in range(len(splitLine)):
        if(splitLine[k] == ''):
            toDelete = [k] + toDelete
    for key in toDelete:
        splitLine.pop(key)
    print(splitLine)
    
  print('-------')


# may make use of df['data'].str.split("\t", expand=True)