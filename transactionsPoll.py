
import asyncio
import httpx
import json
import logging
from datetime import datetime

# Generate timestamped log filename
timestamp = datetime.now().strftime("%Y%m%d")
log_filename = f"transactions_{timestamp}.log"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)


# --- Constants ---
POLL_INTERVAL = 5  # seconds
RPS_LIMIT = 10     # max 10 requests per second
URL = "https://localhost:5000/v1/api/pa/transactions"
CONIDS = [265598, 9939, 10517, 14241431, 10627, 11032, 11574, 2585629, 14904, 115826951]
ACCID = "DU6036902"

headers = {
  'Content-Type': 'application/json'
}


# --- Global Rate Limiter and Shutdown Event ---
rate_limiter = asyncio.Semaphore(RPS_LIMIT)
shutdown = asyncio.Event()

# --- Limited GET Request ---
async def limited_post(client, url, payload):
    async with rate_limiter:
        try:
            response = await client.post(url, data=payload, headers=headers)
            return response
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            return None

# --- Poll History ---
async def poll_transactions():
    logging.info(f"Requesting transactions history")

    payload = json.dumps({
        "acctIds": [
            "DU6036902",
        ],
        "conids": CONIDS,
        "currency": "EUR",
        "days": 999
    })

    async with httpx.AsyncClient(verify=False) as client:
        url = URL
        while not shutdown.is_set():
            try:
                response = await limited_post(client, url, payload)

                retry_503 = False

                if response is None:
                    logging.warning(f"[{ACCID}] No response received. Retrying...")
                    await asyncio.sleep(POLL_INTERVAL)
                    continue

                if response.status_code == 503:
                    logging.warning(f"[{ACCID}] Server unavailable. Retrying after {POLL_INTERVAL} seconds")
                    retry_503 = True

                elif response.status_code == 429:
                    logging.warning(f"[{ACCID}] Too many requests. Try again in 10 minutes.")
                    logging.debug(response.text)
                    return

                elif response.status_code == 400:
                    logging.error(f"[{ACCID}] No bridge. Reauthenticate the session.")
                    logging.debug(response.text)
                    return

                elif response.status_code == 401:
                    logging.error(f"[{ACCID}] Not authenticated. Reauthenticate the session.")
                    logging.debug(response.text)
                    return

                elif response.status_code == 200:
                    logging.info(f"[{ACCID}] Success - URL: {url} - payload: {payload}")
                    logging.debug(json.dumps(json.loads(response.text), indent=4))

                elif response.status_code == 500:
                    logging.debug(response.text)
                    if "Cannot deserialize value" in response.text:
                        logging.debug("exiting due to error 500")
                        sys.exit()

                else:
                    logging.warning(f"[{ACCID}] Unexpected status: {response.status_code} - Switching to BETA URL")

                if retry_503:
                    await asyncio.sleep(2)
                    continue

            except httpx.RequestError as exc:
                logging.error(f"[{conid}] Request error: {exc}")

            except KeyboardInterrupt:
                logging.info(f"[{conid}] KeyboardInterrupt received. Shutting down...")
                shutdown.set()

            await asyncio.sleep(POLL_INTERVAL)

# --- Main ---
async def main():
    logging.info("Initializing polling session...")
    tasks = [asyncio.create_task(poll_transactions())]

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        logging.info("Tasks were cancelled.")
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Cancelling tasks...")
        shutdown.set()
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

# --- Entry Point ---
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Polling interrupted by user. Exiting.")
