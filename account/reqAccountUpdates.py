#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import (Contract, ContractDetails)
from ibapi.utils import decimalMaxString, intMaxString, floatMaxString, Decimal
from contracts import CustomContracts 
import sys

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}
        self.contract = None

    # WRAPPERS HERE
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        #logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        # As soon as next valid id is received it is safe to send requests
        self.start()
        
    def updateAccountValue(self, key: str, val: str, currency: str,
                           accountName: str):
        super().updateAccountValue(key, val, currency, accountName)
        # Dumb idea becaues keys are not unique, cashBalance + currency should be a key
        self.dataframe[key] = val
        print(key, val, currency, accountName)
    # ! [updateaccountvalue]

    # ! [updateportfolio]
#    def updatePortfolio(self, contract: Contract, position: Decimal,
#                        marketPrice: float, marketValue: float,
#                        averageCost: float, unrealizedPNL: float,
#                        realizedPNL: float, accountName: str):
#        super().updatePortfolio(contract, position, marketPrice, marketValue,
#                                averageCost, unrealizedPNL, realizedPNL, accountName)
#        print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",
#              contract.exchange, "Position:", decimalMaxString(position), "MarketPrice:", floatMaxString(marketPrice),
#              "MarketValue:", floatMaxString(marketValue), "AverageCost:", floatMaxString(averageCost),
#              "UnrealizedPNL:", floatMaxString(unrealizedPNL), "RealizedPNL:", floatMaxString(realizedPNL),
#              "AccountName:", accountName)
    # ! [updateportfolio]

    # ! [updateaccounttime]
    def updateAccountTime(self, timeStamp: str):
        super().updateAccountTime(timeStamp)
        print("UpdateAccountTime. Time:", timeStamp)
    # ! [updateaccounttime]

    # ! [accountdownloadend]
    def accountDownloadEnd(self, accountName: str):
        super().accountDownloadEnd(accountName)
        print("AccountDownloadEnd. Account:", accountName)
        if len(self.dataframe) != 0:
            with open('outfile.txt', 'w') as file:
                for key, value in self.dataframe.items():
                    file.write(f"{key}: {value}\n")
            print("DATAFRAME: ", self.dataframe)
#        self.reqAccountUpdates(False, "DU6036902")
    # ! [accountdownloadend]

    def accountSummary(self, reqId, account, tag, value, currency):
        super().accountSummary(reqId, account, tag, value, currency)
        print(f"AccountSummary\nReqId: {reqId}\nAccount: {account}\nTag: {tag}\nValue: {value}") 
    
    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float, size, tickAtrribLast, exchange: str,specialConditions: str):
          print(" ReqId:", reqId, "Time:", time, "Price:", floatMaxString(price), "Size:", size, "Exch:" , exchange, "Spec Cond:", specialConditions, "PastLimit:", tickAtrribLast.pastLimit, "Unreported:", tickAtrribLast.unreported)

    def accountSummaryEnd(self, reqId):
        super().accountDownloadEnd(reqId)
        print("account summary end for: ", reqId)

    def start(self):

        contract = Contract()

        contract = Contract()
        contract.symbol = "LHV1T"
        contract.secType = "STK"
        contract.exchange = "N.TALLINN"
        contract.currency = "EUR"
        self.reqAccountUpdates(True, "DU6036902")
#        self.reqTickByTickData(self.nextValidOrderId, contract, "AllLast", 0, True)
#        self.reqAccountSummary(self.nextValidOrderId, 'All', 'DayTradesRemaining,Leverage,NetLiquidation')

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=0)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
