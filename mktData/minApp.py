#! /usr/bin/env python3

import logging
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.execution import Execution

print(Execution.mro())
exec = Execution()

print(exec.__dict__)

logging.basicConfig(
                level = logging.INFO,
                format = '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
                )

logger = logging.getLogger(__name__)

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}

    def error(self, reqId: int, errorCode: int, errorString: str, errorTime: str,
              advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'
        print(error_message)
       
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId # Snippet 1
        print(self.nextValidOrderId)
        self.start()

    def tickPrice(self, reqId, tickType, price: float,
                  attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if tickType == "4":
            print("TickPrice. TickerId:", reqId, "tickType:", tickType,
                      "Price:", price, "CanAutoExecute:", attrib.canAutoExecute,
                      attrib.preOpen)

    def start(self):
        contract = Contract()

        contract.symbol = "BHP"
        contract.exchange = "ASX"
        contract.currency = "AUD"
        contract.secType = "STK"

        self.reqMarketDataType(3)
        self.reqMktData(1, contract, '', False, False, [])

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('127.0.0.1', 7496, clientId=3)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
