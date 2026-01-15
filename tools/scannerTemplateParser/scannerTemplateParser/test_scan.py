#! /usr/bin/env python3

import logging
import datetime
import ibapi
import time
import sys
import os
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString
from ibapi.scanner import ScannerSubscription
from ibapi.tag_value import TagValue
from parseTemplate import createScanner
from threading import Timer

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.scannerObject = ''

    # WRAPPERS HERE

    def error(self, reqId: int, errorTime, errorCode: int, errorString: str,
            advansedOrderreject=''):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'error time: {errorTime} Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'
        print(error_message)
        if '162' in error_message:
            print('Error code 162')
            self.scanner_done = True

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")


    def scannerData(self, reqId, rank, contractDetails, distance,
            benchmark, projection, legsStr):
        super().scannerData(reqId, rank, contractDetails, distance, benchmark,
                projection, legsStr)
        print("Scanner Dta. ReqID: ", reqId, contractDetails.contract, rank, distance, benchmark, projection, legsStr)

    def scannerDataEnd(self, reqId):
        super().scannerDataEnd(reqId)
        print("ScannerDataEnd ReqId: ", reqId)
        self.scanner_done = True
        self.cancelScannerSubscription(reqId)

    def scannerParameters(self, xml):
        super().scannerParameters(xml)
        open('scanner.xml', 'w').write(xml)
        print("Scanner params received")

    def start(self):
        # .stp is exported from TWS -> Advansed Scanner -> Export  
        # It is recommended to first create a desired scanner  in TWS
        # and export it's settings.
        scanner, tagsValues = createScanner(self.scannerObject)
        locations = ['STK.NASDAQ', 'STK.US.MAJOR']
        scanner.locationCode = locations.pop(0) 
        mktCapUsdAbv = TagValue('usdMarketCapAbove', 1)
#        mktCapUsdBlv = ['usdMarketCapBelove', 1]
        tagsValues.append(mktCapUsdAbv)
#        tagsValues.append(mktCapUsdBlv)
#                self.reqScannerParameters()

        scanner.numberOfRows = 50 

        self.reqScannerSubscription(self.nextValidOrderId, scanner, [],
                tagsValues)
        print(self.scanner_done)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        scanTemp = "./xmls/market_cap_above.xml"
        if not os.path.exists(scanTemp):
            print("Specified path does not exist")
            sys.exit()
        if not scanTemp.endswith('xml'):
            print("Wrong extension, change .stp to .xml")
            sys.exit()
    except IndexError:
        print("Path to scanner template as first argument: ./scannerRun 'sample.xml'")
        sys.exit()
    try:
        app = TestApp()
        app.connect('172.23.208.1', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()


