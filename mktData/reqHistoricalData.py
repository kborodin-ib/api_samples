#! /usr/bin/env python3

import logging
import datetime
import time
import pytz
import ibapi
from threading import Timer
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from datetime import datetime
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
        print("Historical data: ", reqId, bar.date, f"BID: {bar.open}", f"CLOSE: {bar.close}", f"{bar.wap}", type(bar)) 
        self.historicalBars.append(bar)

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        if len(self.historicalBars) != 0:
            print("Writing bars...")
            with open(f'data/{reqId}data.txt', 'a') as file:
                file.write(f"{start}-{end}\n")
                file.write("BAR DATE   OPEN   HIGH    LOW\n")
                for bar in self.historicalBars:
                    string = f"{bar.date}, {bar.open}, {bar.high}, {bar.low}\n"
                    file.write(string)
                file.write('\n')
                file.close()
                print("Finished writing bars")
        print("Historical data end for: ", reqId)
        print(f"Start: {start} - End: {end}")
        self.disconnect()
    
    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("contract details: ", reqId, contractDetails.contract.conId)

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def headTimestamp(self, reqId, headTimeStamp):
        print("HeadTimeStamp: ", headTimeStamp)

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

    def setTimeZone(timezone):
        endTime = datetime(2024, 3, 26, 16, 15, 0, 0, pytz.timezone('America/New_York'))
        endTimeString = endTime.astimezone(pytz.UTC).strftime('%Y%m%d-%H:%M:%S')
        return endTimeString


    def start(self):
        # TWS will retunr data only for instrument's timezone or 
        # for time zone that is configured as local in TWS settings.
        contract = CustomContracts().aaplContract()
        print(contract)
        self.reqContractDetails(self.nextValidOrderId, contract)
        endDate = "20240404 12:00:00 US/Eastern"
        endDate = ""
        self.reqHeadTimeStamp(self.nextValidOrderId, contract, "TRADES", True,
                1)
        print(f"END DATE: ", endDate)
        self.reqHistoricalData(self.nextValidOrderId, contract, endDate, 
                '6 M', '1 day', 'ADJUSTED_LAST', 1, 1, False, [])

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
