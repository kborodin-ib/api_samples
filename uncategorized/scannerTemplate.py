#! /usr/bin/env python3

import logging
import datetime
from threading import Timer
import ibapi
import time
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString
from ibapi.scanner import ScannerSubscription
from ibapi.tag_value import TagValue
from createScanner import createScanner

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def scannerData(self, reqId, rank, contractDetails, distance,
            benchmark, projection, legsStr):
        super().scannerData(reqId, rank, contractDetails, distance, benchmark,
                projection, legsStr)
        print("Scanner Dta. ReqID: ", reqId, contractDetails.contract, rank,
                distance, benchmark, projection, legsStr)
    
    def scannerDataEnd(self, reqId):
        super().scannerDataEnd(reqId)
        print("ScannerDataEnd ReqId: ", reqId)

    def scannerParameters(self, xml):
        super().scannerParameters(xml)
        open('scanner.xml', 'w').write(xml)
        print("Scanner params received")

    def start(self):
        
#        scanner, tagsValues = createScanner("sampleScan.xml")

        scanner = ScannerSubscription()
        scanner.instrument = "BOND"
        scanner.locationCode = "BOND.US"
        scanner.scanCode = "HIGH_BOND_ASK_YIELD_ALL"
        scanner.numberOfRows = 20

        tagsValues = []

        self.reqScannerParameters()

        self.reqScannerSubscription(self.nextValidOrderId, scanner, [],
                tagsValues)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('172.22.21.200', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()


