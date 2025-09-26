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


#logging.basicConfig(
 #               level = logging.INFO,
 #               format = '%(asctime)s - %(levelname)s - %(message)s',
 #               datefmt='%Y-%m-%d %H:%M:%S'
#                )
#
# logger = logging.getLogger(__name__)

class TestApp(EWrapper, EClient):


    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}

    def error(self, reqId: int, errorCode: int, errorString: str, errorTime,
              advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error time: {errorTime}, Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'
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
        self.nextValidOrderId = orderId # Snippet 1
        print("NVOID: ", self.nextValidOrderId)
        self.start()

 #   def openOrder(self, orderId, contract, order, orderState):
 #       print("Open Order: ", orderId, contract, order)
  #      self.attachStopLoss(orderId, order=order, contract=contract)

 #  def orderStatus(self, orderId, status, filled, remaining,
  #          avgFillPrice, permid, parentId, lastFillPrice,
  #          clientId, whyHeld, mktCapPrice):
   #     print(f"Order Status: id: {orderId}, status: {status}," +\
   #             f"filled: {filled}, remaining: {remaining}," +\
   #             f"avgFillPrice: {avgFillPrice}, permid: {permid}," +\
   #             f"parentId: {parentId}, lastFillPrice: {lastFillPrice}," +\
    #            f"clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def attachStopLoss(self, parentOid, contract, order):
        stopLoss = Order()
        stopLoss.orderId = parentOid + 2
        stopLoss.action = "SELL" if order.action == "BUY" else "BUY"
        stopLoss.orderType = "STP"
        #Stop trigger price
   #     stopLoss.auxPrice = order.price + 10
        stopLoss.totalQuantity = 1 
        stopLoss.parentId = parentOid 
        #In this case, the low side order will be the last child being sent. Therefore, it needs to set this attribute to True
        #to activate all its predecessors
        stopLoss.trailingPercent = 10
        stopLoss.percentOffset = 12
        stopLoss.transmit = True
        self.placeOrder

    def placeAdjustedOrder(self):

        contract = Contract()

        contract.symbol = "SSUN"
        contract.exchange = "SMART"
        contract.currency = "CHF"
        contract.secType = 'STK'

        order = Order()

        order.action = 'BUY'
        order.orderType = 'MKT'
        order.totalQuantity = 1
        order.auxPrice = 108.55
        order.hidden = True
        order.tif = 'DAY'
        order.advancedErrorOverride="EUROWARN4LIQ"

#        adjusted = Order()
#        adjusted.parentId = order.orderId
#        adjusted.orderId = order.orderId + 1
#        adjusted.action = "BUY"
#        adjusted.tif = "DAY"
#        adjusted.totalQuantity = 2
#        adjusted.triggerPrice = 175
#        adjusted.adjustedOrderType = "TRAIL LMT"
#        adjusted.adjustedStopLimitPrice = 105.6
#        adjusted.lmtPriceOffset = 1
#        adjusted.auxPrice = 3

        orderid = self.nextValidOrderId()

        self.placeOrder(orderid, contract, order)

    def placePegBest(self, oid):

        contract1 = Contract()

        contract1.symbol = "AAPL"
        contract1.exchange = "SMART"
        contract1.conId = 265598

        contract2 = Contract()

        contract2.symbol = "MSFT"
        contract2.exchange = "SMART"
        contract2.conId = 272093

        order = Order()
        order.orderType = "LMT"
        order.action = "BUY"
        order.lmtPrice = 221.02
        order.outsideRth = True
        order.totalQuantity = 1000

        lmtOrder = Order()

        lmtOrder.orderType = "LMT"
        lmtOrder.action = "BUY"
        lmtOrder.lmtPrice = 520.60
        lmtOrder.outsideRth = True
        lmtOrder.totalQuantity = 1000
        lmtOrder.tif = "OVERNIGHT + DAY"

        self.placeOrder(oid, contract1, order)
        oid += 1
        self.placeOrder(oid, contract2, lmtOrder)

    def placeSampleOrder(self):

        contract = Contract()

        contract.conid = 265598
        contract.secType = "STK"
        contract.exchange = "OVERNIGHT"
        contract.primaryExchange = "NASDAQ"
        contract.symbol = "AAPL"
        contract.currency = "USD"

        order = Order()

        order.orderType = "LMT"
        order.lmtPrice = 240.69
        order.totalQuantity = 1
   #     order.tif = "OVERNIGHT + DAY"
        order.action = "BUY"

        oid = self.nextValidOrderId
        self.placeOrder(oid, contract, order)

    def start(self):

        oid = self.nextValidOrderId
       # accounts = ['DU74649', 'DU74650']
        self.placeSampleOrder()
        self.reqIds(-1)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        cid = 0
        app = TestApp()
        app.connect('127.0.0.1', 7496, clientId=cid)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
