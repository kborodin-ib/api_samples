#! /usr/bin/env python3

import logging
import datetime
import sys
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

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def tickPrice(self, reqId, tickType, price: float,
                  attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if tickType == 4:
            print("TickPrice. TickerId:", reqId, "tickType:", tickType,
                  "Price:", floatMaxString(price), "CanAutoExecute:", attrib.canAutoExecute,
                  attrib.preOpen)

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("contract details: ", reqId, contractDetails)

    def tickSize(self, reqId, tickType, size):
        super().tickSize(reqId, tickType, size)
        if tickType == 4:
            print("TickSize. TickerId:", reqId, "TickType:", tickType, "Size: ", decimalMaxString(size))

    def tickGeneric(self, reqId, tickType, value: float):
        super().tickGeneric(reqId, tickType, value)
        print("TickGeneric. TickerId:", reqId, "TickType:", tickType, "Value:", floatMaxString(value))

    def tickString(self, reqId, tickType, value: str):
        super().tickString(reqId, tickType, value)
        print("TickString. TickerId:", reqId, "Type:", tickType, "Value:", value)

    def tickSnapshotEnd(self, reqId: int):
        super().tickSnapshotEnd(reqId)
        print("TickSnapshotEnd. TickerId:", reqId)

    def openOrder(self, orderId, contract, order, orderState):
            print(orderId, contract, order, orderState)

    def orderStatus(self, orderId, status: str, filled, remaining, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
          super().orderStatus(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def execDetails(self, reqId: int, contract, execution):
          print("ExecDetails. ReqId:", reqId, "Symbol:", contract.symbol, "SecType:", contract.secType, "Currency:", contract.currency, execution)
        
    def currentTime(self, time):
        super().currentTime(time)
        print("current server time: ", time)

    def start(self):
        contract = CustomContracts().isinAaplContract()
        
        print('hello')
        print(contract)
        self.reqCurrentTime()
        self.reqContractDetails(self.nextValidOrderId, contract)
#        self.reqMarketDataType('1')
#        self.reqMktData(8, contract, '', False, False, [])

    def stop(self):
        self.done = True
        print("Stopped")
        self.disconnect()

def main():
    app = TestApp()
    cid = sys.argv[1]
    port = int(sys.argv[2])
    while True:
        if not app.isConnected():
            app.connect('172.22.21.200', port, clientId=cid)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
    #   Timer(15, app.stop).start()
        app.run()

if __name__ == '__main__':
    main()
