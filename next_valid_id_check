#! /usr/bin/env python3

import ibapi
import time

print(ibapi.__version__)

from ibapi.sync_wrapper import TWSSyncWrapper

client = TWSSyncWrapper()

client.connect_and_start('127.0.0.1', 4002, 0)

while True:
    if client.next_valid_id_value is None:
        continue
    else:
        print(client.next_valid_id_value)
        print(client.isConnected())

        portfolio = client.get_portfolio(account_code="DU6036902")
        print("Portfolio: ", portfolio)

        client.reqCurrentTime()
        break
