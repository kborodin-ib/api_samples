#! /usr/bin/env python3

from ibapi.contract import Contract
from ibapi.contract import ComboLeg


class CustomContracts():

    def __init__(self):
        self.args = ""

    def spxIndContract(self):

        mycontract = Contract()
        mycontract.exchange = "CBOE"
        mycontract.secType ="IND"
        mycontract.symbol ="SPX"
        mycontract.currency = "USD"
        
        return mycontract 
    
    def gbpContract(self):
        
        contract = Contract()
        contract.conId = 12087811

        return contract

    def cboeContract(self):

        contract = Contract()

        contract.exchange = "CBOE"
        contract.secType = "IND"
        contract.symbol = "SPX"
        contract.currency = "USD"

        return contract

    def aaplOptionContract(self):

        contract = Contract()

        contract.secType = "OPT"
        contract.symbol = "AAPL"
        contract.lastTradeDateOrContractMonth = "20241115"
        contract.strike = 225
        contract.currency = "USD"
        contract.right = "C"
        contract.multiplier = 100
        contract.tradingClass = "AAPL"
        contract.exchange = "SMART"
        contract.conid = 682678216

        return contract

    def ibust100(self):

        contract = Contract()

        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.secType = "CFD"
        contract.symbol = "IBUST100"

        return contract

    def estx50contract(self):

        contract = Contract()

#        contract.conId = 595139153
        contract.symbol = "ESTX50"
        contract.secType = "OPT"
        contract.lastTradeDateOrContractMonth = "20231215"
        contract.strike = 4325
        contract.right = "C"
        contract.multiplier = 10
        contract.exchange = "EUREX"
        contract.currency = "EUR"
        contract.localSymbol = "C OESX 20231215 4325 M"

        return contract
    
    def aaplContract(self):

        contract = Contract()
        contract.conId = 265598
        contract.exchange = "SMART"
        contract.symbol = "AAPL"

        return contract

    def eurUsdContract(self):

        contract = Contract()

        contract.exchange = "IDEALPRO"
        contract.symbol = "EUR"
        contract.currency = "USD"
        contract.secType = "CASH"

        return contract

    def mecContractCuntFut(self):

        contract = Contract()

        contract.exchange = "CME"
        contract.currency = "USD"
        contract.secType = "CONTFUT"
        contract.symbol = "MES"

        return contract

    def spxOptionsContract(self):

        contract = Contract()
        contract.conId = 637792305
        contract.exchange = "SMART"
        contract.symbol = "SPXW"
        contract.currency = "USD"
        contract.secType = "OPT"
        contract.multiplier = 100
        contract.right = "C"
        contract.lastTradeDateOrContractMonth = "20231214"
        contract.strike = 4570
        contract.localSymbol = "SPX   231215C04570000"


        return contract

    def spyOptionsContract(self):

        contract = Contract()

        contract.conId = 663434788
        contract.exchange = "SMART"

        return contract



if __name__ == "__main__":
    contracts = CustomContracts()
