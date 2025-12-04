#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}

    def error(self, reqId: int, errorTime, errorCode: int, errorString: str,
              advansedOrderreject=''):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}, {errorTime}'
        print(error_message)

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print(contractDetails)

    def contractDetailsEnd(self, reqId):
        super().contractDetailsEnd(reqId)
        print("Contract details end for ", reqId)

    def bondContractDetails(self, reqId, contractDetails):
        super().bondContractDetails(reqId, contractDetails)
        print("Bond contract details: ", contractDetails)
        print("CUSIP: ", type(contractDetails.cusip), contractDetails.cusip)
        print("SecIdList: ", contractDetails.secIdList)

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId  # Snippet 1
        print("NVOID: ", self.nextValidOrderId)
        self.start()

    def openOrder(self, orderId, contract, order, orderState):
        print("Open Order: ", orderId, contract, order)
        print("Order State: ", orderState)
        self.stop()

    def orderStatus(self, orderId, status, filled, remaining,
                    avgFillPrice, permid, parentId, lastFillPrice,
                    clientId, whyHeld, mktCapPrice):
        print(f"Order Status: id: {orderId}, status: {status}," + \
              f"filled: {filled}, remaining: {remaining}," + \
              f"avgFillPrice: {avgFillPrice}, permid: {permid}," + \
              f"parentId: {parentId}, lastFillPrice: {lastFillPrice}," + \
              f"clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def placeSampleOrder(self):

        fordContract = Contract()

        fordContract.exchange = "SMART"
        fordContract.secType = "STK"
        fordContract.symbol = "F"
        fordContract.currency = "USD"

        order = Order()

        order.orderType = "MKT"
        order.action = "BUY"
        order.totalQuantity = 1
        order.tif = "GTC"
        order.whatIf = True
        order.outsideRth = True

        oid = self.nextValidOrderId
        self.reqContractDetails(oid, fordContract)
        self.placeOrder(oid, fordContract, order)

    def start(self):
        oid = self.nextValidOrderId
        print("Next order id: ", oid)
        self.placeSampleOrder()


    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('127.0.0.1', 7496, clientId=4)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        #        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
