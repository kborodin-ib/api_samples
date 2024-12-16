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
from contracts import CustomContracts

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    # WRAPPERS HERE

#    def error(self, reqId: int, errorCode: int, errorString,
#            advansedOrderreject=""):
#        super().error(reqId, errorCode, errorString, advansedOrderreject)
#        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
#                        + f'Msg: {errorString}'

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def historicalTicks(self, reqId, ticks, done):
        for tick in ticks:
            print(tick)

    def historicalTicksLast(self, reqId, ticks, done):
        for tick in ticks:
            print(tick)

        
    def start(self):


        contracts = CustomContracts()
        print(contracts.aaplOptContract())

        aapOpt = contracts.aaplOptContract()
        print(aapOpt)
        print(type(aapOpt))

        self.reqHistoricalTicks(self.nextValidOrderId, aapOpt, "20240403 09:30:00", "", 100, "TRADES", 1, True, [])

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
