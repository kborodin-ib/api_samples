#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
import datetime
from ibapi.contract import (Contract, ContractDetails)
from ibapi.utils import Decimal, floatMaxString, decimalMaxString

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    # WRAPPERS HERE
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        #logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
       # As soon as next valid id is received it is safe to send requests
        self.start()


    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)
        self.contract = contractDetails.contract # store contract in the TestApp instance
        symbol = contractDetails.contract.symbol
        self.reqHistoricalNews(reqId, contractDetails.contract.conId , "BRFG", "", "", 300, [])

    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float,
                          size: Decimal, tickAtrribLast, exchange: str,
                          specialConditions: str):
        super().tickByTickAllLast(reqId, tickType, time, price, size, tickAtrribLast,
                                  exchange, specialConditions)
        if tickType == 1:
            print("Last.", end='')
        else:
            print("AllLast.", end='')
        print(" ReqId:", reqId,
              "Time:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d-%H:%M:%S"),
              "Price:", floatMaxString(price), "Size:", decimalMaxString(size), "Exch:" , exchange,
              "Spec Cond:", specialConditions, "PastLimit:", tickAtrribLast.pastLimit, "Unreported:", tickAtrribLast.unreported)

    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float,
                         bidSize: Decimal, askSize: Decimal, tickAttribBidAsk):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize,
                                 askSize, tickAttribBidAsk)
        print("BidAsk. ReqId:", reqId,
              "Time:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d-%H:%M:%S"),
              "BidPrice:", floatMaxString(bidPrice), "AskPrice:", floatMaxString(askPrice), "BidSize:", decimalMaxString(bidSize),
              "AskSize:", decimalMaxString(askSize), "BidPastLow:", tickAttribBidAsk.bidPastLow, "AskPastHigh:", tickAttribBidAsk.askPastHigh)
        if reqId == 90 or reqId == '90':
            print(90)
            self.disconnect()
        
    def tickByTickMidPoint(self, reqId: int, time: int, midPoint: float):
        super().tickByTickMidPoint(reqId, time, midPoint)
        print("Midpoint. ReqId:", reqId,
              "Time:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d-%H:%M:%S"),
              "MidPoint:", floatMaxString(midPoint))

    def start(self):

        contract = Contract()
        contract.symbol = 'AAPL'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.secType = "STK"
        
        startDate = "20230308 10:30:00 US/Eastern"
        self.reqTickByTickData(1, contract, "BidAsk", numberOfTicks=0, ignoreSize=1)
        self.reqTickByTickData(2, contract, "BidAsk", numberOfTicks=0, ignoreSize=1)
        self.reqTickByTickData(3, contract, "BidAsk", numberOfTicks=0, ignoreSize=1)
        self.reqTickByTickData(4, contract, "BidAsk", numberOfTicks=0, ignoreSize=1)
        self.reqTickByTickData(5, contract, "BidAsk", numberOfTicks=0, ignoreSize=1)
        self.reqTickByTickData(6, contract, "BidAsk", numberOfTicks=0, ignoreSize=1)
        self.reqTickByTickData(7, contract, "BidAsk", numberOfTicks=0, ignoreSize=1)
        self.reqTickByTickData(8, contract, "BidAsk", numberOfTicks=0, ignoreSize=1)
        for i in range(9,70):
            self.reqTickByTickData(i, contract, "BidAsk", numberOfTicks=0, ignoreSize=1)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=1)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
