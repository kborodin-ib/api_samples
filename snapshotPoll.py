import asyncio
import httpx
import time
import sys

POLL_INTERVAL = 0.1 # seconds
RPS_LIMIT = 10 # max 10 request per second
URL = "https://localhost:5000/v1/api/iserver/marketdata/snapshot"
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

async def poll_snapshot(conid_list):

    request_params = {
        'conids': ','.join(str(i) for i in conid_list),
        'fields': '7655,84,86,88,85,31,7762,7697',
    }

    print(request_params)

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
                sys.exit()

            await asyncio.sleep(POLL_INTERVAL)

async def main():
    # Handles single task
    tasks = [poll_snapshot(CONIDS)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
