#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
import csv
from ibapi.contract import Contract
from ibapi.order import Order
import logging
from ibapi.order_cancel import OrderCancel

import os

#logging.basicConfig(
#                level = logging.INFO,
#                format = '%(asctime)s - %(levelname)s - %(message)s',
#                datefmt='%Y-%m-%d %H:%M:%S'
#                )
#logger = logging.getLogger(__name__)

class TestApp(EWrapper, EClient):


    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    def error(self, reqId: int, errorTime, errorCode: int, errorString: str,
              advansedOrderreject=''):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}, {errorTime}'
        print(error_message)

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print(contractDetails)

    def contractDetailsEnd(self, reqId):
        super().contractDetailsEnd(reqId)
        print("Contract details end for ", reqId)
       
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId # Snippet 1
        print("NVOID: ", self.nextValidOrderId)
        self.start()

    def openOrder(self, orderId, contract, order, orderState):
        print("Open Order: ", orderId, contract, order)
        print("Order State: ", orderState)

    def orderStatus(self, orderId, status, filled, remaining,
            avgFillPrice, permid, parentId, lastFillPrice,
            clientId, whyHeld, mktCapPrice):
        if status == 'Submitted' or status == 'PreSubmitted':
            self.cancelOrder(int(orderId), OrderCancel())

    def placeCancelFOP(self, oid):
        
        contract = Contract()
        contract.symbol = "ES"
        contract.exchange = "CME"
        contract.currency = "USD"
        contract.secType = "FOP"
        contract.lastTradeDateOrContractMonth = "20260320"
        contract.right = "C"
        contract.strike = 7025
        contract.multiplier = 50
        contract.tradingClass = "ES"

        lmtOrder = Order()

        lmtOrder.orderType = "LMT"
        lmtOrder.action = "SELL"
        lmtOrder.lmtPrice = 140 
        lmtOrder.outsideRth = True
        lmtOrder.totalQuantity = 1

        self.placeOrder(oid, contract, lmtOrder)
        
    def start(self):

        oid = self.nextValidOrderId
        self.placeCancelFOP(oid)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('172.23.208.1', 7496, clientId=5)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
