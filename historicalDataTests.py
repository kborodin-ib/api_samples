#! /usr/bin/env python3

import requests
import ssl
import threading
import json
import time

from datetime import datetime

sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS)
sslContext.verify_mode = ssl.CERT_NONE

requests.packages.urllib3.disable_warnings()

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"
headers = {
        "User-Agent": "python-requests/2.28.1",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-type": "application/json"
        }

def checkAuthStatus():
    resp = requests.get(base_url + "/iserver/auth/status", verify=False)
    print(f"[+] Auth response: {resp.text}")

def historicalData(conid, exchange, period, bar, outsideRth, startTime):
    sleep_time = 5 # 5 seconds to sleep before next request
    params = {
            "conid": conid,
            "exchange": exchange,
            "period": period,
            "bar": bar,
            "outsideRth": outsideRth,
            "startTime": startTime
            }

    response = requests.get(base_url + '/iserver/marketdata/history', params=params, verify=False)
    if response.status_code == 503:
        # Try again recursively until data is returned
        historicalData(params['conid'], params['exchange'], params['period'],
                       params['bar'], params['outsideRth'], params['startTime'])
    if response.status_code != 200:
        print(f"[{conid}] Data unavailable; HTTP status: {response.status_code}, Error: {response.text}")
    else:
        print(f"[{conid}] historical data:\n {response.text}\n")
        return

def historicalDataBeta(conid, exchange, period, bar, outsideRth, barType, startTime, direction, outFile):

    params = {
            "conid": conid,
            "exchange": exchange,
            "period": period,
            "bar": bar,
            "outsideRth": outsideRth,
            "barType": barType,
            "startTime": startTime,
            "direction": direction,
            }

    response = requests.get(base_url + '/hmds/history', params=params, verify=False)
    if response.status_code == 503:
        # Try again recursively until data is returned
        print("---> 503; Service unavailable, trying again")
        historicalDataBeta(params['conid'], params['exchange'], params['period'],
                       params['bar'], params['outsideRth'], params['barType'], params['startTime'], params['direction'])
    if response.status_code != 200:
        print(f"[{conid}] Data unavailable; HTTP status: {response.status_code}, Error: {response.text}")
    else:
        # Write historical data to a frame
        jsonData = json.loads(response.text)
        print(f"[{conid}] historical data:\n {json.dumps(jsonData, indent=4)}\n")
        with open(outFile, "a") as file:
            file.write(json.dumps(jsonData, indent=4))
        return

def getAllDatasConcurrently(conidList):

    threads=[]

    # query params
    exchange = "SMART"
    period = "1D"
    bar = '1h'
    outsideRth = True
    startTime = ''

    for conid in conidList:
        thread = threading.Thread(target=historicalData, args=(conid,exchange,period,bar,outsideRth,startTime))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def getAllDatasSequentially(conidlist, outFile):


    hmdsAuthInit = requests.post(base_url + "/hmds/auth/init", verify=False)

    print(f"[+] Response from /hmds/auth/init: {hmdsAuthInit.text}")

    for conid in conidlist:
        historicalDataBeta(conid, 'SMART', '11y', '1d', False, 'Inventory', "20250720-00:00:00", '-1', outFile)

def compareOutputs(first_file, second_file):
    with open(first_file, 'r') as file1:
        with open(second_file, 'r') as file2:
            difference = set(file1).difference(file2)
            if len(difference) > 0:
                print(f"[+] Files are not identical. \n {difference}")

    difference.discard('\n')

    with open('diff.txt', 'w') as file_out:
        for line in difference:
            file_out.write(line)

def checkHistoricalOutput(listOconnodis):
    filename_uno = "testOutUno.txt"
    filename_dos = "testOutDos.txt"
    print(f"[+] Retrieving first dataset, writing to {filename_uno}")
    getAllDatasSequentially(listOconnodis, filename_uno)
    time.sleep(5)
    print(f"[+] Retrieving second dataset. Writing to {filename_dos}")
    getAllDatasSequentially(listOconnodis, filename_dos)
    print(f"[+] Comparing {filename_uno} and {filename_dos}. Diffences, if any are written to 'diff.txt'.")
    compareOutputs(filename_uno, filename_dos)

if __name__ == "__main__":
    checkAuthStatus()
    listOconnodis = [265598,14094,4350,4661,4521593,2730872]
    checkHistoricalOutput(listOconnodis)
