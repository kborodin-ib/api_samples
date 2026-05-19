#! /usr/bin/env python3

import logging
import signal
import socket
import sys
import threading
import time
from typing import Optional

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

# -- Config
HOST = "172.23.208.1"
PORT = 4002# 7497 TWS paper | 7496 TWS live | 4002 GW paper | 4001 GW live
TARGET = 99  # IB hard limit to verify
CONNECT_TIMEOUT = 8  # Seconds to wait for nextValidId handshake
SPAWN_DELAY = 0.1  # Seconds between spawning each thread
HOLD_TIME = 3  # Seconds to hold all connections open simultaneously

# -- Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-5s] %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)

stop_event = threading.Event()


# -- Result
class Result:
    def __init__(self, cid):
        self.cid = cid
        self.ok = False
        self.ms = 0.0
        self.err_code = None  # type: Optional[int]
        self.err_msg = None  # type: Optional[str]
        self.note = ""


# -- Wrapper + Client
class Wrapper(EWrapper):
    def __init__(self, result, ready):
        super().__init__()
        self._r = result
        self._ready = ready  # type: threading.Event

    def nextValidId(self, orderId):
        self._r.ok = True
        self._ready.set()

    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        self._r.err_code = errorCode
        self._r.err_msg = errorString
        self._r.err_time = errorTime
        if errorCode in (326, 504, 509):
            if errorCode == 326:
                self._r.note = "duplicate_id"
            self._ready.set()

    def connectionClosed(self):
        if not self._r.ok:
            self._r.note = self._r.note or "server_closed"
            self._ready.set()


class Client(EClient):
    def __init__(self, wrapper):
        super().__init__(wrapper)


# -- Safe disconnect
def safe_disconnect(c):
    """
    Disconnect a Client instance.
    Handles None, already-disconnected clients, and AttributeError cleanly.
    """
    if c is None:
        log.debug("safe_disconnect: client is None, nothing to disconnect")
        return
    try:
        c.disconnect()
    except AttributeError as e:
        log.warning("safe_disconnect: AttributeError during disconnect -- %s", e)
    except Exception as e:
        log.warning("safe_disconnect: unexpected error during disconnect -- %s", e)


# -- Single probe
def probe(cid):
    """
    Open one connection, block until connected or failed, return (Result, client).
    Caller is responsible for disconnecting the client.
    """
    r = Result(cid)
    ready = threading.Event()
    w = Wrapper(r, ready)
    c = Client(w)

    try:
        s = socket.create_connection((HOST, PORT), timeout=3)
        s.close()
    except OSError as e:
        r.err_msg = "TCP preflight failed: %s" % e
        r.note = "tcp_error"
        return r, None

    t0 = time.perf_counter()

    try:
        c.connect(HOST, PORT, clientId=cid)
    except OSError as e:
        r.err_msg = "connect() raised: %s" % e
        r.note = "socket_error"
        return r, None

    reader = threading.Thread(target=c.run, daemon=True, name="rd-%d" % cid)
    reader.start()

    fired = ready.wait(timeout=CONNECT_TIMEOUT)
    r.ms = round((time.perf_counter() - t0) * 1000, 1)

    if not fired:
        r.note = "timeout"

    return r, (c if r.ok else None)


# -- Sweep
def run_sweep():
    """
    Spawn TARGET simultaneous connections, hold them all open, then tear down.
    Returns a list of Result objects.
    """
    log.info("Attempting %d simultaneous connections to %s:%d", TARGET, HOST, PORT)

    results = []
    live_clients = []
    lock = threading.Lock()

    def worker(cid):
        r, c = probe(cid)
        with lock:
            results.append(r)
            if c:
                live_clients.append(c)
        status = "OK " if r.ok else "FAIL"
        log.info(
            " %s cid=%-5d %6.0f ms %s",
            status,
            cid,
            r.ms,
            r.note or r.err_msg or "",
        )

    threads = []
    for cid in range(1, TARGET + 1):
        if stop_event.is_set():
            break
        t = threading.Thread(target=worker, args=(cid,), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(SPAWN_DELAY)

    for t in threads:
        t.join(timeout=CONNECT_TIMEOUT + 2)

    log.info(
        "Connections alive: %d / %d -- holding for %ds",
        len(live_clients),
        TARGET,
        HOLD_TIME,
    )
    time.sleep(HOLD_TIME)

    for c in live_clients:
        safe_disconnect(c)

    return results


# -- Report
def report(results):
    ok = [r for r in results if r.ok]
    fail = [r for r in results if not r.ok]

    by_note = {}
    for r in fail:
        k = r.note or "unknown"
        by_note[k] = by_note.get(k, 0) + 1

    sep = "-" * 52
    print("")
    print("=" * 52)
    print(" IB Max-Connection Test | %s:%d" % (HOST, PORT))
    print("=" * 52)
    print(" Target : %d (IB default hard limit)" % TARGET)
    print(" Successful : %d" % len(ok))
    print(" Failed : %d" % len(fail))

    for reason, cnt in sorted(by_note.items(), key=lambda x: -x[1]):
        print(" %-20s : %d" % (reason, cnt))

    if ok:
        lats = [r.ms for r in ok]
        print(
            " Latency ms : min=%.0f avg=%.0f max=%.0f"
            % (min(lats), sum(lats) / len(lats), max(lats))
        )

    print(sep)

    if len(ok) >= TARGET:
        print(" PASS -- all %d connections succeeded" % TARGET)
    else:
        print(" FAIL -- only %d of %d connections succeeded" % (len(ok), TARGET))
        first_fail = next(
            (r for r in sorted(results, key=lambda x: x.cid) if not r.ok), None
        )
        if first_fail:
            print(
                " First failure: cid=%d code=%s note=%s"
                % (
                    first_fail.cid,
                    first_fail.err_code or "n/a",
                    first_fail.note or first_fail.err_msg or "n/a",
                )
            )

    print("=" * 52)
    print("")


# -- Graceful Ctrl-C
signal.signal(signal.SIGINT, lambda *_: stop_event.set())
signal.signal(signal.SIGTERM, lambda *_: stop_event.set())


# -- Main
def main():
    log.info(
        "IB Max-Connection Test host=%s port=%d target=%d", HOST, PORT, TARGET
    )

    try:
        socket.create_connection((HOST, PORT), timeout=4).close()
    except AttributeError as e:
        log.error(
            "Socket object is None or malformed -- %s", e
        )
        log.error(
            "This is likely a Python environment issue. Check your installation."
        )
        sys.exit(1)
    except OSError as e:
        log.error("Cannot reach %s:%d -- %s", HOST, PORT, e)
        log.error("Start TWS or IB Gateway, enable API connections, then retry.")
        sys.exit(1)

    results = run_sweep()
    report(results)


if __name__ == "__main__":
    main()
