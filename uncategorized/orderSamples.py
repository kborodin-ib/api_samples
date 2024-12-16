#! /usr/bin/env python3

from ibapi.order import Order

def marketGTDorder():

    order = Order()
    order.orderType = 'MKT'
    order.action = 'SELL'
    order.totalQuantity = 1
    order.tif = 'GTD'
    order.goodTillDate = '20240404 16:00:00'

    return order


