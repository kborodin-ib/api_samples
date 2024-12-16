#! /usr/bin/env python3

from AvailableAlgoParams import AvailableAlgoParams
from ibapi.order import Order
from ibapi.tag_value import TagValue


def sampleTwapOrder():
    order = Order()

    order.action = "BUY"
    order.orderType = "MKT"
    order.totalQuantity = 1

#    AvailableAlgoParams.FillTwapParams(order, 'Marketable', '03:04:48 US/Eastern',
#            '06:04:52 US/Eastern', True)
    print(order)
    return order

def sampleAdaptiveOrder():

    order = Order()
    order.orderType = "MKT"
    order.action = "BUY"
    order.outsideRth = True
    order.transmit = True
    order.totalQuantity = 1
    order.algoStrategy = "Adaptive"
    order.algoParams = []
    order.algoParams.append(TagValue('adaptivePriority', 'Patient'))

def sampleDarkIceAlgo():

    order = Order()
    order.orderType = "LMT"
    order.action = "BUY"
    order.totalQuantity = 200 
    order.lmtPrice = '175.4'
    order.algoStrategy = "DarkIce"
    order.algoParams = []
    order.algoParams.append(TagValue('displaySize', '2'))
    order.algoParams.append(TagValue('startTime', '16:00:00 MET'))
    order.algoParams.append(TagValue('endTime', '18:00:00 MET'))
    order.algoParams.append(TagValue('allowPastEndTime', '1'))

    return order


if __name__ == "__main__":
    twapOrder = sampleTwapOrder()


