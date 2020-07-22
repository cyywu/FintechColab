import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import urllib.request
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ssl
import numpy as np
context = ssl._create_unverified_context()

# COFER
# http://jsonviewer.stack.hu/#http://dataservices.imf.org/REST/SDMX_JSON.svc/DataStructure/COFER
# Dataset information - ['Structure']['KeyFamilies']['KeyFamily']['Annotations']
# Dimension - ['Structure']['KeyFamilies']['KeyFamily']['Components']['Dimension']

# CL_FREQ http://jsonviewer.stack.hu/#http://dataservices.imf.org/REST/SDMX_JSON.svc/CodeList/CL_FREQ
FREQ_A = "A"  # Annual
FREQ_Q = "Q"  # Quarterly

# CL_AREA_COFER http://jsonviewer.stack.hu/#http://dataservices.imf.org/REST/SDMX_JSON.svc/CodeList/CL_AREA_COFER
AREA_W00 = "W00"  # All countries
AREA_XR43 = "XR43"  # Emerging and Developing Countries,
AREA_XR29 = "XR29"  # Advanced Economies

# CL_INDICATOR_COFER http://jsonviewer.stack.hu/#http://dataservices.imf.org/REST/SDMX_JSON.svc/CodeList/CL_INDICATOR_COFER
RAXGFX_USD = "RAXGFX_USD" # Foreign Exchange, US Dollars
RAXGFX_AR_AUD_USD = "RAXGFXARAUD_USD"
RAXGFX_AR_CAD_USD = "RAXGFXARCAD_USD"
RAXGFX_AR_EURO_USD = "RAXGFXAREURO_USD"
RAXGFX_AR_JPY_USD = "RAXGFXARJPY_USD"
RAXGFX_AR_GBP_USD = "RAXGFXARGBP_USD"
RAXGFX_AR_CHF_USD = "RAXGFXARCHF_USD"
RAXGFX_AR_USD_USD = "RAXGFXARUSD_USD"
RAXGFX_AR_OC_USD = "RAXGFXAROC_USD"
RAXGFX_AR_USD = "RAXGFXAR_USD"  # Allocated Reserves, US Dollars
RAXGFX_UR_USD = "RAXGFXUR_USD"  # Unallocated Reserves, US Dollars
RAXGFX_AR_CNY_USD = "RAXGFXARCNY_USD"
RAXGFX_AR_CNY_PT= "RAXGFXARCNYRT_PT"

# ---------------------------------------------------------------
# Customising the API request
COFER_url = "http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/COFER/"
COFER_startPeriod = "1999"
COFER_endPeriod = "2020"
COFER_FREQ = FREQ_Q
COFER_AREA = AREA_W00
COFER_INDICATORS = [RAXGFX_USD,
                    RAXGFX_AR_AUD_USD,
                    RAXGFX_AR_CAD_USD,
                    RAXGFX_AR_EURO_USD,
                    RAXGFX_AR_JPY_USD,
                    RAXGFX_AR_GBP_USD,
                    RAXGFX_AR_CHF_USD,
                    RAXGFX_AR_USD_USD,
                    RAXGFX_AR_OC_USD,
                    RAXGFX_AR_USD,
                    RAXGFX_UR_USD,
                    RAXGFX_AR_CNY_USD,
                    RAXGFX_AR_CNY_PT]

url = COFER_url \
    + COFER_FREQ \
    + "." + COFER_AREA + "." \
    + ('+'.join(COFER_INDICATORS)) + "?" \
    + "startPeriod=" + COFER_startPeriod + "&" \
    + "endPeriod=" + COFER_endPeriod

req = urllib.request.urlopen(url, context=context)

