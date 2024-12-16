#! /usr/bin/env python3

from ibapi.client import *
from ibapi.wrapper import *
import threading
import time
import logging

# Set up logging
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s - %(levelname)s - %(message)s',
#                    handlers=[logging.StreamHandler()])

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def tickPrice(self, reqId, tickType, price, attrib):
        logging.debug(f"Tick Price. ReqId: {reqId}, TickType: {tickType}, Price: {price}")
        if tickType == 2 and reqId == 1:
            logging.info(f'The current ask price is: {price}')

    def tickSize(self, reqId: TickerId, tickType: TickType, size: Decimal):
        print("TickSize. TickerId:", reqId, "TickType:", tickType, "Size: ", decimalMaxString(size))

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        logging.error(f"Error {errorCode}: {errorString}")

def run_loop():
    app.run()

app = IBapi()
app.connect('192.168.43.222', 7496, 123)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(3)  # Increase sleep interval to allow time for connection to server

# Create contract object
contract = Contract()
contract.symbol = 'SPX'
contract.secType = 'OPT'
contract.exchange = 'SMART'
contract.currency = 'USD'
contract.right = 'P'
contract.strike = 4175  # Strike price should be a number, not a string
contract.lastTradeDateOrContractMonth = '20240920'

# Log the contract details
logging.info(f"Requesting data for contract: {contract}")

# Set to delayed market data
app.reqMarketDataType('3')  # 1 = real-time, 2 = frozen, 3 = delayed, 4 = delayed-frozen

# Request Market Data
app.reqMktData(1, contract, '', False, False, [])

time.sleep(15)  # Increase sleep interval to allow time for incoming price data
app.disconnect()

