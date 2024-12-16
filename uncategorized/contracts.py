#! /usr/bin/env python3

from ibapi.contract import Contract
from ibapi.contract import ComboLeg


class CustomContracts():

    def __init__(self):
        self.args = ""

    def idxContract(self):

        contract = Contract()

        contract.conId = 13796838
        contract.exchange = 'MEFFRV'

        return contract

    def spxOpt(self):

        contract = Contract()

        contract.symbol = 'SPX'
        contract.secType = 'OPT'
        contract.exchange = 'CBOE'
        contract.currency = 'USD'
        contract.right = 'P'
        contract.strike = 4175
        contract.lastTradeDateOrContractMonth = '20240920'

        return contract

    def amdOption(self):

        contract = Contract()

        contract.conId = 667983900
        contract.exchange = "SMART"
        contract.symbol = "AMD"

        return contract

    def vseContract(self):

        contract = Contract()

        contract.symbol = "OMV"
        contract.secType = "STK"
        contract.exchange = "VSE"
        contract.currency = "EUR"

        return contract
    
    def rsvContract(self):

        contract = Contract()
        contract.conId = 654503359 
        contract.exchange = 'CME'
        contract.symbol = 'RSVZ4'
        contract.secType = 'FUT'
        contract.lastTradeDateOrContractMonth = '20241220'
        
        return contract

    def aaplOptContract(self):
        contract = Contract()

        contract.symbol = "AAPL"
        contract.secType = "OPT"
        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.lastTradeDateOrContractMonth = "20240419"
        contract.strike = 10 
        contract.multiplier = 100
        contract.right = "C"
        return contract

    def mbtkContract(self):

        contract = Contract()

        contract.symbol = "MBTK4"
        contract.exchange = "CME"
        contract.currency = "USD"
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20240531"
        contract.multiplier = 0.1
        contract.tradingClass = "MBT"
        
        return contract

    def conidContract(self):

        contract = Contract()

        contract.conId = 693958228 
        contract.exchange = "SMART"

        return contract

    def testIndexContract(self, symbol, exchange):

        contract = Contract()

        contract.symbol = symbol
        contract.exchange = exchange 
        contract.secType = "IND"
        contract.currency = "USD"

        return contract

    def testContract(self):

        contract = Contract()

        contract.symbol = 'DFAS'
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'

        return contract

    def esContFut(self):        

        contract = Contract()

        contract.symbol = "ES"
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "2023"
        contract.exchange = "CME"
        contract.currency = "USD"
        contract.multiplier = 50
        contract.includeExpired = True

        return contract

    def aaplOption(self):

        contract = Contract()
        contract.secType = "OPT"
        contract.conid = 701273684
        contract.symbol = "AAPL 240524C00182500"
        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.tradingClass = "AAPL"
        contract.strike = 182.5 
        contract.multiplier = 100
        contract.right = "C"
        contract.lastTradeDateOrContractMonth = '20240524'
        return contract

    def lhvStkContract(self):
        
        contract = Contract()
        contract.symbol = "LHV1T"
        contract.secType = "STK"
        contract.exchange = "N.TALLINN"
        contract.currency = "EUR"

        return contract
        
    def bzg2Contract(self):

        contract = Contract()

        contract.symbol = "BZG2"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "EUR"

        return contract

    def qqqContract(self):

        contract = Contract()
        contract.symbol = "QQQ"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
#        contract.conid = 320227571

        return contract

    def zcComboContract(self):

        contract = Contract()
        contract.symbol = "ZC"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "CBOT"

        leg1 = ComboLeg()
        leg1.conId = "532513362"
        leg1.ratio = 1
        leg1.action = "SELL"
        leg1.exchange = "CBOT"

        leg2 = ComboLeg()
        leg2.conId = "460126205"
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "CBOT"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        return contract

    def someContract(self):

        contract = Contract()

#        contract.conId = 660320547
        contract.exchange = "CME"
        contract.symbol = "NQ"
        contract.localSymbol = "QNEV3 P14650"
        contract.strike = 14650
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = 20231031
        contract.tradingClass = "QNE"
        contract.right = "P"
        contract.secType = "FOP"

        return contract


    def spreadContract(self):

        contract = Contract()

        contract.symbol = "SPX"
        contract.secType = "BAG"
        contract.exchange = "SMART"
        contract.currency = "USD"
        
        leg1 = ComboLeg()
        leg1.conId = ""
        leg1.action = "SELL"
        leg1.ratio = 1
        leg1.exchange = "SMART"

        leg2 = ComboLeg()
        leg2.conId = ""
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "SMART"

        contract.comboLegs = [leg1, leg2]

        return contract

    def sehkContract(self):

        contract = Contract()