odata = json.loads(req.read().decode())
fx = pd.DataFrame(odata['CompactData']['DataSet']['Series'][0]['Obs'])
fx_ar_AUD = pd.DataFrame(odata['CompactData']['DataSet']['Series'][1]['Obs'])
fx_ar_CAD = pd.DataFrame(odata['CompactData']['DataSet']['Series'][2]['Obs'])
fx_ar_EURO = pd.DataFrame(odata['CompactData']['DataSet']['Series'][3]['Obs'])
fx_ar_JPY = pd.DataFrame(odata['CompactData']['DataSet']['Series'][4]['Obs'])
fx_ar_GBP = pd.DataFrame(odata['CompactData']['DataSet']['Series'][5]['Obs'])
fx_ar_CHF = pd.DataFrame(odata['CompactData']['DataSet']['Series'][6]['Obs'])
fx_ar_USD = pd.DataFrame(odata['CompactData']['DataSet']['Series'][7]['Obs'])
fx_ar_OC = pd.DataFrame(odata['CompactData']['DataSet']['Series'][8]['Obs'])
fx_ar = pd.DataFrame(odata['CompactData']['DataSet']['Series'][9]['Obs'])
fx_ur = pd.DataFrame(odata['CompactData']['DataSet']['Series'][10]['Obs'])
fx_ar_CNY = pd.DataFrame(odata['CompactData']['DataSet']['Series'][11]['Obs'])
fx_ar_CNY_pt = pd.DataFrame(odata['CompactData']['DataSet']['Series'][12]['Obs'])

fx.columns = ['date','fx']
fx_ar_AUD.columns = ['date','fx_ar_AUD']
fx_ar_CAD.columns = ['date','fx_ar_CAD']
fx_ar_EURO.columns = ['date','fx_ar_EURO']
fx_ar_JPY.columns = ['date','fx_ar_JPY']
fx_ar_GBP.columns = ['date','fx_ar_GBP']
fx_ar_CHF.columns = ['date','fx_ar_CHF']
fx_ar_USD.columns = ['date','fx_ar_USD']
fx_ar_OC.columns = ['date','fx_ar_OC']
fx_ar.columns = ['date','fx_ar']
fx_ur.columns = ['date','fx_ur']
fx_ar_CNY.columns = ['date','fx_ar_CNY']
fx_ar_CNY_pt.columns = ['date','fx_ar_CNY_pt']

cofer = fx.merge(fx_ar, how='outer').fillna(method='ffill')\
  .merge(fx_ur, how='outer').fillna(method='ffill')\
  .merge(fx_ar_USD, how='outer').fillna(method='ffill')\
  .merge(fx_ar_EURO, how='outer').fillna(method='ffill')\
  .merge(fx_ar_CNY, how='outer').fillna(method='ffill')\
  .merge(fx_ar_JPY, how='outer').fillna(method='ffill')\
  .merge(fx_ar_GBP, how='outer').fillna(method='ffill')\
  .merge(fx_ar_AUD, how='outer').fillna(method='ffill')\
  .merge(fx_ar_CAD, how='outer').fillna(method='ffill')\
  .merge(fx_ar_CHF, how='outer').fillna(method='ffill')\
  .merge(fx_ar_OC, how='outer').fillna(method='ffill')\
  .merge(fx_ar_CNY_pt, how='outer').fillna(method='ffill')\

cofer.date = pd.to_datetime(cofer.date)
cofer.fx = pd.to_numeric(cofer.fx) * 1000000
cofer.fx_ar = pd.to_numeric(cofer.fx_ar) * 1000000
cofer.fx_ur = pd.to_numeric(cofer.fx_ur) * 1000000
cofer.fx_ar_USD = pd.to_numeric(cofer.fx_ar_USD) * 1000000
cofer.fx_ar_EURO = pd.to_numeric(cofer.fx_ar_EURO) * 1000000
cofer.fx_ar_CNY = pd.to_numeric(cofer.fx_ar_CNY) * 1000000
cofer.fx_ar_JPY = pd.to_numeric(cofer.fx_ar_JPY) * 1000000
cofer.fx_ar_GBP = pd.to_numeric(cofer.fx_ar_GBP) * 1000000
cofer.fx_ar_AUD = pd.to_numeric(cofer.fx_ar_AUD) * 1000000
cofer.fx_ar_CAD = pd.to_numeric(cofer.fx_ar_CAD) * 1000000
cofer.fx_ar_CHF = pd.to_numeric(cofer.fx_ar_CHF) * 1000000
cofer.fx_ar_OC = pd.to_numeric(cofer.fx_ar_OC) * 1000000
cofer.fx_ar_CNY_pt = pd.to_numeric(cofer.fx_ar_CNY_pt)

