#! /usr/bin/env python3

import ibapi
import time
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString
from ibapi.contract import Contract

try:
    import google.protobuf
    print(google.protobuf.__version__)
except ImportError:
    pass

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    def error(self, reqId: int, errorTime, errorCode: int, errorString: str,
              advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        print(f"{errorTime} - {errorCode} - {errorString}")

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        self.start()

    def currentTime(self, time):
        print(time)
        self.disconnect()

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("[+] Contract Details: ", reqId, contractDetails)

    def tickSize(self, reqId, tickType, size):
        if tickType == 89:
            super().tickSize(reqId, tickType, size)
            print("TickSize. TickerId:", reqId, "TickType:", tickType, "Size: ", size)

    def currentTime(self, time):
        super().currentTime(time)
        print("current server time: ", time)

    def start(self):
        contract = Contract()

        contract.symbol = "AAPL"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.secType = "STK"

        self.reqContractDetails(self.nextValidOrderId, contract)
        self.reqMarketDataType(1)
        self.reqMktData(8, contract, '236', False, False, [])

    def stop(self):
        self.done = True
        print("Stopped")
        self.disconnect()

def main():
    app = TestApp()
    cid = 0 #sys.argv[1]
    port = 7496  #int(sys.argv[2])
    time_seconds = 300 # 5 minutes
    start_time = time.time()
    local_ip = "172.23.208.1"
    remote_ip = "10.12.100.185"
    while True:
        elapsed = time.time() - start_time
        if elapsed > time_seconds:
            print("[+] Recconection timeout exceeded")
            sys.exit()

        if not app.isConnected():
            print("[+] Connecting")
            app.connect(local_ip, port, clientId=cid)
            time.sleep(10)
        else:
            print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
            app.run()

if __name__ == '__main__':
    main()
