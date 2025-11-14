#! /usr/bin/env python3

import logging
import datetime
import time
import ibapi
from threading import Timer

from ibapi.common import ListOfPriceIncrements
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from datetime import datetime
from threading import Thread
from contracts import CustomContracts
import sys

from uncategorized.convert_tz import convert_times


def clFuturesOptions():
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

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.historicalBars = []

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject='', errTime=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    def historicalData(self, reqId, bar):
        super().historicalData(reqId, bar)
        #print("Historical data: ", reqId, bar.date, f"BID: {bar.open}", f"CLOSE: {bar.close}", f"{bar.wap}, time: {bar.date}")
        print(f"DATE {bar.date} --> OHLC: O: {bar.open} H: {bar.high} L: {bar.low} C: {bar.close}")
       # price = "469.06"
       # if f"{price}" in str(bar.open) or f"{price}" in str(bar.high) or f"{price}" in str(bar.close) or f"{price}" in str(bar.low):
        #    print(bar)
      #  self.historicalBars.append(bar)

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        if len(self.historicalBars) != 0:
            print("Writing bars...")
            with open(f'data/{reqId}data.txt', 'a') as file:
                file.write(f"{start}-{end}\n")
                file.write("BAR DATE   OPEN   HIGH    LOW\n")
                for bar in self.historicalBars:
                    string = f"{bar.date}, {bar.open}, {bar.high}, {bar.low}\n"
                    file.write(string)
                file.write('\n')
                file.close()
                print("Finished writing bars")
        print("Historical data end for: ", reqId)
        print(f"Start: {start} - End: {end}")
        self.disconnect()

    def marketRule(self, marketRuleId: int, priceIncrements: ListOfPriceIncrements):
        super().marketRule(marketRuleId, priceIncrements)
        print(f"[+] Market rule id: {marketRuleId}, price incremet: {priceIncrements}")
    
    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print(f"[+] TIME DATA: {reqId} - CONID: {contractDetails.contract.conId} - TH: {contractDetails.tradingHours} - TZID: {contractDetails.timeZoneId})")
        print(f"[+] EXCHANGE DATA: {reqId} - CONID: {contractDetails.contract.conId} - SYMBOL: {contractDetails.contract.symbol} - PRIMARY EXCH: {contractDetails.contract.primaryExchange} - EXCH: {contractDetails.contract.exchange}" )
        print(f"[+] PRIMARY EXCHANGE: {contractDetails.contract.primaryExchange}")

        if contractDetails.marketRuleIds:
            print(f"[+] MARKET RULE ID's: {contractDetails.marketRuleIds}")
            listOfIds = contractDetails.marketRuleIds.split(',')
            print(type(listOfIds))
            for rule in listOfIds:
                self.reqMarketRule(rule)

        if contractDetails.contract.primaryExchange == "ISLAND":
            print(f"[+] Received primary exchange: {contractDetails.contract.primaryExchange}")
            sys.exit()

        if contractDetails.contract.symbol == "MES":
            if contractDetails.contract.conId != 711280067:
                print(f"[+] Invalid conid received for MES: {contractDetails.contract.conId}; Correct is 711280067")
                sys.exit()

        if contractDetails.contract.symbol == "MYM":
            if contractDetails.contract.conId != 730283051:
                print(f"[+] Invalid conid received for MYM: {contractDetails.contract.conId}; Correct is 711280067")
                sys.exit()
        time.sleep(1)
     #   print("Disconnecting")
      #  self.disconnect()
      #  self.start()
    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def headTimestamp(self, reqId, headTimeStamp):
        print("HeadTimeStamp: ", headTimeStamp)

    def historicalTicksBidAsk(self, reqId: int, ticks,
                              done: bool):
        for tick in ticks:
            self.convert_unix_timestamp(tick.time)
            print("HistoricalTickBidAsk. ReqId:", reqId, tick)

    def historicalTicksLast(self, reqId: int, ticks,
                            done: bool):
        for tick in ticks:
            self.convert_unix_timestamp(tick.time)
            print("HistoricalTickLast. ReqId:", reqId, tick)

    def setTimeZone(timezone):
        endTime = datetime(2024, 3, 26, 16, 15, 0, 0, pytz.timezone('America/New_York'))
        endTimeString = endTime.astimezone(pytz.UTC).strftime('%Y%m%d-%H:%M:%S')
        return endTimeString

    def headTimestamp(self, reqId, headTimeStamp):
        print(f"[+] TIMESTAMP: {headTimeStamp}")
        self.disconnect()


    def start(self):
        contract = CustomContracts().vxxStk()
        print(contract)
        
        endDate = "20240614 00:00:00 US/Eastern"
     #   endDate = ""
  #      self.reqHeadTimeStamp(self.nextValidOrderId, contract, "TRADES", True,2)
        print(f"END DATE: ", endDate)
        self.reqHistoricalData(self.nextValidOrderId, contract, endDate,
                '1 D', '1 min', 'TRADES', False, 1, False, [])

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        print(ibapi.__version__)
        print("test")
        app = TestApp()
        app.connect('127.0.0.1', 7496, clientId=5)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