#        contract.conId = 652529945
        contract.exchange = "SEHK"
        contract.secType = "OPT"
        contract.strike = 277
        contract.right = "C"
        contract.multiplier = 0.002
        contract.exchange = "SEHK"
        contract.symbol = "53672"
        contract.currency = "HKD"

        return contract

    def eurUsdContract(self):

        contract = Contract()

        contract.exchange = "IDEALPRO"
        contract.symbol = "EUR"
        contract.currency = "USD"
        contract.secType = "CASH"
        contract.conId = 0
        contract.strike = 0.0

        return contract

    def espContract(self):

        contract = Contract()

        contract.symbol = "ES"
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20230915"
        contract.exchange = "QBALGO"
        contract.currency = "USD"
        contract.multiplier = 50
        contract.localSymbol = "ESU3"

        return contract

    def audUSDcontract(self):
        
        contract = Contract()

        contract.symbol = "AUD"
        contract.secType = "CASH"
        contract.currency = "USD"
        contract.exchange = "IDEALPRO"

        return contract

    def bagContract(self):

        contract = Contract()

        contract.symbol = "SPX"
        contract.secType = "BAG"
        contract.exchange = "SMART"
        contract.currency = "USD"

        leg1 = ComboLeg()
        leg1.conId = 656015286 
        leg1.ratio = 1
        leg1.action = "SELL"
        leg1.exchange = "SMART"

        leg2 = ComboLeg()
        leg2.conId = 656015352 
        leg2.ratio = 2
        leg2.action = "BUY"
        leg2.exchange = "SMART"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        return contract

    def mbcnContract(self):

        contract = Contract()
        contract.symbol = "MBCN"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        return contract

    def metContract(self):
        contract = Contract()
        contract.conId = 570162771
        contract.symbol = "METM3"
        contract.exchange = "CME"
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20230623"
        contract.multiplier = 0.1


        return contract

    def xauusd_contract(self):

        contract = Contract()

        contract.symbol = "XAUUSD"
        contract.secType = "CFD"
        contract.exchange = "SMART"
        contract.currency = "USD"

        return contract

    def forex_pair(self):

        contract = Contract()
        contract.symbol = "EUR"
        contract.exchange = "IDEALPRO"
        contract.secType = "CASH"
        contract.currency = "USD"

        return contract

    def bmw_contract(self):

        contract = Contract()
        contract.symbol = 'BMW'
        contract.exchange = 'SMART'
        contract.currency = 'EUR'
        contract.secType = "STK"
        
        return contract

    def bmwOption(self):

        contract = Contract()
        contract.conId = 694794973 
        contract.exchange = "SMART"

        return contract

    def ndx_nasdaq_contract(self):

        contract = Contract()
        contract.symbol = "NDX"
        contract.secType = "STK"
        contract.exchange = "VALUE"
        contract.currency = "CAD"

        return contract

    def ndx_idx_nasdaq(self):

        contract = Contract()
        contract.symbol = "NDX"
        contract.secType = "IND"
        contract.exchange = "NASDAQ"
        contract.currency = "USD"

        return contract

    def cnh_contract(self):
        contract = Contract()
        contract.symbol = "CNH"
        contract.lastTradeDateOrContractMonth = "20230416"
        contract.secType = "FUT"
        contract.multiplier = 100000
        contract.exchange = "CME"
        contract.currency = "CNH"
        contract.localSymbol = "CNHJ3"
        return contract

    def spy_contract(self):
        contract = Contract()
        contract.symbol = "SPY"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.lastTradeDateOrContractMonth = "20230818"
        contract.right = "CALL"
        contract.strike = "330"
        return contract

    def idx_contract(self):
        contract = Contract()
        contract.symbol = "SPX"
        contract.exchange = "CBOE"
        contract.currency = "USD"
        contract.secType = "IND"

        return contract

    def options_contract(self):
        contract = Contract()
        contract.symbol = "SPY"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.right = "P"
        contract.strike = 396
        contract.lastTradeDateOrContractMonth = "202303"
        return contract

    def tsla_contract(self):

        contract = Contract()

        contract.symbol = "TSLA"
        contract.secType = "STK"
        contract.exchange = "NYSE"
        contract.currency = "USD"

        return contract

    def shkntl_contract(self):

        contract = Contract()
        contract.symbol = "600519"
        contract.secType = "STK"
        contract.exchange = "SEHKNTL"
        contract.currency = "CNH"

        return contract

    def qmi_contract(self):

        contract = Contract()
        contract.symbol = "QMI"
        contract.secType = "IND"
        contract.currency = "USD"
        contract.exchange = "NASDAQ"

        return contract

    def aapl_contract(self):

        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"

        return contract

    def contFutContract(self):

        contract = Contract()
        contract.symbol = "DAX"
        contract.exchange = "EUREX"
        contract.currency = "EUR"
        contract.secType = "CONTFUT"

        return contract

    def comboContract(self):

        contract = Contract()




if __name__ == "__main__":
    contracts = CustomContracts()
