#!/usr/bin/env python3
"""
Interactive Brokers API — SPX Combo TRAIL Order Submission
Creates and submits a 4-leg SPX BAG contract with trailing stop order
"""

import threading
import time

from ibapi.client import EClient
from ibapi.contract import ComboLeg, Contract
from ibapi.order import Order
from ibapi.wrapper import EWrapper
from ibapi.tag_value import TagValue


class IBApp(EWrapper, EClient):
  
    def __init__(self):
        EClient.__init__(self, self)
        self.nextOrderId = None

    def nextValidId(self, orderId: int):
        self.nextOrderId = orderId
        print(f"Next Valid Order ID: {orderId}")

    def orderStatus(self, orderId, status, filled, remaining,
                    avgFillPrice, permId, parentId, lastFillPrice,
                    clientId, whyHeld, mktCapPrice):
        print(
            f"Order {orderId} Status: {status} | "
            f"Filled: {filled} | Remaining: {remaining}"
        )

    def openOrder(self, orderId, contract, order, orderState):
        print(f"Open Order {orderId} | Status: {orderState.status}")

    def error(self, reqId, errorTime, errorCode, errorString,
              advancedOrderRejectJson=""):
        print(f"Error {reqId} | Code: {errorCode} | Msg: {errorString}")


def create_spx_combo_contract() -> Contract:

    contract = Contract()
    contract.symbol = "SPX"
    contract.secType = "BAG"
    contract.exchange = "CBOE"
    contract.currency = "USD"


    leg1 = ComboLeg()
    leg1.conId = 895592631 
    leg1.ratio = 1
    leg1.action = "BUY"
    leg1.exchange = "CBOE"

    leg2 = ComboLeg()
    leg2.conId = 895592637 
    leg2.ratio = 1
    leg2.action = "BUY"
    leg2.exchange = "CBOE"

    leg3 = ComboLeg()
    leg3.conId = 895591454 
    leg3.ratio = 1
    leg3.action = "SELL"
    leg3.exchange = "CBOE"

    leg4 = ComboLeg()
    leg4.conId = 895591463 
    leg4.ratio = 1
    leg4.action = "SELL"
    leg4.exchange = "CBOE"

    contract.comboLegs = [leg1, leg2, leg3, leg4]
    return contract


def create_trail_order(order_id: int, limit_price: float,
                       trail_amount: float) -> Order:

    order = Order()

    order.orderId = order_id
    order.clientId = 0
    order.action = "BUY"
    order.totalQuantity = 1
    order.displaySize = 0
    order.orderType = "TRAILLMT"

    order.lmtPrice = limit_price
    order.smartComboRoutingParams = [TagValue("NonGuaranteed", "0")]
    order.auxPrice = trail_amount
    order.trailStopPrice = limit_price 
    order.tif = "GTC"
    order.outsideRth = True
    order.ocaGroup = str(order_id)
    order.ocaType = 3

    # Order reference (from original log)
    order.orderRef = f"TAT T: 508 O: {order_id} (STP)"
    order.transmit = True

    print(order.lmtPrice)

    return order


def main():
    """Main execution: connect to IB Gateway and submit order"""
    app = IBApp()
    app.connect("172.23.208.1", 7496, clientId=1)
    thread = threading.Thread(target=app.run, daemon=True)
    thread.start()
    timeout = 10
    while app.nextOrderId is None and timeout > 0:
        time.sleep(0.1)
        timeout -= 0.1

    if app.nextOrderId is None:
        print("ERROR: Did not receive nextValidId — check Gateway connection")
        app.disconnect()
        return

    contract = create_spx_combo_contract()

    # The example below uses a placeholder — replace with live data
    CURRENT_COMBO_NET_PRICE = 5.00
    TRAIL_AMOUNT = 2.50

    order = create_trail_order(
        order_id=app.nextOrderId,
        limit_price=CURRENT_COMBO_NET_PRICE,
        trail_amount=TRAIL_AMOUNT
    )

    print(
        f"Placing 4-leg SPX combo TRAIL order | "
        f"ID: {app.nextOrderId} | "
        f"lmtPrice: {CURRENT_COMBO_NET_PRICE} | "
        f"Trail: {TRAIL_AMOUNT}"
    )

    app.placeOrder(app.nextOrderId, contract, order)

    time.sleep(3)
    app.disconnect()


if __name__ == "__main__":
    main()

