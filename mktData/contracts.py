#! /usr/bin/env python3

from ibapi.contract import Contract
from ibapi.contract import ComboLeg

class CustomContracts():

    def __init__(self):
        self.args = ""

    def vxxStk(self):

        contract = Contract()

        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.symbol = "VXX"
        contract.primaryExchange = "BATS"

        return contract

    def nqFutures(self):

        contract = Contract()

        contract.symbol = "NQ"
        contract.secType = "FOP"
        contract.exchange = "CME"
        contract.multiplier = 20
        contract.right = "C"
        contract.conId = 799532732

        return contract

    def oilyContract(self):

        contract = Contract()
        contract.exchange = "CBOT"
        contract.symbol = "ZL"
        contract.secType = "FUT"
        contract.conid = 671574028
        contract.lastTradeDateOrContractMonth = "20260114"
        contract.multiplier = 60000

        return contract

    def esFuturesContractSept(self):

        contract = Contract()

        contract.conId = "711280067"
        contract.symbol = "NQ"
        contract.symbol = "MES"
        contract.exchange = "CME"

        return contract

    def futuresContract(self):

        contract = Contract()

        contract.symbol = "MES"
        contract.exchange = "CME"
        contract.secType = "FUT"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20250919"

        return contract

    def mymContract(self):

        contract = Contract()

        contract.symbol = "MYM"
        contract.exchange = "CBOT"
        contract.secType = "FUT"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20250919"

        return contract


    def unknownContract(self):

        contract = Contract()

        contract.conId = 705924553
        contract.exchange = "SMART"

        return contract

    def clFuturesOptions(self):

        contract = Contract()

        contract.symbol = "LN1U5 C1750"
        contract.exchange = "NYMEX"
        contract.lastTradeDateOrContractMonth = "20250905"
        contract.strike = 1.75
        contract.multiplier = 10000
        contract.right = "C"
        contract.tradingClass = "LN1"
        contract.secType = "FOP"

        return contract

    def clFuturesOptions(self):

        contract = Contract()

        contract.symbol = "LO1U5 C6575"
        contract.exchange = "NYMEX"
        contract.lastTradeDateOrContractMonth = "20250905"
        contract.strike = 65.75
        contract.multiplier = 1000
        contract.right = "P"
        contract.tradingClass = "LO1"
        contract.secType = "FOP"

        return contract

    def qcomSMART(self):

        contract = Contract()

        contract.symbol = "QCOM"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        return contract

    def nq5mini(self):

        contract = Contract()

        contract.conid = 672387474
        contract.exchange = "CME"
        contract.symbol = "NQ"
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20250620"

        return contract

    def esFuturesContractSept(self):

        contract = Contract()

        contract.conId = "711280067"
        contract.symbol = "MES"
        contract.exchange = "CME"

        return contract

    def qcomContract(self):

        contract = Contract()

        contract.symbol = "QCOM"
        contract.exchange = "ISLAND"
        contract.currency = "USD"
        contract.secType = "STK"

        return contract

    def esu5Futures(self):

        contract = Contract()
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20250919"
        contract.currency = "USD"
        contract.multiplier = 50
        contract.exchange = "CME"
        contract.tradingClass = "ES"
        contract.symbol = "ESU5"

        return contract

    def esOptions(self):

        contract = Contract()

        contract.secType = "OPT"
        contract.lastTradeDateOrContractMonth = "20250718"
        contract.strike = 45
        contract.right = "P"
        contract.currency = "USD"
        contract.multiplier = 100
        contract.exchange = "SMART"
        contract.symbol = "ES  250718P00045000"
        contract.tradingClass = "ES"

        return contract

    def tqqOption(self):

        contract = Contract()

        contract.symbol = "TQQQ"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20250718"
        contract.strike = 58
        contract.right = "P"
        contract.multiplier = "100"

        return contract

    def esContFut(self):

        contract = Contract()

        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20250919"
        contract.currency = "USD"
        contract.multiplier = 50
        contract.exchange = "CME"
        contract.tradingClass = "ES"
        contract.symbol = "ESU5"

        return contract

    def daxFutures(self):

        contract = Contract()

        contract.symbol = "EUR"
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20250920"
        contract.currency = "EUR"
        contract.multiplier = 1
        contract.exchange = "EUREX"
        contract.tradingClass = "FDXS"

        return contract
    
    def tslaContract(self):

        contract = Contract()

        contract.conId = '76792991'
        contract.secType = "STK"
        contract.symbol = "TSLA"
        contract.currency = "USD"
        contract.exchange = "SMART"

        return contract

    def nyseFANGcontract(self):

        contract = Contract()

        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20251219"
        contract.currency = "USD"
        contract.multiplier = 5
        contract.exchange = "NYBOT"
        contract.tradingClass = "FNG"
        contract.symbol = "FNGM5"

        return contract

    def expiredOptionsContract(self):

        contract = Contract()

        contract.symbol = "GOOG"
        contract.secType = "OPT"
        contract.exchange = "BOX"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20190315"
        contract.strike = 1180
        contract.right = "C"
        contract.multiplier = 100

        return contract

    def dltrContract(self):

        contract = Contract()

        contract.secType = "OPT"
        contract.lastTradeDateOrContractMonth = "20250606"
        contract.strike = 94
        contract.right = 'C'
        contract.currency = "USD"
        contract.multiplier = 100
        contract.exchange = "SMART"
        contract.tradingClass = "DLTR"
        contract.symbol = "DLTR  250606C00094000"

        return contract

    def bmwContract(self):

        contract = Contract()

        contract.symbol = "BMW"
        contract.exchange = "IBIS"
        contract.currency = "EUR"
        contract.secType = "STK"

        return contract

    def matifFutures(self):

        contract = Contract()

        contract.exchange = "MATIF"
        contract.symbol = "EBMU5"
        contract.currency = "EUR"
        contract.lastTradeDateOrContractMonth = "20250910"
        contract.multiplier = 50
        contract.tradingClass = "EBM"
        contract.secType = "FUT"

        return contract

    def sbFutures(self):

        contract = Contract()

        contract.conId = 577421489
        contract.exchange = "NYBOT"

        return contract

    def goldContFut(self):

        contract = Contract()

        contract.symbol = "1610200A0"
        contract.exchange = "OSE.JPN"
        contract.conId = 764466855

        return contract

    def bmwContFut(self):

        contract = Contract()

        contract.symbol = "BMW"
        contract.secType = "CONTFUT"
        contract.exchange = "EUREX"
        contract.currency = "EUR"
        contract.lastTradeDateOrContractMonth = "20250520"
        contract.tradingClass = "BMWF"
        contract.multiplier = 100
        contract.conId = 705063011

        return contract

    def esFuturesContract(self):

        contract = Contract()

        contract.symbol = "ESM5"
        contract.lastTradeDateOrContractMonth = "20250620"
        contract.currency = "USD"
        contract.multiplier = 50
        contract.exchange = "CME"
        contract.tradingClass = "ES"
        contract.secType = "FUTco"

        return contract

    def appContract(self):

        contract = Contract()

        contract.symbol = "APP"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20250815"
        contract.right = "C"
        contract.strike = 490

        return contract

    def appContractStok(self):

        contract = Contract()

        contract.symbol = "APP"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"

        return contract

    def spxOptContract(self):

        contract = Contract()

        contract.conId = 780432873
        contract.symbol = "SPX"
        contract.exchange = "SMART"

        return contract

    def currencyContract(self):

        contract = Contract()

        contract.symbol = "EUR"
        contract.currency = "USD"
        contract.exchange = "IDEALPRO"
        contract.secType = "CASH"

        return contract

    def testContract(self):

        contract = Contract()

        contract.symbol = "GCM5"
        contract.conId = 0
        contract.secType = "FUT"
        contract.exchange = "COMEX"
        contract.currency = "USD"
        contract.tradingClass = "GC"
        contract.lastTradeDateOrContractMonth = "202506"

        return contract

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

    def toyotaContract(self):

        contract = Contract()

        contract.exchange = "SMART"
        contract.secType = "STK"
        contract.currency = "JPY"
        contract.symbol = "7203"
     #   contract.primaryExchange = "TSEJ"

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
