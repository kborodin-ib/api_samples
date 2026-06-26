#! /usr/bin/env python3

from ibapi.contract import Contract
from ibapi.contract import ComboLeg


contract = Contract() 

class testContracts():

    def __init__(self):
        self.args = ""


    def qcomContract(self):

        contract.symbol = 'QCOM'
        contract.conid = 728962271
        contract.lastTradeDateOrContractMonth = '20270115'
        contract.exchange = 'SMART'
        contract.secType = "OPT"
        contract.strike = 150
        contract.right = 'P'

        return contract

    def topX(self):

        contract.symbol = "TOPX"
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20260910"
        contract.multiplier = 10000
        contract.exchange = "OSE.JPN"
        contract.currency = "JPY"
        
        return contract

    def bagContract(self):

        mycontract = Contract()
        mycontract.symbol = "NOB"
        mycontract.secType = "BAG"
        mycontract.currency = "USD"
        mycontract.exchange = "CBOT"

        leg1 = ComboLeg()
        leg1.conId = 815824229# 3845
        leg1.ratio = 2
        leg1.action = "BUY"
        leg1.exchange = "CBOT"

        leg2 = ComboLeg()
        leg2.conId = 815824224# 3855
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "CBOT"
        
        mycontract.comboLegs = []
        mycontract.comboLegs.append(leg1)
        mycontract.comboLegs.append(leg2)

        return mycontract

    def dteOption(self):

        contract.symbol = "DTR"
        contract.exchange = "EUREX"
        contract.strike = 29.5
        contract.currency = "EUR"
        contract.multiplier = 100
        contract.right = "P"
        contract.secType = "OPT"
        contract.tradingClass = "DTE"
        contract.lastTradeDateOrContractMonth = "20260529"

        return contract

    def spyStkContract(self):


        contract.symbol = 'SPY'
        contract.secType = "STK"
        contract.exchange = "ARCA"
        contract.currency = "USD"

        return contract

    def wierdChineseContract(self):


        contract.symbol = "000001"
        contract.exchange = "SEHKSZSE"
        contract.secType = "STK"
        contract.currency = "CNH"

        return contract