# Plot Total Foreign Exchange
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
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx, mode='lines', name='Total_FX', line=dict(width=1.5, color='black')))
fig.update_layout(
    title_text="<b>Total Foreign Exchange</b>",
    xaxis_title='End of period <b>(Quarterly)</b>',
    yaxis_title='<b>USD</b> US Dollars',
    width=800,
    height=400,
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )
)
fig.show()

# Plot ar / ur
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
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ar, mode='lines', line=dict(width=0.5), stackgroup='cofer', name='Allocated Reserves', groupnorm='percent'))
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ur, mode='lines', line=dict(width=0.5), stackgroup='cofer', name='Unallocated Reserves'))
fig.update_layout(
    title_text="<b>Allocated / Unallocated Reserves</b>",
    xaxis_title='End of period <b>(Quarterly)</b>',
    yaxis_title='<b>%</b> Percentage',
    yaxis=dict(
      type='linear',
      range=[1, 100],
      ticksuffix='%'
    ),
    width=800,
    height=400,
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )
)
fig.show()

# Plot Share of CNY
fig = make_subplots(specs=[[{"secondary_y": True}]])
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
fig.add_trace( go.Scatter(x=cofer.date, y=cofer.fx_ar_CNY, mode='lines', name='CNY', line=dict(width=1.5, color='red')), secondary_y=False)
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ar_CNY_pt, mode='lines', name='CNY_Percent', line=dict(width=1.5, color='grey')), secondary_y=True)
fig.update_layout(
    title_text="<b>Shares of Chinese Renminbi in Cofer</b>",
    xaxis_title='End of period <b>(Quarterly)</b>',
    width=800,
    height=400,
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )
)
fig.update_yaxes(title_text=" <b>USD</b> US Dollars", secondary_y=False)
fig.update_yaxes(title_text="<b>%</b> Percentage", secondary_y=True)
fig.show()

# Plot Composition
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
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ar_USD, mode='lines', line=dict(width=0.5, color='navy'), stackgroup='cofer', name='USD', groupnorm='percent'))
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ar_EURO, mode='lines', line=dict(width=0.5, color='mediumturquoise'), stackgroup='cofer', name='EURO'))
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ar_CNY, mode='lines', line=dict(width=0.5, color='red'), stackgroup='cofer', name='CNY'))
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ar_JPY, mode='lines', line=dict(width=0.5, color='indigo'), stackgroup='cofer', name='JPY'))
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ar_GBP, mode='lines', line=dict(width=0.5, color='royalblue'), stackgroup='cofer', name='GBP'))
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ar_AUD, mode='lines', line=dict(width=0.5, color='darkorange'), stackgroup='cofer', name='AUD'))
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ar_CAD, mode='lines', line=dict(width=0.5, color='hotpink'), stackgroup='cofer', name='CAD'))
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ar_CHF, mode='lines', line=dict(width=0.5, color='lime'), stackgroup='cofer', name='CHF'))
fig.add_trace(go.Scatter(x=cofer.date, y=cofer.fx_ar_OC, mode='lines', line=dict(width=0.5, color='violet'), stackgroup='cofer', name='Other Currency'))
fig.update_layout(
    title_text="<b>Currency Composition of Official Foreign Exchange</b>",
    xaxis_title='End of period <b>(Quarterly)</b>',
    yaxis_title='<b>%</b> Percentage',
    yaxis=dict(
      type='linear',
      range=[1, 100],
      ticksuffix='%'
    ),
    width=800,
    height=1000,
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )
)
fig.show()