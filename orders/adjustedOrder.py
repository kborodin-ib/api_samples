#! /usr/bin/env python3

from ibapi.client import *
from ibapi.wrapper import *

port=7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def adjustedOrder(self, orderId):

        order1 = Order()
        order1.orderId = orderId
        order1.action = "BUY"
        order1.tif = "DAY"
        order1.totalQuantity = 1 
        order1.orderType = "TRAIL LIMIT"
        order1.trailingPercent = 4
        order1.trailStopPrice = 78 
        order1.lmtPriceOffset = 80

        # Adjusted trailing stop limit order
        order2 = Order()
        order2.parentId = order1.orderId
        order2.orderId = order1.orderId+1
        order2.action = "SELL"
        order2.tif = "DAY"
        order2.totalQuantity = 1
        order2.orderType = 'MKT'
        order2.trailingPercent = 4
#        order2.triggerPrice = 103.65 
        order2.adjustedOrderType = "STP LMT"
        order2.adjustableTrailingUnit = 1
        order2.adjustedStopLimitPrice = 108.1
#        order2.adjustedStopPrice = 103.80
#        order2.auxPrice = 103.80

        return [order1, order2]

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "BMW"
        mycontract.secType = "STK"    
        mycontract.exchange = "SMART"
        mycontract.currency = "EUR"

        orders = self.adjustedOrder(orderId)
        oid = orderId 
        for o in orders:
            self.placeOrder(oid, mycontract, o)
            oid += 1

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}") 
        print(f"Maintenance Margin: {orderState.maintMarginAfter}, {orderState.maintMarginBefore}, {orderState.maintMarginChange}")
        print(f"Initial Margin: {orderState.initMarginAfter}, {orderState.initMarginBefore}, {orderState.initMarginChange}")


    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)

app = TestApp()
app.connect("172.22.21.200", port, 7496)
app.run()
