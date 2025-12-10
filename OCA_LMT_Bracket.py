#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
import logging
import time

def loggingConfig():
    
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

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId # Snippet 1
        print("NVOID: ", self.nextValidOrderId)
        self.start()

    def openOrder(self, orderId, contract, order, orderState):
        print("Open Order: ", orderId, contract, order)
        print("Order State: ", orderState)

    def orderStatus(self, orderId, status, filled, remaining,
            avgFillPrice, permid, parentId, lastFillPrice,
            clientId, whyHeld, mktCapPrice):
        print(f"Order Status: id: {orderId}, status: {status}," +\
                f"filled: {filled}, remaining: {remaining}," +\
                f"avgFillPrice: {avgFillPrice}, permid: {permid}," +\
                f"parentId: {parentId}, lastFillPrice: {lastFillPrice}," +\
                f"clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")


    def create_OCA_bracket(self, oid):

        # Entry Order 1
        entry1 = Order()
        entry1.orderId = oid
        entry1.action = "BUY"
        entry1.orderType = "LMT"
        entry1.totalQuantity = 1
        entry1.lmtPrice = 50.00
        entry1.ocaGroup = "test1"
        entry1.ocaType = 1  # Cancel all on fill
        entry1.transmit = False  # Don't transmit until all orders are ready

        # Profit Target for Entry 1
        profit1 = Order()
        profit1.orderId = oid + 1
        profit1.action = "SELL"
        profit1.orderType = "LMT"
        profit1.totalQuantity = 1
        profit1.lmtPrice = 29
        profit1.parentId = entry1.orderId  # Links to Entry Order 1
        profit1.ocaType = 1
        profit1.transmit = False

        # Stop Loss for Entry 1
        stop1 = Order()
        stop1.orderId = oid + 2
        stop1.action = "SELL"
        stop1.orderType = "STP"
        stop1.totalQuantity = 1
        stop1.auxPrice = 29  # Stop price
        stop1.parentId = entry1.orderId  # Links to Entry Order 1
        stop1.ocaType = 1
        stop1.transmit = False

        # Entry Order 2
        entry2 = Order()
        entry2.orderId = oid + 3
        entry2.action = "BUY"
        entry2.orderType = "LMT"
        entry2.totalQuantity = 100
        entry2.lmtPrice = 145.00
        entry2.ocaGroup = "test1"  # Same OCA as Entry 1
        entry2.ocaType = 1
        entry2.transmit = False

        # Profit Target for Entry 2
        profit2 = Order()
        profit2.orderId = oid + 4
        profit2.action = "SELL"
        profit2.orderType = "LMT"
        profit2.totalQuantity = 100
        profit2.lmtPrice = 150.00
        profit2.parentId = entry2.orderId  # Links to Entry Order 2
        profit2.ocaType = 1
        profit2.transmit = False

        # Stop Loss for Entry 2
        stop2 = Order()
        stop2.orderId = oid + 5
        stop2.action = "SELL"
        stop2.orderType = "STP"
        stop2.totalQuantity = 100
        stop2.auxPrice = 143.00
        stop2.parentId = entry2.orderId  # Links to Entry Order 2
        stop2.ocaType = 1
        stop2.transmit = True  # Transmit the entire order chain


        return [entry1, profit1, stop1, entry2, profit2, stop2]

    def place_OCA_bracket(self):

        contract = Contract()

        contract.symbol = "AAPL"
        contract.exchange = "SMART"
        contract.secType = "STK"
        contract.currency = "USD"

        oid = self.nextValidOrderId

        OCA_orders = self.create_OCA_bracket(oid)

        for o in OCA_orders:
            print(o.ocaGroup, o.orderId, o.parentId)
            self.placeOrder(o.orderId, contract, o)
            time.sleep(1)

    def start(self):
        self.place_OCA_bracket()

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        cid = 0
        app = TestApp()
        app.connect('127.0.0.1', 7496, clientId=5)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
