import requests
import json
import logging
import threading
import asyncio
import websockets
import ssl
import sys
import time
from datetime import datetime

BASE_URL = "https://127.0.0.1:5000/v1/api"
ORDER_URL = BASE_URL + "/iserver/account/DU6036902/orders"
WS_URL = "wss://127.0.0.1:5000/v1/api/ws"

requests.packages.urllib3.disable_warnings()

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler('app.log'),
                    ])
logger.info('Started')

orders_to_place = [
            {
                "conidex": "14094@IBIS",
                "orderType": "LMT",
                "side": "BUY",
                "price": 60,
                "tif": "DAY",
                "outsideRTH": True,
                "quantity": 100
            },
            {
                "conidex": "14094@IBIS",
                "orderType": "LMT",
                "side": "BUY",
                "price": 60,
                "tif": "DAY",
                "outsideRTH": True,
                "quantity": 100
            },
            {
                "conidex": "14094@IBIS",
                "orderType": "LMT",
                "side": "BUY",
                "price": 60,
                "tif": "DAY",
                "outsideRTH": True,
                "quantity": 100
            },
            {
                "conidex": "14094@IBIS",
                "orderType": "LMT",
                "side": "BUY",
                "price": 60,
                "tif": "DAY",
                "outsideRTH": True,
                "quantity": 100
            },
            {
                "conidex": "14094@IBIS",
                "orderType": "LMT",
                "side": "BUY",
                "price": 60,
                "tif": "DAY",
                "outsideRTH": True,
                "quantity": 100
            },
            {
                "conidex": "14094@IBIS",
                "orderType": "LMT",
                "side": "BUY",
                "price": 60,
                "tif": "DAY",
                "outsideRTH": True,
                "quantity": 100
            },
            {
                "conidex": "14094@IBIS",
                "orderType": "LMT",
                "side": "BUY",
                "price": 60,
                "tif": "DAY",
                "outsideRTH": True,
                "quantity": 100
            },
            {
                "conidex": "14094@IBIS",
                "orderType": "LMT",
                "side": "BUY",
                "price": 60,
                "tif": "DAY",
                "outsideRTH": True,
                "quantity": 100
            },
            {
                "conidex": "14094@IBIS",
                "orderType": "LMT",
                "side": "BUY",
                "price": 60,
                "tif": "DAY",
                "outsideRTH": True,
                "quantity": 100
            },
            {
                "conidex": "14094@IBIS",
                "orderType": "LMT",
                "side": "BUY",
                "price": 60,
                "tif": "DAY",
                "outsideRTH": True,
                "quantity": 100
            },



        ]

