#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
import csv
from ibapi.contract import Contract
from ibapi.order import Order
import logging
from ibapi.order_cancel import OrderCancel
from ibapi.tag_value import TagValue

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
        self.dataframe = {}
        self.contracts = []

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
        print("Order that is placed: ", order)
        print("Order was placed from: ", order.account)
        print("Order is allocated to: ", order.faGroup)
        #self.disconnect()

    def orderStatus(self, orderId, status, filled, remaining,
            avgFillPrice, permid, parentId, lastFillPrice,
            clientId, whyHeld, mktCapPrice):
        oid = self.reqIds(-1)
        print(f"Order Status: id: {orderId}, status: {status}," +\
                f"filled: {filled}, remaining: {remaining}," +\
                f"avgFillPrice: {avgFillPrice}, permid: {permid}," +\
                f"parentId: {parentId}, lastFillPrice: {lastFillPrice}," +\
                f"clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def bracketOrderMOC(self, parent_order_id, action, quantity, limit_price,
                        take_profit_price):

         parent = Order()
         parent.orderId = parent_order_id 
         parent.action = action
         parent.orderType = "LMT"
         parent.totalQuantity = quantity
         parent.lmtPrice = limit_price 
         parent.tif = "DAY"
         parent.transmit = False

         takeProfit = Order()
         takeProfit.orderId = parent.orderId + 1
         takeProfit.action = "SELL" if action == "BUY" else "BUY"
         takeProfit.orderType = "LMT"
         takeProfit.totalQuantity = 1 
         takeProfit.lmtPrice = take_profit_price 
         takeProfit.parentId = parent_order_id 
         takeProfit.transmit = False
         takeProfit.tif = "DAY"

         stopLoss = Order()
         stopLoss.orderId = parent.orderId + 2
         stopLoss.action = "SELL" if action == "BUY" else "BUY"
         stopLoss.orderType = "MOC"
         stopLoss.totalQuantity = quantity
         stopLoss.parentId = parent_order_id
         stopLoss.tif = "DAY"
         stopLoss.transmit = True

         bracketOrder = [parent, takeProfit, stopLoss]

         return bracketOrder

    def start(self):

        bmw_contract = Contract()
        bmw_contract.symbol = "BMW"
        bmw_contract.secType = "STK"
        bmw_contract.exchange = "SMART"
        bmw_contract.currency = "EUR"

        oid = self.nextValidOrderId
        bracketMOClong = self.bracketOrderMOC(oid, "BUY", 1, 89.78, 89.74)
        for o in bracketMOClong:
            self.placeOrder(o.orderId, bmw_contract, o)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('172.23.208.1', 7496, clientId=5)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
