
import asyncio
import httpx
import time
import logging
from datetime import datetime

# Generate timestamped log filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"poll_history_{timestamp}.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
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
URL = "https://localhost:5000/v1/api/iserver/marketdata/history"
URL_BETA = "https://localhost:5000/v1/api/hmds/history"
CONIDS = [265598, 9939, 10517, 14241431, 10627, 11032, 11574, 2585629]

# --- Global Rate Limiter and Shutdown Event ---
rate_limiter = asyncio.Semaphore(RPS_LIMIT)
shutdown = asyncio.Event()

# --- Limited GET Request ---
async def limited_get(client, url, params):
    async with rate_limiter:
        try:
            response = await client.get(url, params=params)
            return response
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            return None

# --- Poll History ---
async def poll_history(conid):
    logging.info(f"Starting session for conid: {conid}")

    request_params = {
        'conid': conid,
        'exchange': 'SMART',
        'period': '1d',
        'bar': '1min',
        'outsideRth': True,
        'direction': 1,
        'startTime': '20250703-23:59:59'
    }

    request_params_beta = {
        'conid': conid,
        'exchange': 'SMART',
        'period': '1m',
        'bar': '1h',
        'outsideRth': True,
        'direction': 1,
        'startTime': '20250703-23:59:59',
        "barType": "Inventory"
    }

    async with httpx.AsyncClient(verify=False) as client:
        url = URL
        params = request_params
        while not shutdown.is_set():
            try:
                response = await limited_get(client, url, params)

                retry_503 = False

                if response is None:
                    logging.warning(f"[{conid}] No response received. Retrying...")
                    await asyncio.sleep(POLL_INTERVAL)
                    continue

                if response.status_code == 503:
                    logging.warning(f"[{conid}] Server unavailable. Retrying after {POLL_INTERVAL} seconds")
                    retry_503 = True

                elif response.status_code == 429:
                    logging.warning(f"[{conid}] Too many requests. Try again in 10 minutes.")
                    logging.debug(response.text)
                    return

                elif response.status_code == 400:
                    logging.error(f"[{conid}] No bridge. Reauthenticate the session.")
                    logging.debug(response.text)
                    return

                elif response.status_code == 401:
                    logging.error(f"[{conid}] Not authenticated. Reauthenticate the session.")
                    logging.debug(response.text)
                    return

                elif response.status_code == 200:
                    logging.info(f"[{conid}] Success - URL: {url} - Params: {params}")
                    logging.debug(response.text)

                else:
                    logging.warning(f"[{conid}] Unexpected status: {response.status_code} - Switching to BETA URL")
                    logging.debug(response.text)
                    url = URL_BETA
                    params = request_params_beta

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
    tasks = [asyncio.create_task(poll_history(677037673))]

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