# Suppress messages
def suppressMessageIDS():
    suppress_url = BASE_URL + "/iserver/questions/suppress"
    payload = json.dumps({
        "messageIds": ["o102,o163,o10331,o383,o451,o354"]
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.post(suppress_url, headers=headers, data=payload, verify=False)
    print("Suppress: ", response.text)

# Place one or more orders

def placeOrdersIndividually(order_list, max_retries=3, retry_delay=2, side="BUY"):
    """
    Submits each order individually with retry logic for failures.
    :param order_list: List of order dictionaries.
    :param max_retries: Number of retry attempts per order.
    :param retry_delay: Delay in seconds between retries.
    """
    for idx, order in enumerate(order_list, start=1):
        print(f"\n [+] Placing order: {order})")
        attempt = 0
        success = False

        while attempt < max_retries and not success:
            payload = {"orders": [order]}
            try:
                response = requests.post(ORDER_URL, json=payload, verify=False)
                if response.status_code == 200:
                    if "error" in json.loads(response.text) and "15 orders working on either" in json.loads(response.text)['error']:
                        print("15 orders limit reached, changing direction")
                        curretSide = payload["orders"][0]['side']
                        newSide = "BUY" if curretSide == "SELL" else "SELL"
                        payload["orders"][0]['side'] = newSide
                        response = requests.post(ORDER_URL, json=payload, verify=False)
                        print(response.text)
                    print(f"[{idx}] ✅ Order submitted successfully.")
                    print(f"Response: {response.text}")
                    success = True
                    order_data = json.loads(response.text)[0]
                    print(order_data)
                    if order_data and int(order_data['order_id']) % 3 == 0:
                        print(f"Canceling order with id {order_data['order_id']}")
                        cancelOrder(order_data)

                else:
                    print(f"[{idx}] ❌ Failed (Status {response.status_code}). Retrying...")
            except requests.exceptions.RequestException as e:
                print(f"[{idx}] ❌ Exception occurred: {e}. Retrying...")

            attempt += 1
            if not success and attempt < max_retries:
                time.sleep(retry_delay)

        if not success:
            print(f"[{idx}] ❌ Order failed after {max_retries} attempts.")

CANCEL_URL = BASE_URL + "/iserver/account/DU6036902/order/"
cancelled_orders = []
def cancelOrder(order_info):
    response = requests.delete(f"{CANCEL_URL}/{order_info['order_id']}", verify=False)
    if response.status_code == 200:
        print(f"✅ Cancelled order {order_info['order_id']}")
        cancelled_orders.append({
            "id": order_info["order_id"],
            "timestamp": datetime.now().isoformat()
        })

        data = {
            "order id": order_info["order_id"],
            "timestamp": datetime.now().isoformat()
        }

        with open("cancelled_orders.json", "a") as f:
            json.dump(data, f, indent=4)

    else:
        print(f"❌ Failed to cancel order {order_info['order_id']}: {response.status_code} - {response.text}")


# Monitor orders via WebSocket
async def monitorOrders(msgList):
    ssl_context = ssl._create_unverified_context()
    async with websockets.connect(WS_URL, ssl=ssl_context) as websocket:
        rst = await websocket.recv()
        jsonData = json.loads(rst.decode())
        print(jsonData)

        if jsonData.get('message') == 'waiting for session':
            print('No active sessions found. Are you logged in?')
            sys.exit()

        while True:
            if msgList:
                currentMsg = msgList.pop(0)
                await asyncio.sleep(1)
                await websocket.send(currentMsg)

            rst = await websocket.recv()
            jsonData = json.loads(rst.decode())

            if 'topic' in jsonData:
                if jsonData['topic'] == 'sor':
                    response = f"{jsonData['topic']} --> {json.dumps(jsonData, indent=4)}"
                    cOID_presence = "order_ref" in jsonData['args'][0]
                    print("SOR: ", response)
                    print(f"[+] order_ref key is present: {cOID_presence}")

            if 'error' in jsonData:
                print(jsonData['error'])

# Thread wrapper for asyncio
def startMonitoring(msgList):
    print(f"[+] Subscribed to live order updates")
    asyncio.run(monitorOrders(msgList))

# Thread wrapper for placing orders
def startPlacingOrders(order_list):
    placeOrders(order_list)

def infiniteLoop():
    while True:
        placeOrdersIndividually(orders_to_place, 3, 2)

# Main execution
if __name__ == "__main__":
    try:
        suppressMessageIDS()

        # Define messages to send via WebSocket
        messages = [
            "sor+{}"
        ]

        # Define orders to place


        # Start monitoring and placing orders in parallel
        monitor_thread = threading.Thread(target=startMonitoring, args=(messages,))
      #  order_thread = threading.Thread(target=placeOrdersIndividually, args=(orders_to_place, 3, 2))
        infiniteThread = threading.Thread(target=infiniteLoop, args=())

      #  monitor_thread.start()
      #  time.sleep(5)
        infiniteThread.start()

      #  monitor_thread.join()
        infiniteThread.join()
    except KeyboardInterrupt:
        # Cancels order updates
        asyncio.run(monitorOrders("uor+{}"))

        with open("cancelled_orders.json", "w") as f:
            json.dump({"cancelled_orders": cancelled_orders}, f, indent=4)
