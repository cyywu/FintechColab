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
def trendOTCFCbyInstrument():
  url = "https://www.bis.org/statistics/rpfx19_fx_tables.xlsx"
  r = requests.get(url) 
  workbook = xlrd.open_workbook(file_contents=r.content)
  worksheet = workbook.sheet_by_name('Txt_01')

  startAt = 6
  endBefore = 11
  endOfMons = list(map(lambda x: x.value, worksheet.row(3)[2:][1:]))

  otcFxbyInstr = pd.DataFrame(endOfMons)
  otcFxbyInstr.columns = ['date']
  otcFxbyInstr_dfs = {}
  for i in range(startAt-1, endBefore-1):
    curInstr = worksheet.row(i)[2:]
    curInstrName = curInstr[0].value
    curInstrValue = [[endOfMons[index], x.value * 1000000000] for index, x in enumerate(curInstr[1:])]
    curDf = pd.DataFrame(curInstrValue)
    curDf.columns = ['date', curInstrName]
    otcFxbyInstr = otcFxbyInstr.merge(curDf, how='outer').fillna(method='ffill')

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
      title_text="<b>Trend of OTC FX by Instrument (stacked)</b>",
      xaxis_title='End of period <b>(Monthly)</b>',
      yaxis_title='<b>USD</b> US Dollars',
      height=700,
      showlegend=True,
  )
  if fixed_plot_width:
    fig.update_layout(width=plot_width)
  fig.show()

trendOTCFCbyInstrument()