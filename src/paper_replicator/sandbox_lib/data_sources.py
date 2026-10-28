"""Loaded at start-up in the clean run (as sitecustomize): records every host the script fetches from.

Python's audit hooks (PEP 578) see each name lookup a Python socket makes, so requests, urllib, pandas
and the market-data module are all covered. The record is rewritten on each new host, so a run cut off
by its time limit still leaves it behind. It holds host names only: nothing from headers or URLs.
"""

import json
import os
import sys

_hosts: list[str] = []
_record = os.path.join(os.environ.get("WORK_DIR", "/work"), "data_sources.json")


def _seen(event: str, args: tuple) -> None:
    if event != "socket.getaddrinfo" or not args[0]:
        return
    host = args[0].decode(errors="replace") if isinstance(args[0], bytes) else str(args[0])
    if host in _hosts:
        return
    _hosts.append(host)
    try:
        with open(_record, "w") as f:
            json.dump(_hosts, f)
    except OSError as error:  # never break the script's fetch over the record; say so where the run log shows it
        sys.stderr.write(f"data source record not written: {error}\n")


sys.addaudithook(_seen)
