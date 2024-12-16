#! /usr/bin/env python3

import ibapi
from ibapi.client import * 
from ibapi.wrapper import * 
from ibapi.contract import Contract
import datetime
import threading
datetime.datetime.now()
port = 7496


class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        print(f"next oid: {orderId}")
        self.start() 

    def historicalDataUpdate(self, reqId: int, bar):
        super().historicalDataUpdate(reqId, bar)
        print("histUpdate.", reqId, bar)

    def historicalData(self, reqId: int, bar):
        super().historicalData(reqId, bar)
        print(reqId, bar)
        # print(bar.date)


    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print(reqId, start, end)
    #    self.disconnect()

    def start(self):

        mycontract = Contract()
        mycontract.exchange = "CBOE"
        mycontract.secType ="IND"
        mycontract.symbol ="SPX"
        mycontract.currency = "USD"

        self.reqHistoricalData(
        reqId=123,
        contract=mycontract,
        endDateTime="",
        #endDateTime="",
        #endDateTime=datetime.datetime. now().strftime("%Y%m%d %H:%M:%S"),
        durationStr="1 D",
        barSizeSetting = "30 mins",
        whatToShow= "TRADES",#"TRADES",
        useRTH=1,
        formatDate=1,
        keepUpToDate=True,
        chartOptions=[],
        )


    def error(self, reqId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        super().error(reqId, errorCode, errorString, advancedOrderRejectJson="")
        print(reqId, errorCode, errorString, advancedOrderRejectJson)

if __name__ == '__main__':
    app = TestApp()
    app.connect("172.22.21.200", port, 1)
    print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
    print(f'ibapi version: {ibapi.__version__}')
    app.run()
