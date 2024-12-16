#! /usr/bin/env python3

import logging
import datetime
import time
from threading import Timer
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from datetime import datetime, timedelta
from threading import Thread
from contracts import CustomContracts 


class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.historicalBars = []

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject=''):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    def historicalData(self, reqId, bar):
        super().historicalData(reqId, bar)
        print(bar)
        self.historicalBars.append(bar)

    def historicalDataUpdate(self, reqId, bar):
        super().historicalDataUpdate(reqId, bar)
        print(f"UPDATE! {bar}")

    def getNext40days(self, end):
        if " US/Central" in end:
            endDate = end.rstrip(" US/Central")

        if " US/Eastern" in end:
            endDate = end.rstrip(" US/Eastern")

        date = datetime.strptime(endDate, "%Y%m%d %H:%M:%S")
        newDate = date - timedelta(days=40) 
        strNewDate = newDate.strftime("%Y%m%d %H:%M:%S US/Central")
        return strNewDate 

    def getTimeBetweenDateAndBar(self, end, barDate):
        endDate = end.rstrip(' US/Eastern')
        barDate = barDate.date.rstrip(' US/Eastern')
        edate = datetime.strptime(endDate, "%Y%m%d %H:%M:%S")
        bdate = datetime.strptime(barDate, "%Y%m%d %H:%M:%S")

        difference = edate - bdate

        return difference

    def writeData(self):
        if len(self.historicalBars) != 0:
            with open(f'sampleData.txt', 'a') as file:
                for bar in self.historicalBars:
                    string = f"Date: {bar.date}, O: {bar.open}, H: {bar.high}, L: {bar.low}, C {bar.close}\n"
                    file.write(string)
                file.write('\n')
                file.close()
                print("Finished writing bars")

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        #TODO: crop timezone id into separate string.
        #TODO: format bar date time to more human readable form
        print("End of static data")
        self.writeData()
        self.disconnect()

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("contract details: ", reqId, contractDetails)

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def headTimestamp(self, reqId, headTimeStamp):
        print("HeadTimeStamp: ", headTimeStamp)

    def convert_unix_timestamp(self, stamp):
        print(stamp)
        ts = int(stamp)
        print(datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"))
        
    def historicalTicksBidAsk(self, reqId: int, ticks,
                              done: bool):
        for tick in ticks:
            self.convert_unix_timestamp(tick.time)
            print("HistoricalTickBidAsk. ReqId:", reqId, tick)

    def historicalTicksLast(self, reqId: int, ticks,
                            done: bool):
        for tick in ticks:
            self.convert_unix_timestamp(tick.time)
            print("HistoricalTickLast. ReqId:", reqId, tick)


    def start(self):
        # TWS will retunr data only for instrument's timezone or 
        # for time zone that is configured as local in TWS settings.
        contract = CustomContracts().spxIndContract()
        self.reqContractDetails(self.nextValidOrderId, contract)
        endDate = ""
        self.reqHeadTimeStamp(self.nextValidOrderId, contract, "BID_ASK", True,
                1)

        self.nextValidOrderId += 1 
        self.reqHistoricalData(self.nextValidOrderId, contract, endDate, 
                '1 D', '30 mins', 'TRADES', 1, 1, True, [])

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('172.22.21.200', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
