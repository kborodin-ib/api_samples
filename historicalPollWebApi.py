import asyncio
import httpx
import time
import sys

POLL_INTERVAL = 5 # seconds
RPS_LIMIT = 10 # max 10 request per second
URL = "https://localhost:5000/v1/api/iserver/marketdata/history"
CONIDS = [265598, 9939, 10517, 14241431, 10627, 11032, 11574, 2585629]

# Global rate limiter
rate_limiter = asyncio.Semaphore(RPS_LIMIT)

async def limited_get(client, url, params):
    async with rate_limiter:
        try:
            response = await client.get(url, params=params)
            return response
        except httpx.RequestError as exc:
            print(f"[{time.strftime('%X')}] Reques error: {exc}")
            return None

async def poll_history(conid):

    request_params = {
        'conid': conid,
        'exchange': 'SMART',
        'period': '3h',
        'bar': '1min',
        'outsideRth': True,
        'direction': 1,
        'barType': 'last'
 #       'startTime': '20250513-00:00:00'
    }

    async with httpx.AsyncClient(verify=False) as client:
        while True:
            try:
                response = await limited_get(client, URL, request_params)

                retry_503 = False

                if response.status_code == 503:
                    print(f"[{time.strftime('%X')}] Server unavailable. Retrying after {POLL_INTERVAL} seconds")
                    retry_503 = True

                elif response.status_code == 429:
                    print(f"[{time.strftime('%X')}] Too many requests. Try again in 10 minutes.")
                    print(response.text)
                    sys.exit()

                elif response.status_code == 400:
                    print(f"[{time.strftime('%X')}] No bridge. Reauthenticate the session.")
                    print(response.text)
                    sys.exit()

                elif response.status_code == 401:
                    print(f"[{time.strftime('%X')}] Not authenticated. Reauthenticate the session.")
                    print(response.text)
                    sys.exit()

                elif response.status_code == 200:
                    print(f"[{time.strftime('%X')}] Success")
                    print(response.text)

                else:
                    print(f"[{time.strftime('%X')}] Received status: {response.status_code})")
                    print(response.text)

                if retry_503:
                    await asyncio.sleep(2)
                    continue # Retry immediately


            except httpx.RequestError as exc:
                print(f"[{time.strftime('%X')}] Request errror {exc}")

            await asyncio.sleep(POLL_INTERVAL)

async def main():
    tasks_conid_list = [poll_history(conid) for conid in CONIDS]
    tasks_single_conid = [poll_history(356068332)]
    await asyncio.gather(*tasks_single_conid)

if __name__ == "__main__":
    asyncio.run(main())
