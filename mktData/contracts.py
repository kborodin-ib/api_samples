#! /usr/bin/env python3

from ibapi.contract import Contract
from ibapi.contract import ComboLeg

class CustomContracts():

    def __init__(self):
        self.args = ""

    def isinAaplContract(self):

        contract = Contract()
        contract.secIdType = 'ISIN'
        contract.secId = 'US0378331005'
        contract.exchange = 'SMART'

        return contract

    def cgbContract(self):
        
        contract = Contract()

        contract.conId = 692364773
        contract.secType = "BOND"
        contract.currency = "CAD"
        contract.exchange = "CDE"
        
        return contract

    def mnqContract(self):

        contract = Contract()

        contract.secType = 'FUT'
        contract.lastTradeDateOrContractMonth = "20241220"
        contract.currency = "USD"
        contract.tradingClass = "MNQ"
        contract.exchange = "CME"
        contract.multiplier = 2
        contract.symbol = "MNQZ4"

        return contract


    def conidContractSample(self):

        contract = Contract()

        contract.conid = 723652244

        return contract

    def basfContract(self):

        contract = Contract()

        contract.symbol = 'BAS'
        contract.exchange = 'SMART'
        contract.secType = "STK"
        contract.currency = "EUR"
        contract.primaryExchange = 'ENEXT.BE'
        
        return contract

    
    def niftyIndex(self):

        contract = Contract()

        contract.symbol = 'BANKNIFTY'
        contract.exchange = "NSE"
        contract.secType = "IND"
        contract.currency = 'INR'

        return contract

    def cfdContract(self):

        contract = Contract()

        contract.symbol = 'USD'
        contract.secType = 'CFD'
        contract.exchange = 'SMART'
        contract.currency = 'JPY'

        return contract

    def fopContractMES(self):

        contract = Contract()

        contract.symbol = "MES"
        contract.secType = "FOP"
        contract.lastTradeDateOrContractMonth = "20241018"
        contract.exchange = "CME"
        contract.currency = "USD"
        contract.tradingClass = "EX3"
        contract.strike = 100
        contract.right = "C"
        contract.multiplier = 5

        return contract

    def comboLegContract(self):

        contract = Contract()

        contract.symbol = 'GC'
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "COMEX"
#        contract.multiplier = 100
#        contract.tradingClass = 'GC'
#        contract.lastTradeDateOrContractMonth = '20240926'

        leg1 = ComboLeg()
        leg1.conId = 726219326
        leg1.ratio = 1
        leg1.action = "SELL"
        leg1.exchange = "SMART"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)

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
#        contract.conId = 265598
        contract.exchange = "SMART"
        contract.primaryExchange = "NASDAQ"
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.currency = "USD"

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
