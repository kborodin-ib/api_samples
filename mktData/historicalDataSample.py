#! /usr/bin/env python3

import ibapi
import logging
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from contracts import CustomContracts


class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
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
        super().historicalDataEnd(reqId, start, end)
        print("Historical data end for: ", self.clientId)

    def headTimestamp(self, reqId, headTimestamp):
        print("HeadTimeStamp: ", headTimestamp)

    def start(self):

        contract = Contract()

        contract.secType = 'STK'
        contract.currency = 'USD'
        contract.exchange = 'NASDAQ'
        contract.symbol = 'SMCI'

#        endDate = '20231113 11:15:00 US/Eastern' 
        endDate =""
        self.reqHeadTimeStamp(self.nextValidOrderId, contract, whatToShow="TRADES", useRTH=True, formatDate=1)
        self.reqContractDetails(self.nextValidOrderId, contract)
        self.reqHistoricalData(self.nextValidOrderId, contract, endDate, 
                '1 M', '1 min', 'MIDPOINT', 0, 1, False, [])

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.0.106', 7496, clientId=1)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
