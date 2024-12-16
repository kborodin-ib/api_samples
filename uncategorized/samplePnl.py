#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import (Contract, ContractDetails)
from ibapi.utils import floatMaxString, decimalMaxString

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    # WRAPPERS HERE
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        #logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        # As soon as next valid id is received it is safe to send requests
        self.start()

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)
        print(contractDetails)
        
    def pnl(self, reqId: int, dailyPnL: float,
            unrealizedPnL: float, realizedPnL: float):
        super().pnl(reqId, dailyPnL, unrealizedPnL, realizedPnL)
        print("Daily PnL. ReqId:", reqId, "DailyPnL:", floatMaxString(dailyPnL),
              "UnrealizedPnL:", floatMaxString(unrealizedPnL), "RealizedPnL:", floatMaxString(realizedPnL))
    
    # Place requests here
    def start(self):

        contract = Contract()
        contract.symbol = 'AAPL'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.secType = "STK"

        # Add values here
        accId = ''

        self.reqContractDetails(self.nextValidOrderId, contract)
        self.reqPnl(self.nextValidOrderId, accId, "") 

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('127.0.0.1', 7497, clientId=1)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
