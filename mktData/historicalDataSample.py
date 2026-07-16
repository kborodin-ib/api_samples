#! /usr/bin/env python3

import ibapi
import logging
import threading
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from contracts import testContracts 


class TestApp(EWrapper, EClient):

    def __init__(self, timeout=10):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.timeout = timeout
        self._timers = {}

    # TIMEOUT HANDLERS

    def _on_timeout(self, reqId):
        print(f"ReqId: {reqId} | TIMEOUT - cancelling historical data request")
        self.cancelHistoricalData(reqId)
        self._timers.pop(reqId, None)

    def _start_timer(self, reqId):
        timer = threading.Timer(self.timeout, self._on_timeout, args=[reqId])
        timer.daemon = True
        self._timers[reqId] = timer
        timer.start()

    def _cancel_timer(self, reqId):
        timer = self._timers.pop(reqId, None)
        if timer:
            timer.cancel()

    # WRAPPERS HERE

    def error(self, reqId: int,errorTime, errorCode: int, errorString: str,
            advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        if reqId != -1:
            self._cancel_timer(reqId)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("contract details: ", reqId, contractDetails)

    def historicalData(self, reqId, bar):
        super().historicalData(reqId, bar)
        print("Historical data: ", reqId, bar)

    def historicalDataEnd(self, reqId, start, end):
        self._cancel_timer(reqId)
        super().historicalDataEnd(reqId, start, end)
        print("Historical data end for: ", self.clientId)

    def headTimestamp(self, reqId, headTimestamp):
        print("HeadTimeStamp: ", headTimestamp)

    def request_historical_data(self, reqId, contract, endDateTime, 
        durationString, barSizeSetting, whatToShow, useRTH):
        self._start_timer(reqId)
        self.reqHistoricalData(
            reqId = reqId,
            contract = contract,
            endDateTime = endDateTime,
            durationStr = durationString,
            barSizeSetting = barSizeSetting,
            whatToShow = whatToShow,
            useRTH = useRTH,
            formatDate = 1,
            keepUpToDate = False,
            chartOptions = []
        )

    def start(self):

        contract = Contract()

        contract.secType = 'STK'
        contract.symbol = 'APLZ'
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.primaryExchange = "AMEX"

        endDate = '20250925 16:59:00 US/Eastern' 
#        endDate =""
        self.reqHeadTimeStamp(self.nextValidOrderId, contract, whatToShow="TRADES", useRTH=True, formatDate=1)
        self.reqContractDetails(self.nextValidOrderId, contract)
        self.request_historical_data(self.nextValidOrderId, contract, endDate, 
                '5 D', '1 day', 'TRADES', 1)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('172.23.208.1', 7496, clientId=1)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
