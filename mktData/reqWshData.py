#! /usr/bin/env python3

import logging
import datetime
from threading import Timer
import ibapi
import time
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract, ComboLeg
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString
from ibapi.common import WshEventData


def aaplContract():

    contract = Contract()
    contract.exchange = "SMART"
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.currency = "USD"

    return contract

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject=""):
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

    def wshMetaData(self, reqId, dataJson):
        super().wshMetaData(reqId, dataJson)
        print("WSH Metadata: ", "ReqId: ", reqId, "DataJSON: ", dataJson)

    def wshEventData(self, reqId, dataJson):
        super().wshEventData(reqId, dataJson)
        print("WSH EventData: ", "ReqId: ", reqId, "DataJSON: ", dataJson)


    def start(self):
        contract = aaplContract()
        # Comment out the line below to receive live data 
        self.reqWshMetaData(self.nextValidOrderId)
#        wshEventData = WshEventData()
#        wshEventData.conId = 8314
#        wshEventData.startDate = "20220511"
#        wshEventData.endDate = "20220611"
#        wshEventData.totalLimit = 5
#        self.reqWshEventData(self.nextValidOrderId, wshEventData)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
#        print(f'ibapi version: ', ibapi.__version__)
        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
