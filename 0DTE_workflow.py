#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_cancel import OrderCancel
from ibapi.contract import ComboLeg
from ibapi.tag_value import TagValue
import logging
from datetime import datetime

#logging.basicConfig(
#    level=logging.INFO,
#    format='%(asctime)s - %(levelname)s - %(message)s',
#    datefmt='%Y-%m-%d %H:%M:%S'
#)
#logger = logging.getLogger(__name__)

ACCOUNTS = ["DU74649", "DU74650"]
TODAY = datetime.now().strftime("%Y%m%d")
ORDER_CANCEL = OrderCancel()

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
      # A hashmap to store open orders 
        self.multilegs = {}

    def error(self, reqId: int, errorTime, errorCode: int, errorString: str,
              advansedOrderreject=''):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}, {errorTime}'
        print(error_message)

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
      # Here contracts are updated with expiration date so we can further compare it against current date
        for k in self.multilegs.keys():
            if contractDetails.contract.conId == self.multilegs[k].conId:
                self.multilegs[k].lastTradeDateOrContractMonth = contractDetails.contract.lastTradeDateOrContractMonth

    def contractDetailsEnd(self, reqId):
        super().contractDetailsEnd(reqId)
        print("Contract details end for ", reqId)
      # Once all contracts were updated - we can compare dates and cancel those orders that have 0DTE contracts as legs
        for k in self.multilegs:
            print("OrderID: ", k)
            if self.multilegs[k].lastTradeDateOrContractMonth == TODAY:
                self.cancelOrder(int(k), ORDER_CANCEL)

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId  # Snippet 1
        self.start()

    def createFOPContract(self, conid, exchange, currency):

        contract = Contract()

        contract.conId = conid
        contract.exchange = exchange
        contract.secType = "FOP"
        contract.currency = currency

        return contract

    def openOrder(self, orderId, contract, order, orderState):
        contractToCheck = Contract()
      # Initially all combo orders are added to hashmap here
        for i in range(len(contract.comboLegs)):
            contractToCheck = self.createFOPContract(contract.comboLegs[i].conId,
                                                     contract.comboLegs[i].exchange, contract.currency)
            self.multilegs[str(orderId)] = contractToCheck

    def openOrderEnd(self):
      # Once all open orders are sent - we would need to update contract details in hashmap to include expiration dates
        for key in self.multilegs.keys():
            print(type(self.multilegs[key]))
            storedContracts = self.multilegs[key]

            fopContract = self.createFOPContract(storedContracts.conId,
                                                 storedContracts.exchange,
                                                 storedContracts.currency)
            self.reqContractDetails(1, contract=fopContract)


    def placeSampleOrder(self,oid):

        mycontract = Contract()
        mycontract.symbol = "ES"
        mycontract.secType = "BAG"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"

        leg1 = ComboLeg()
        leg1.conId = 828072800  # 3845
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "CME"

        leg2 = ComboLeg()
        leg2.conId = 828072981  # 3855
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "CME"

        mycontract.comboLegs = []
        mycontract.comboLegs.append(leg1)
        mycontract.comboLegs.append(leg2)

        myorder = Order()
        myorder.orderId = oid
        myorder.action = "BUY"
        myorder.orderType = "REL+LMT"
        myorder.totalQuantity = 1
        myorder.smartComboRoutingParams = []
        myorder.smartComboRoutingParams.append(TagValue("NonGuaranteed", "1"))
        myorder.orderComboLegs = []
        myorder.lmtPrice = 6000

        print("NEW ORDER ID: ", oid)
        for acc in ACCOUNTS:
            myorder.account = acc
            print(f"{myorder.account} - {myorder}")
            self.placeOrder(oid, mycontract, myorder)
            oid += 1

    def start(self):
        oid = self.nextValidOrderId
        self.placeSampleOrder(oid)
        self.reqOpenOrders()



    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
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
