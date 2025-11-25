#! /usr/bin/env python3

from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from ibapi.contract import ComboLeg
from ibapi.order import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.symbol = "SPX"
        mycontract.secType = "BAG"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"

        leg1 = ComboLeg()
        leg1.conId = 823940009
        leg1.ratio = 1
        leg1.action = "SELL"
        leg1.exchange = "CBOE"

        leg2 = ComboLeg()
        leg2.conId = 823940029
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "CBOE"

        leg3 = ComboLeg()
        leg3.conId = 823939252
        leg3.ratio = 1
        leg3.action = "BUY"
        leg3.exchange = "CBOE"

        leg4 = ComboLeg()
        leg4.conId = 823939259
        leg4.ratio = 1
        leg4.action = "SELL"
        leg4.exchange = "CBOE"

        mycontract.comboLegs = [leg1, leg2, leg3, leg4]

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.orderType = "MKT"
        myorder.totalQuantity = 1

#        myorder.lmtPrice = 6.20

        # myorder.smartComboRoutingParams = []
        # myorder.smartComboRoutingParams.append(TagValue("NonGuaranteed", "0"))


        self.placeOrder(myorder.orderId, mycontract, myorder)

    def openOrder(
        self,
        orderId: OrderId,
        contract: Contract,
        order: Order,
        orderState: OrderState,
    ):
        print(
            "openOrder.",
            f"orderId:{orderId}",
            f"contract:{contract}",
            f"order:{order}",
            f"orderState:{orderState}",
            f"contract: {contract.comboLegs}"
        )

    def orderStatus(
        self,
        orderId: OrderId,
        status: str,
        filled: Decimal,
        remaining: Decimal,
        avgFillPrice: float,
        permId: int,
        parentId: int,
        lastFillPrice: float,
        clientId: int,
        whyHeld: str,
        mktCapPrice: float,
    ):
        print(
            "orderStatus.",
            f"orderId:{orderId}",
            f"status:{status}",
            f"filled:{filled}",
            f"remaining:{remaining}",
            f"avgFillPrice:{avgFillPrice}",
            # f"permId:{permId}",
            f"parentId:{parentId}",
            f"lastFillPrice:{lastFillPrice}",
            # f"clientId:{clientId}",
            # f"whyHeld:{whyHeld}",
            # f"mktCapPrice:{mktCapPrice}",
        )


app = TestApp()
app.connect("127.0.0.1", port, 7496)
app.run()
