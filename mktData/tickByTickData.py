#! /usr/bin/env python3

from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        # mycontract.conId = 76792991
        mycontract.symbol = "EUR"
        mycontract.secType = "CASH"
        mycontract.exchange = "IDEALPRO"
        mycontract.currency = "USD"

        # self.reqMarketDataType(3)

        self.reqTickByTickData(
            reqId=123,
            contract=mycontract,
            tickType="Last",
            numberOfTicks=1000,
            ignoreSize=False
        )

    # whatToShow=BidAsk
    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float, bidSize: int, askSize: int, tickAttribBidAsk: TickAttribBidAsk):
        print(f"reqId: {reqId}, time: {datetime.fromtimestamp(time) }, bidPrice: {bidPrice}, askPrice: {askPrice}, bidSize: {bidSize}, askSize: {askSize}, tickAttribBidAsk: {tickAttribBidAsk}")

    # whatToShow=MidPoint
    def tickByTickMidPoint(self, reqId: int, time: int, midPoint: float):
        print(f"reqId: {reqId}", time, midPoint)

    # # whatToShow=AllLast
    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float, size: int, tickAttribLast: TickAttribLast, exchange: str, specialConditions: str):
        # Tick type does not correspond to tickType.py
        if tickType == 1:
            print(f"Last. reqId: {reqId}, time: {datetime.fromtimestamp(time)}, price: {price}, size: {size}, tickAttribLast: {tickAttribLast}, exchange: {exchange}, specialConditions: {specialConditions}")
        else:
            print(f"AllLast. reqId: {reqId}, time: {datetime.fromtimestamp(time)}, price: {price}, size: {size}, tickAttribLast: {tickAttribLast}, exchange: {exchange}, specialConditions: {specialConditions}")
        

    def tickSnapshotEnd(self, reqId: int):
        print(f"tickSnapshotEnd. reqId:{reqId}")


app = TestApp()
app.connect("192.168.43.222", port, 1001)
app.run()
