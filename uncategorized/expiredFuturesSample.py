#! /usr/bin/env python3

import logging
import datetime
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString, Decimal
from contracts import CustomContracts

def futContract(symbol, exchange, currency, lastTradeDate):

    contract = Contract()

    contract.symbol = symbol # HSI
    contract.secType = "FUT"
    contract.exchange = exchange # HKFE
    contract.currency = currency # HKD
#    contract.lastTradeDateOrContractMonth = lastTradeDate # "20231129"
    contract.includeExpired = True

    return contract

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")


    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print(f"Conid: {contractDetails.contract.conId} - Expiration: {contractDetails.contract.lastTradeDateOrContractMonth}")


    def start(self):
        contract = futContract(symbol="HSI", exchange="HKFE", 
                currency="HKD", lastTradeDate="20231129")
        contract = CustomContracts().mbtkContract()
        print(contract)
        self.reqContractDetails(self.nextValidOrderId, contract)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=1)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
