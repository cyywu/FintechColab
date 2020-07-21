import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import urllib.request
import json
from datetime import datetime
import pandas as pd
import ssl
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
                    RAXGFX_AR_CNY_USD]

url = COFER_url \
    + COFER_FREQ \
    + "." + COFER_AREA + "." \
    + ('+'.join(COFER_INDICATORS)) + "?" \
    + "startPeriod=" + COFER_startPeriod + "&" \
    + "endPeriod=" + COFER_endPeriod

with urllib.request.urlopen(url, context=context) as req:
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
      .merge(fx_ar_OC, how='outer').fillna(method='ffill')

    # cofer.date = pd.to_datetime(cofer.date)
    cofer.fx = pd.to_numeric(cofer.fx)
    cofer.fx_ar = pd.to_numeric(cofer.fx_ar)
    cofer.fx_ur = pd.to_numeric(cofer.fx_ur)
    cofer.fx_ar_USD = pd.to_numeric(cofer.fx_ar_USD)
    cofer.fx_ar_EURO = pd.to_numeric(cofer.fx_ar_EURO)
    cofer.fx_ar_CNY = pd.to_numeric(cofer.fx_ar_CNY)
    cofer.fx_ar_JPY = pd.to_numeric(cofer.fx_ar_JPY)
    cofer.fx_ar_GBP = pd.to_numeric(cofer.fx_ar_GBP)
    cofer.fx_ar_AUD = pd.to_numeric(cofer.fx_ar_AUD)
    cofer.fx_ar_CAD = pd.to_numeric(cofer.fx_ar_CAD)
    cofer.fx_ar_CHF = pd.to_numeric(cofer.fx_ar_CHF)
    cofer.fx_ar_OC = pd.to_numeric(cofer.fx_ar_OC)

    print(cofer.date.values.tolist())
    print(cofer.fx.values.tolist())