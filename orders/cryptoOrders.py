#! /usr/bin/env python3

import logging
import ibapi
import time
from threading import Timer
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.execution import Execution
from ibapi.order import Order
from contracts import CustomContracts

class TestApp(EWrapper, EClient):


    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}

    def error(self, reqId: int, errorCode: int, errorString: str,
              advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'
        print(error_message)
       
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId # Snippet 1
        print(self.nextValidOrderId)
        self.start()

    def openOrder(self, orderId, contract, order, orderState):
        print("Open Order: ", orderId, contract, order)

    def orderStatus(self, orderId, status, filled, remaining,
            avgFillPrice, permid, parentId, lastFillPrice, 
            clientId, whyHeld, mktCapPrice):
        print(f"Order Status: id: {orderId}, status: {status}," +\
                f"filled: {filled}, remaining: {remaining}," +\
                f"avgFillPrice: {avgFillPrice}, permid: {permid}," +\
                f"parentId: {parentId}, lastFillPrice: {lastFillPrice}," +\
                f"clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")


    def start(self):

        # BUY orders - must use cashQty (with totalQuantity=0)  &  TIF=IOC
        # SELL orders - must use totalQuantity**  &  TIF=IOC -> if I use cashQty at all for sell orders I get "Error 10244 Cash Quantity cannot be used for this order"

        contract = CustomContracts().cryptoContract() 
        orderMktBuy = Order()
        orderMktBuy.action = 'BUY'
        orderMktBuy.orderType = 'MKT'
        orderMktBuy.cashQty = 1 
        orderMktBuy.totalQuantity = 0
        orderMktBuy.tif = 'IOC'
        
        orderMktSell = Order()
        orderMktSell.action = 'SELL'
        orderMktSell.orderType = 'MKT'
        orderMktSell.totalQuantity = .1
        orderMktSell.tif = 'IOC'

        orderLmtBuy = Order()
        orderLmtBuy.action = 'BUY'
        orderLmtBuy.orderType = 'LMT'
        orderLmtBuy.lmtPrice = 64031.0
        orderLmtBuy.totalQuantity = '0.00001562' 
        orderLmtBuy.tif = 'IOC'
        
        orderLmtSell = Order()
        orderLmtSell.action = 'SELL'
        orderLmtSell.orderType = 'LMT'
        orderLmtSell.lmtPrice = 64031.0
        orderLmtSell.totalQuantity = '0.00001562' 
        orderLmtSell.tif = 'IOC'

        orders = [orderMktBuy, orderMktSell, orderLmtBuy, orderLmtSell]
        
        orderId = self.nextValidOrderId
        for o in orders:
            self.placeOrder(orderId, contract, o)
            orderId += 1
        

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
