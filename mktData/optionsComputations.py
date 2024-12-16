#! /usr/bin/env python3

import logging
import ibapi
import time
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from contracts import CustomContracts


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

    def error(self, reqId: int, errorCode: int, errorString: str,
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

    def tickOptionComputation(self, reqId, tickType, tickAttrib,
                              impliedVol, delta, optPrice, pvDivident,
                              gamma, vega, theta, undPrice):
        super().tickOptionComputation(reqId, tickType, tickAttrib,
                                  impliedVol, delta, optPrice, pvDivident,
                                  gamma, vega, theta, undPrice)
        print(delta, vega, gamma)

    def start(self):
        contract = CustomContracts().amdOption()
        self.reqMktData(self.nextValidOrderId, contract, "", False, False, [])
#        self.calculateOptionPrice(self.nextValidOrderId, contract, .2, 159.6, [])


    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
