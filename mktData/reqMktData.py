#! /usr/bin/env python3

import logging
import ibapi
import time
import sys
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString
from contracts import CustomContracts

try:
    import google.protobuf
    print(google.protobuf.__version__)
except ImportError:
    print("google.protobuff needs to be added")
    sys.exit()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    def error(self, reqId: int, errorCode: int, errorString: str,
              advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'
        print(error_message)

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def tickPrice(self, reqId, tickType, price: float,
                  attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("TickPrice. TickerId:", reqId, "tickType:", tickType,
                  "Price:", floatMaxString(price), "CanAutoExecute:", attrib.canAutoExecute,
                  attrib.preOpen)

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("[+] Contract Details: ", reqId, contractDetails)

    def tickSize(self, reqId, tickType, size):
        super().tickSize(reqId, tickType, size)
        print("TickSize. TickerId:", reqId, "TickType:", tickType, "Size: ", decimalMaxString(size))


    def tickGeneric(self, reqId, tickType, value: float):
        super().tickGeneric(reqId, tickType, value)
        if tickType == 46:
            print("OPEN INTERESET: TickGeneric. TickerId:", reqId, "TickType:", tickType, "Value:", floatMaxString(value))

    def tickString(self, reqId, tickType, value: str):
        super().tickString(reqId, tickType, value)
        print("TickString. TickerId:", reqId, "Type:", tickType, "Value:", value)
  
    def currentTime(self, time):
        super().currentTime(time)
        print("current server time: ", time)

    def start(self):
        contract = CustomContracts().nqFutures()
        print(contract)
        self.reqCurrentTime()
        self.reqContractDetails(self.nextValidOrderId, contract)
        self.reqMarketDataType('3')
        self.reqMktData(8, contract, '236', False, False, [])

    def stop(self):
        self.done = True
        print("Stopped")
        self.disconnect()

def main():
    app = TestApp()
    cid = 0 #sys.argv[1]
    port = 7497  #int(sys.argv[2])
    time_seconds = 300 # 5 minutes
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > time_seconds:
            print("[+] Recconection timeout exceeded")
            sys.exit()

        if not app.isConnected():
            print("[+] Reconnecting")
            app.connect('127.0.0.1', port, clientId=cid)
            time.sleep(3)
        else:
            print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
            app.run()

if __name__ == '__main__':
    main()
