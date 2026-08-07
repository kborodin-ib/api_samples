#!/usr/bin/env python3
"""
Interactive Brokers API — Contract Details and Security Definition Lookup
Queries contract details and security definition option parameters via TWS API
"""

import threading
import time

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper


class IBApp(EWrapper, EClient):
    """Interactive Brokers API wrapper for contract queries"""

    def __init__(self):
        EClient.__init__(self, self)
        self.contract_details = {}
        self.sec_def_opt_params = []
        self.contract_details_event = threading.Event()
        self.sec_def_event = threading.Event()

    # Contract details callbacks
    def contractDetails(self, reqId, contractDetails):
        """Store contract details when received"""
        self.contract_details.setdefault(reqId, []).append(contractDetails)

    def contractDetailsEnd(self, reqId):
        """Signal completion of contract details request"""
        self.contract_details_event.set()

    # Security definition option params callbacks
    def securityDefinitionOptionParameter(
        self,
        reqId,
        exchange,
        underlyingConId,
        tradingClass,
        multiplier,
        expirations,
        strikes
    ):
        """Store security definition option parameters when received"""
        self.sec_def_opt_params.append({
            "exchange": exchange,
            "underlyingConId": underlyingConId,
            "tradingClass": tradingClass,
            "multiplier": multiplier,
            "expirations": expirations,
            "strikes": strikes,
        })
        print('sec def call')
        print(self.sec_def_opt_params)

    def securityDefinitionOptionParameterEnd(self, reqId):
        """Signal completion of security definition request"""
        self.sec_def_event.set()

    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        """Handle API errors"""
        print(
            f"Error. Id: {reqId}, Time: {errorTime}, Code: {errorCode}, Msg: {errorString}"
        )


def run_loop(app):
    """Run API event loop in background thread"""
    app.run()


def main():
    """Main execution: query contract details and security definitions"""
    
    # Create unique client ID
    client_id = int(time.time()) % 10000
    
    # Initialize app and connect
    app = IBApp()
    app.connect('172.23.208.1', 7496, clientId=client_id)
    
    # Start event loop in background thread
    api_thread = threading.Thread(target=run_loop, args=(app,), daemon=True)
    api_thread.start()
    
    # Allow connection to establish
    time.sleep(1)
    
    # Test symbols and date
    test_symbols = ['CFBTC', 'CFETH', 'CFXRP', 'CFSOL']
    today_str = '20260806'
    
    print("Querying contract details (5s delay between requests)\n")
    
    req_id = 1
    for symbol in test_symbols:
        # Build contract
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'OPT'
        contract.exchange = 'FORECASTX'
        contract.currency = 'USD'
        contract.lastTradeDateOrContractMonth = today_str
        
        # Clear event and storage
        app.contract_details_event.clear()
        app.contract_details[req_id] = []
        
        # Request and time
        t0 = time.perf_counter_ns()
        app.reqContractDetails(req_id, contract)
        
        # Wait for response (timeout 15s)
        app.contract_details_event.wait(timeout=15)
        elapsed_s = (time.perf_counter_ns() - t0) / 1_000_000_000
        
        # Report results
        details = app.contract_details.get(req_id, [])
        print(f"{symbol:<10} | Details: {len(details):<3} | Time: {elapsed_s:.2f}s")
        
        req_id += 1
    
    # Query security definition option parameters
    print("\nQuerying security definition option parameters...")
    app.sec_def_event.clear()
    app.sec_def_opt_params = []
    
    app.reqSecDefOptParams(
        reqId=req_id,
        underlyingSymbol="CFETH",
        futFopExchange="",
        underlyingSecType="IND",
        underlyingConId=860825103
    )
    
    app.sec_def_event.wait(timeout=15)
    
    if app.sec_def_opt_params:
        print(f"\nReceived {len(app.sec_def_opt_params)} parameter sets:")
        for idx, params in enumerate(app.sec_def_opt_params, 1):
            print(f"\n  Set {idx}:")
            for key, value in params.items():
                print(f"    {key}: {value}")
    else:
        print("⚠️  No parameters returned (list is empty)")
    
    # Cleanup
    app.disconnect()


if __name__ == "__main__":
    main()
