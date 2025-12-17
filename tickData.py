#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
import datetime
from ibapi.contract import (Contract, ContractDetails)
from ibapi.utils import Decimal, floatMaxString, decimalMaxString
from contracts import CustomContracts

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

    def historicalData(self, reqId, bar):
        super().historicalData(reqId, bar)
        #print("Historical data: ", reqId, bar.date, f"BID: {bar.open}", f"CLOSE: {bar.close}", f"{bar.wap}, time: {bar.date}")
        print(f"DATE {bar.date} --> OHLC: O: {bar.open} H: {bar.high} L: {bar.low} C: {bar.close}")
        self.historicalBars.append(bar)

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        if len(self.historicalBars) != 0:
            print("Writing bars...")
            with open(f'data/{reqId}data.txt', 'a') as file:
                file.write(f"{start}-{end}\n")
                file.write("BAR DATE   OPEN   HIGH    LOW\n")
                for bar in self.historicalBars:
                    file.write(string)
                file.write('\n')
                file.close()
                print("Finished writing bars")
        print("Historical data end for: ", reqId)
        print(f"Start: {start} - End: {end}")

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

        contract.secType = "STK"
        contract.conId = 76792991
        contract.currency = "USD"
        contract.symbol = "TSLA"
        contract.exchange = "SMART"
        
        self.reqTickByTickData(1, contract, "Last", numberOfTicks=50, ignoreSize=0)


    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        print(ibapi.__version__)
        app = TestApp()
        app.connect('127.0.0.1', 7496, clientId=1)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
