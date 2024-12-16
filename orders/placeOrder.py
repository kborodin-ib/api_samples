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
from stopLimitOrder import stopLimitOrder
import logging 
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

    def openOrder(self, orderId, contract, order, orderState):
        print("Open Order: ", orderId, contract, order)
        self.attachStopLoss(orderId, order=order, contract=contract)

    def orderStatus(self, orderId, status, filled, remaining,
            avgFillPrice, permid, parentId, lastFillPrice, 
            clientId, whyHeld, mktCapPrice):
        print(f"Order Status: id: {orderId}, status: {status}," +\
                f"filled: {filled}, remaining: {remaining}," +\
                f"avgFillPrice: {avgFillPrice}, permid: {permid}," +\
                f"parentId: {parentId}, lastFillPrice: {lastFillPrice}," +\
                f"clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def attachStopLoss(self, parentOid, contract, order):
        stopLoss = Order()
        stopLoss.orderId = parentOid + 2
        stopLoss.action = "SELL" if order.action == "BUY" else "BUY"
        stopLoss.orderType = "STP"
        #Stop trigger price
        stopLoss.auxPrice = order.price + 10 
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
        
        for order in orders:
            self.placeOrder(orderid, contract, order)

    def start(self):

        contract = Contract()

#        contract.conId = "645927982"
#        contract.exchange = "VALUE"
#        contract.currency = "USD"
#        contract.secType = 'STK'

        bmwContract = Contract()
        bmwContract.symbol = 'PXDT'
        bmwContract.secType = 'STK'
        bmwContract.exchange = 'SMART'
        bmwContract.currency = 'USD'
        bmwContract.primaryExchange = 'VALUE'
        bmwContract.localSymbol = 'PXDT'
        bmwContract.conId = '645927982'
        bmwContract.tradingClass = 'SCM'


#        aaplContract = Contract()
#        aaplContract.symbol = 'AAPL'
#        aaplContract.exchange = 'SMART'
#        aaplContract.currency = 'USD'
#        aaplContract.secType = 'STK'
        contract = Contract()
        contract.secIdType = 'ISIN'
        contract.secId = 'US0378331005'
        contract.exchange = 'SMART'
        contract.symbol = "AAPL"
#        self.reqContractDetails(self.nextValidOrderId, bmwContract)
        
        mycontract = CustomContracts().mnqContract()
        order = Order()
        order.action = 'SELL'
        order.totalQuantity = 1
        order.orderType = 'STP LMT'
        # Limit and stop must be within 2 percent of current market price
        order.lmtPrice = 20 
        order.auxPrice = 10 
        order.outsideRth = True

        oid = self.nextValidOrderId
        accounts = ['DU74649', 'DU74650']
        self.placeOrder(oid, contract, order)
#        while True:
#            self.placeOrder(oid, mycontract, order)
#            oid += 1

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
