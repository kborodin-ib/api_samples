#! /usr/bin/env python3

import sys
import logging
import ibapi
import time
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.execution import Execution
from ibapi.order import Order
import logging 
from contracts import CustomContracts
from ibapi.utils import floatMaxString, decimalMaxString

#logging.basicConfig(
#                level = logging.INFO,
#                format = '%(asctime)s - %(levelname)s - %(message)s',
#                datefmt='%Y-%m-%d %H:%M:%S'
#                )

#logger = logging.getLogger(__name__)

class TestApp(EWrapper, EClient):


    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.priceTicks = 0

    def error(self, reqId: int, errorCode: int, errorString: str,
              advancedOrderRejectJson=''):
        super().error(reqId, errorCode, errorString, advancedOrderRejectJson='')
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'
        print(errorCode, error_message)

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print(contractDetails)

    def contractDetailsEnd(self, reqId):
        super().contractDetailsEnd(reqId)
        print("Contract details end for ", reqId)

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId # Snippet 1
        print("NVOID: ", self.nextValidOrderId)
        self.start()

    def openOrder(self, orderId, contract, order, orderState):
        print("Open Order: ", orderId, contract, order)

    def orderStatus(self, orderId, status, filled, remaining,
            avgFillPrice, permid, parentId, lastFillPrice, 
            clientId, whyHeld, mktCapPrice):
        print(f"Order Status: id: {orderId}, status: {status}," +\
                f"filled: {filled}, remaining: {remaining}," +\
                f"avgFillPrice: {avgFillPrice}, permid: {permid}," +\
                f"parentId: {parentId}, lastFillPrice: {lastFillPrice}," +\
                f"clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def tickPrice(self, reqId, tickType, price: float,
                  attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print(f"Tick n {self.priceTicks}", "TickPrice. TickerId:", reqId, "tickType:", tickType,
              "Price:", floatMaxString(price), "CanAutoExecute:", attrib.canAutoExecute,
              attrib.preOpen)
        self.priceTicks += 1
        if self.priceTicks == 200:
            self.startPlacingOrders()


    def tickSize(self, reqId, tickType, size):
        super().tickSize(reqId, tickType, size)
#        print("TickSize. TickerId:", reqId, "TickType:", tickType, "Size: ", decimalMaxString(size))
    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("contract details: ", reqId, contractDetails)

    def startPlacingOrders(self):

        mycontract = CustomContracts().mnqContract()
        order = Order()
        order.action = 'SELL'
        order.totalQuantity = 1
        order.orderType = 'LMT'
        order.lmtPrice = 20 
        order.outsideRth = True

        oid = self.nextValidOrderId
        for i in range(41):
            self.placeOrder(oid, mycontract, order)
            oid += 1


    def start(self):
        mycontract = CustomContracts().mnqContract()
        self.reqMktData(
            reqId=self.clientId,
            contract=mycontract,
            genericTickList="",
            snapshot=False,
            regulatorySnapshot=False,
            mktDataOptions=[],
        )

        

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        cid = sys.argv[1]
        app = TestApp()
        app.connect('172.22.21.200', 7496, clientId=cid)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
