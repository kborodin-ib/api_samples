#! /usr/bin/env python3

import time
from ibapi.sync_wrapper import *
from datetime import datetime
from parseTemplate import createScanner
from ibapi.tag_value import TagValue
from ibapi.scanner import ScannerSubscription 
# Instantiate the reference for our sync class
app = TWSSyncWrapper(timeout=30)
# make a connection to Trader Workstation
# In this case, we're connecting on Localhost with port 7496 and Client ID 0.
# Connect to TWS
if not app.connect_and_start(host="172.23.208.1", port=7496, client_id=8675309):
    print("Failed to connect to TWS")
    exit(1)
else:
    print("Connected to TWS")

locationCodes = open('us_location_codes.txt', 'r').read()
instruments = open('us_instruments.txt', 'r').read()

code_list = locationCodes.split('\n')
instrument_list = instruments.split('\n')
#instrument_list = ['STK', 'STOCK.EU']
xml_template = "./xmls/sampleScan.xml"
scanner, tagsValues = createScanner(xml_template)
tagsValues = []
mktCapUsdAbv = TagValue('usdMarketCapAbove', 1)
tagsValues.append(mktCapUsdAbv)
req_id = 1 

for instr in instrument_list:
    scanner.instrument = instr
    for code in code_list:
        scanner.locationCode = code
        print(scanner)
        app.reqScannerSubscription(req_id, scanner, [], tagsValues)
        #time.sleep(1)
        if app.scanner_data:
            print("scanner data: ", app.scanner_data)
        #    time.sleep(5)
