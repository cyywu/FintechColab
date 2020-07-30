fixed_plot_width = True # set it to False and click Runtime > Run all if you prefer a responsive width
plot_width = 800 # customise plot_width and click Runtime > Run all if you prefer a plot_width other than 600px

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

import xlrd
# ---------------- Trend of OTC FX by Instrument ----------------
def trendOTCFXbyInstrument():
  url = "https://www.bis.org/statistics/rpfx19_fx_tables.xlsx"
  r = requests.get(url) 
  workbook = xlrd.open_workbook(file_contents=r.content)
  worksheet = workbook.sheet_by_name('Txt_01')

  startAt = 6
  endBefore = 11
  endOfMons = []
  for x in worksheet.row(3)[3:]:
    if not (x.value == ''):
      endOfMons.append(str(int(x.value)))

  otcFxbyInstr = pd.DataFrame(endOfMons)
  otcFxbyInstr.columns = ['date']
  
  for i in range(startAt-1, endBefore-1):
    thisInstr = worksheet.row(i)[2:]
    thisInstrName = thisInstr[0].value
    thisInstrValue = [[endOfMons[index], x.value * 1000000000] for index, x in enumerate(thisInstr[1:])]
    thisDf = pd.DataFrame(thisInstrValue)
    thisDf.columns = ['date', thisInstrName]
    otcFxbyInstr = otcFxbyInstr.merge(thisDf, how='outer').fillna(method='ffill')

  otcFxbyInstr.date = pd.to_datetime(otcFxbyInstr.date)
  dfColumns = list(otcFxbyInstr) 
  for col in dfColumns: 
    if not col == 'date':
      otcFxbyInstr[col] = pd.to_numeric(otcFxbyInstr[col])

  # plot stacked chart
  fig = go.Figure()
  fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=3, label="3y", step="year", stepmode="backward"),
            dict(count=6, label="6y", step="year", stepmode="backward"),
            dict(count=10, label="10y", step="year", stepmode="backward"),
            dict(count=15, label="15y", step="year", stepmode="backward"),
            dict(step="all")
        ])
      )
  )
  for col in dfColumns: 
    if not col == 'date':
      fig.add_trace(go.Scatter(x=otcFxbyInstr.date, y=otcFxbyInstr[col], mode='lines', line=dict(width=0.5), stackgroup='otcFxbyInstr', name=col))

  fig.update_layout(
      title_text="<b>Trend of Over-the-counter FX by Instrument (stacked)</b>",
      xaxis_title='End of period <b>(Monthly)</b>',
      yaxis_title='<b>USD</b> US Dollars',
      height=600,
      showlegend=True,
      legend=dict(
          yanchor="top",
          y=0.99,
          xanchor="left",
          x=0.01
      )
  )
  if fixed_plot_width:
    fig.update_layout(width=plot_width)
  fig.show()

