#! /usr/bin/env python3

import logging
import ibapi
import time
import threading
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.execution import Execution
from ibapi.utils import decimalMaxString, floatMaxString, Decimal, intMaxString
from adaptiveBracketOrder import BracketOrder

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

    def openOrder(self, orderId, contract: Contract, order: Order,
                  orderState ):
        super().openOrder(orderId, contract, order, orderState)
        print("OpenOrder. PermId:", intMaxString(order.permId),
              "ParentPermID:", order.parentPermId, 
              "ParentID: ", order.parentId,
              "ClientId:", intMaxString(order.clientId), " OrderId:", intMaxString(orderId), 
              "Account:", order.account, "Symbol:", contract.symbol, "SecType:", contract.secType,
              "Exchange:", contract.exchange, "Action:", order.action, "OrderType:", order.orderType,
              "TotalQty:", decimalMaxString(order.totalQuantity), "CashQty:", floatMaxString(order.cashQty), 
              "LmtPrice:", floatMaxString(order.lmtPrice), "AuxPrice:", floatMaxString(order.auxPrice), "Status:", orderState.status,
              "MinTradeQty:", intMaxString(order.minTradeQty), "MinCompeteSize:", intMaxString(order.minCompeteSize),
              "MidOffsetAtWhole:", floatMaxString(order.midOffsetAtWhole),"MidOffsetAtHalf:" ,floatMaxString(order.midOffsetAtHalf))

        order.contract = contract

    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")

    def orderStatus(self, orderId, status: str, filled: Decimal,
                    remaining: Decimal, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        super().orderStatus(orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        print("OrderStatus. Id:", orderId, "Status:", status, "Filled:", decimalMaxString(filled),
              "Remaining:", decimalMaxString(remaining), "AvgFillPrice:", floatMaxString(avgFillPrice),
              "PermId:", intMaxString(permId), "ParentId:", intMaxString(parentId), "LastFillPrice:",
              floatMaxString(lastFillPrice), "ClientId:", intMaxString(clientId), "WhyHeld:",
              whyHeld, "MktCapPrice:", floatMaxString(mktCapPrice))

    def modifyBracketOrder(self, orderID, execPrice):

        stopPrice = execPrice - execPrice * 0.01
        takePrice = execPrice + execPrice * 0.01

        contract = Contract()
        contract.exchange = "SMART"
        contract.symbol = "BMW"
        contract.currency = "EUR"
        contract.secType = "STK"

        bracket_order = BracketOrder(parentOrderId=orderID,
                                     action="BUY",
                                     quantity=4,
                                     limitPrice=103.5,
                                     takeProfitLimitPrice=takePrice,
                                     stopLossPrice=stopPrice)
        for bo in bracket_order:
            self.placeOrder(bo.orderId, contract, bo)

    def placeBracketOrder(self, orderID, takeProfitPrice, stopLossPrice):
        bracket_order = BracketOrder(orderID, "BUY", 1,limitPrice=1, takeProfitLimitPrice=takeProfitPrice,
                                     stopLossPrice=stopLossPrice)
        contract = Contract()
        contract.exchange = "SMART"
        contract.symbol = "BMW"
        contract.currency = "EUR"
        contract.secType = "STK"
        for bo in bracket_order:
            print(bo)
            self.placeOrder(bo.orderId, contract, bo)

#        time.sleep(4)

#        self.modifyBracketOrder(self.nextValidOrderId, 12)

    def start(self):
        orderId = self.nextValidOrderId
        while True:
            self.placeBracketOrder(orderId, 103, 80)
            orderId += 4
            print("Hello, order id is: ", self.nextValidOrderId)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('172.22.21.200', 7496, 12)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(5, app.stop).start()
        threading.Thread(target=app.run).start()
        threading.Thread(target=app.run).start()
        threading.Thread(target=app.run).start()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
