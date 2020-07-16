# only uncomment it in jupyter notebook
# import sys
# !{sys.executable} -m pip install matplotlib >/dev/null 2>&1

import matplotlib.pyplot as plt
import urllib.request
import json
from datetime import datetime
import ssl
context = ssl._create_unverified_context()

print("dependency ready")

# ---------------- Monetary Base Data ----------------


def get_MBC_from_HKMA():
    # Monetary Base Data released by hkma monthly
    url = 'https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/monetary-operation/monetary-base-endperiod?choose=end_of_month&from=1998-09&to=now&sortby=end_of_month&sortorder=asc'

    # retrieve data from hkma api, 100 entries per call, untill every data are retrieveed
    records = []
    offset = 0
    while True:
        with urllib.request.urlopen(url+"&offset="+str(offset), context=context) as req:
            data = json.loads(req.read().decode())
            records += data['result']['records']
        if data['result']['datasize'] <= 0:
            break
        else:
            offset += 100

    # now data retrieved from hkma are stored in 'records' in a chronological order
    return records


def MBC():
    records = get_MBC_from_HKMA()

    # prepare formattedX and formattedY to plot a stacked area graph
    formattedX = []
    formatted_cert_of_indebt = []
    formatted_gov_notes_coins_circulation = []
    formatted_aggr_balance_bf_disc_win = []
    formatted_outstanding_efbn = []
    formattedY = []

    for record in records:
        formattedX += [record['end_of_month']]
        # cert_of_indebt
        formatted_cert_of_indebt += [record['cert_of_indebt']]
        # gov_notes_coins_circulation
        formatted_gov_notes_coins_circulation += [
            record['gov_notes_coins_circulation']]
        # aggr_balance_bf_disc_win
        formatted_aggr_balance_bf_disc_win += [
            record['aggr_balance_bf_disc_win']]
        # outstanding_efbn
        formatted_outstanding_efbn += [record['outstanding_efbn']]

    formattedY = [formatted_cert_of_indebt,
                  formatted_gov_notes_coins_circulation,
                  formatted_aggr_balance_bf_disc_win,
                  formatted_outstanding_efbn]

    # Plot mbc
    plt.stackplot(
        formattedX,
        formattedY,
        labels=['cert_of_indebt',
                'gov_notes_coins_circulation',
                'aggr_balance_bf_disc_win',
                'outstanding_efbn']
    )
    plt.title("Monetary Base Composition")
    plt.xlabel("End of month")
    plt.ylabel("HK$ million")
    plt.xticks([formattedX[-1], '2016-06', '2012-06',
                '2008-06', '2004-06', '1998-09'])
    plt.legend(loc='upper left')
    plt.show()


# MBC()

# ---------------- 1. Money Multiplier = M3 / MB (HKD) ----------------
def get_MSA_from_HKMA():
    # Monetary Supply-Ddjusted
    url = 'https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/money/supply-adjusted?choose=end_of_month&from=1998-09&to=now&sortby=end_of_month&sortorder=asc'

    # retrieve data from hkma api, 100 entries per call, untill every data are retrieveed
    records = []
    offset = 0
    while True:
        with urllib.request.urlopen(url+"&offset="+str(offset), context=context) as req:
            data = json.loads(req.read().decode())
            records += data['result']['records']
        if data['result']['datasize'] <= 0:
            break
        else:
            offset += 100

    # now data retrieved from hkma are stored in 'records' in a chronological order
    return records


def MM():
    mbc_records = get_MBC_from_HKMA()
    msa_records = get_MSA_from_HKMA()

    syncLength = min(len(mbc_records), len(msa_records))
    mbc_records = mbc_records[:syncLength]  # mb_bf_disc_win_total
    msa_records = msa_records[:syncLength]  # m3_total

    formatted_X = []
    formatted_mm_Y = []
    formatted_m3_total_Y = []
    formatted_mb_total_Y = []

    for i in range(syncLength):
        mm = msa_records[i]['m3_total'] / \
            mbc_records[i]['mb_bf_disc_win_total']
        end_of_month = msa_records[i]['end_of_month']

        if(not msa_records[i]['end_of_month'] == mbc_records[i]['end_of_month']):
            print("something wrong here, please check")  # date sync check

        formatted_X += [end_of_month]
        formatted_mm_Y += [mm]
        formatted_m3_total_Y += [msa_records[i]['m3_total']]
        formatted_mb_total_Y += [mbc_records[i]['mb_bf_disc_win_total']]

    # Plot mm
    plt.plot(formatted_X, formatted_mm_Y, color='orange',
             linewidth=4, alpha=0.7, label="money multiplier")
    plt.title("1. Money Multiplier = M3 / MB (HKD)")
    plt.xlabel("End of month")
    plt.ylabel("m3 to mb ratio")
    plt.xticks([formatted_X[-1], '2016-06', '2012-06',
                '2008-06', '2004-06', '1998-09'])
    plt.legend(loc='upper left')
    plt.show()

    # Plot m3
    plt.plot(formatted_X, formatted_m3_total_Y, color='red',
             linewidth=4, alpha=0.7, label="m3")
    plt.title("M3 Total")
    plt.xlabel("End of month")
    plt.ylabel("HK$ million")
    plt.xticks([formatted_X[-1], '2016-06', '2012-06',
                '2008-06', '2004-06', '1998-09'])
    plt.legend(loc='upper left')
    plt.show()

    # Plot mb
    plt.plot(formatted_X, formatted_mb_total_Y, color='blue',
             linewidth=4, alpha=0.7, label="mb")
    plt.title("Total Monetary Base before Discount Window")
    plt.xlabel("End of month")
    plt.ylabel("HK$ million")
    plt.xticks([formatted_X[-1], '2016-06', '2012-06',
                '2008-06', '2004-06', '1998-09'])
    plt.legend(loc='upper left')
    plt.show()