# ---------------- Trend of OTC FX by Currency Distribution ----------------
def trendOTCFXbyCurDis():
  url = "https://www.bis.org/statistics/rpfx19_fx_tables.xlsx"
  r = requests.get(url) 
  workbook = xlrd.open_workbook(file_contents=r.content)
  worksheet = workbook.sheet_by_name('Txt_02')

  startAt = 6
  endBefore = 42
  endOfMons = []
  for x in worksheet.row(3)[3:]:
    if not (x.value == ''):
      endOfMons.append(str(int(x.value)))

  otcFxbyCurDis = pd.DataFrame(endOfMons)
  otcFxbyCurDis.columns = ['date']

  for i in range(startAt-1, endBefore-1):
    thisCur = worksheet.row(i)[2:]
    
    thisCurName = thisCur[0].value

    thisCurValue = []
    for j, x in enumerate(thisCur[1:]):
      if (j % 2) == 0:
        thisCurValue.append(x.value)
    
    for j, x in enumerate(thisCurValue):
      thisCurValue[j] = [endOfMons[j], thisCurValue[j]]
    
    thisDf = pd.DataFrame(thisCurValue)
    thisDf.columns = ['date', thisCurName]
    otcFxbyCurDis = otcFxbyCurDis.merge(thisDf, how='outer').fillna(method='ffill')

  otcFxbyCurDis.date = pd.to_datetime(otcFxbyCurDis.date)
  dfColumns = list(otcFxbyCurDis) 
  for col in dfColumns: 
    if not col == 'date':
      otcFxbyCurDis[col] = pd.to_numeric(otcFxbyCurDis[col])

  # plot stacked chart
  fig = go.Figure()
  fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=3, label="3y", step="year", stepmode="backward"),
            dict(count=6, label="6y", step="year", stepmode="backward"),
            dict(count=10, label="10y", step="year", stepmode="backward"),
            dict(count=15, label="15y", step="year", stepmode="backward"),
            dict(step="all")
        ])
      )
  )
  for col in dfColumns: 
    if not col == 'date':
      fig.add_trace(go.Scatter(x=otcFxbyCurDis.date, y=otcFxbyCurDis[col], mode='lines', line=dict(width=0.5), stackgroup='otcFxbyCurDis', name=col, groupnorm='percent'))

  fig.update_layout(
      title_text="<b>Trend of Over-the-counter FX by Currency Distribution (100% stacked)</b>",
      xaxis_title='End of period <b>(Monthly)</b>',
      yaxis_title='<b>%</b> Percentage',
      height=700,
      showlegend=True,
      yaxis=dict(
        type='linear',
        range=[1, 100],
        ticksuffix='%'
      ),
  )
  if fixed_plot_width:
    fig.update_layout(width=plot_width)
  fig.show()

# ---------------- Trend of OTC FX by Currency Pair ----------------
def trandOTCFXbyCurPair():
  url = "https://www.bis.org/statistics/rpfx19_fx_tables.xlsx"
  r = requests.get(url) 
  workbook = xlrd.open_workbook(file_contents=r.content)
  worksheet = workbook.sheet_by_name('Txt_03')

  startAt = 6
  endBefore = 49
  endOfMons = []
  for x in worksheet.row(3)[3:]:
    if not (x.value == ''):
      endOfMons.append(str(int(x.value)))

  otcFxbyCurPair = pd.DataFrame(endOfMons)
  otcFxbyCurPair.columns = ['date']

  for i in range(startAt-1, endBefore-1):
    thisCur = worksheet.row(i)[2:]
    
    thisCurName = thisCur[0].value

    thisCurValue = []
    for j, x in enumerate(thisCur[1:]):
      if (j % 2) == 0:
        thisCurValue.append(x.value * 1000000000)
    
    for j, x in enumerate(thisCurValue):
      thisCurValue[j] = [endOfMons[j], thisCurValue[j]]
    
    thisDf = pd.DataFrame(thisCurValue)
    thisDf.columns = ['date', thisCurName]
    otcFxbyCurPair = otcFxbyCurPair.merge(thisDf, how='outer').fillna(method='ffill')

  otcFxbyCurPair.date = pd.to_datetime(otcFxbyCurPair.date)
  dfColumns = list(otcFxbyCurPair) 
  for col in dfColumns: 
    if not col == 'date':
      otcFxbyCurPair[col] = pd.to_numeric(otcFxbyCurPair[col])


  # plot stacked chart
  fig = go.Figure()
  fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=3, label="3y", step="year", stepmode="backward"),
            dict(count=6, label="6y", step="year", stepmode="backward"),
            dict(count=10, label="10y", step="year", stepmode="backward"),
            dict(count=15, label="15y", step="year", stepmode="backward"),
            dict(step="all")
        ])
      )
  )
  for col in dfColumns: 
    if not col == 'date':
      fig.add_trace(go.Scatter(x=otcFxbyCurPair.date, y=otcFxbyCurPair[col], mode='lines', line=dict(width=0.5), stackgroup='otcFxbyCurPair', name=col))

  fig.update_layout(
      title_text="<b>Trend of Over-the-counter FX by Currency Pair (stacked)</b>",
      xaxis_title='End of period <b>(Monthly)</b>',
      yaxis_title='<b>USD</b> US Dollars',
      height=800,
      showlegend=True,
  )
  if fixed_plot_width:
    fig.update_layout(width=plot_width)
  fig.show()