# MM()

# ---------------- 2. Total deposits & M3 (HKD) ----------------
def get_TD_from_HKMA():
    # Monetary Supply-Ddjusted
    url = 'https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/banking/customer-deposits-by-currency?choose=end_of_month&from=1998-09&to=no&sortby=end_of_month&sortorder=asc'

    # retrieve data from hkma api, 100 entries per call, untill every data are retrieveed
    records = []
    offset = 0
    while True:
        with urllib.request.urlopen(url+"&offset="+str(offset), context=context) as req:
            data = json.loads(req.read().decode())
            records += data['result']['records']
        if data['result']['datasize'] <= 0:
            break
        else:
            offset += 100

    # now data retrieved from hkma are stored in 'records' in a chronological order
    return records


def TDHKD():
    msa_records = get_MSA_from_HKMA()
    td_records = get_TD_from_HKMA()  # deposits_hkd

    syncLength = min(len(td_records), len(msa_records))
    td_records = td_records[:syncLength]  # deposits_hkd
    msa_records = msa_records[:syncLength]  # m3_total

    formatted_X = []
    formatted_tdhkd_Y = []
    formatted_m3_total_Y = []

    for i in range(syncLength):
        end_of_month = msa_records[i]['end_of_month']
        if(not msa_records[i]['end_of_month'] == td_records[i]['end_of_month']):
            print("something wrong here, please check")  # date sync check

        formatted_X += [end_of_month]
        formatted_m3_total_Y += [msa_records[i]['m3_total']]
        formatted_tdhkd_Y += [td_records[i]['deposits_hkd']]

    # Plot tdhkd
    plt.plot(formatted_X, formatted_tdhkd_Y, color='green',
             linewidth=4, alpha=0.7, label="m3")
    plt.title("2. Total deposits (HKD)")
    plt.xlabel("End of month")
    plt.ylabel("HK$ million")
    plt.xticks([formatted_X[-1], '2016-06', '2012-06',
                '2008-06', '2004-06', '1998-09'])
    plt.legend(loc='upper left')
    plt.show()

    # Plot m3
    plt.plot(formatted_X, formatted_m3_total_Y, color='red',
             linewidth=4, alpha=0.7, label="m3")
    plt.title("M3 Total")
    plt.xlabel("End of month")
    plt.ylabel("HK$ million")
    plt.xticks([formatted_X[-1], '2016-06', '2012-06',
                '2008-06', '2004-06', '1998-09'])
    plt.legend(loc='upper left')
    plt.show()

    # Plot tdhkd and m3
    fig, ax1 = plt.subplots()

    color = 'tab:green'
    ax1.set_xlabel("End of month")
    ax1.set_ylabel("HK$ million", color=color)
    ax1.set_xlabel('time (s)')
    ax1.plot(formatted_X, formatted_tdhkd_Y, color=color, label="Total deposits (HKD)")
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax1.set_xticks([formatted_X[-1], '2016-06', '2012-06',
                '2008-06', '2004-06', '1998-09'])

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel("HK$ million", color=color)
    ax2.plot(formatted_X, formatted_m3_total_Y, color=color, label="M3 Total")
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax2.set_xticks([formatted_X[-1], '2016-06', '2012-06',
                '2008-06', '2004-06', '1998-09'])

    ax1.legend(loc='upper left')
    ax2.legend(loc='center left')
    ax1.set_title("Total deposits (HKD) and M3 Total Correlation")
    plt.show()

# TDHKD()