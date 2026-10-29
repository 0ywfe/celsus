"""Loaded at start-up in every Python process of a sandbox: the operator's SEC contact goes to sec.gov and
nowhere else.

SEC asks automated tools to declare a contact in the User-Agent. On 29 Oct a builder copied SEC_USER_AGENT into
its requests to Yale's and HEC Lausanne's servers. So the contact is not in the environment: SEC_USER_AGENT
holds a stand-in, and this module, which reads the contact from a file, writes it into the User-Agent of every
request to a sec.gov host (edgartools' form: the client attaches the identity to SEC requests only). A request to
any other host that carries the stand-in or the contact in a header gets a neutral User-Agent in its place, so
the fetch still works. It patches http.client, which requests, urllib and pandas all send through; a
command-line tool such as curl gets only the stand-in.
"""

import http.client
import os

STAND_IN = os.environ.get("SEC_USER_AGENT", "")  # the sandbox sets it to a stand-in (sandbox.STAND_IN)
NEUTRAL = "Mozilla/5.0 (compatible; research script)"
CONTACT_FILE = os.environ.get("SEC_CONTACT_FILE", "/opt/hooks/sec_contact")

try:
    with open(CONTACT_FILE) as f:
        _contact = f.read().strip()
except OSError:
    _contact = ""


def is_sec(host: str | None) -> bool:
    host = (host or "").lower().rstrip(".")
    return host == "sec.gov" or host.endswith(".sec.gov")


def header_value(host: str | None, name: str, value: str, contact: str) -> str:
    """What a header carries on the wire: the contact as sec.gov's User-Agent, never anything with the contact or
    its stand-in to another host."""
    if is_sec(host):
        return contact if name.lower() == "user-agent" and contact else value
    if (STAND_IN and STAND_IN in value) or (contact and contact in value):
        return NEUTRAL
    return value


_putheader = http.client.HTTPConnection.putheader


def _send(self, header, *values):
    name = header.decode("latin-1") if isinstance(header, bytes) else str(header)
    host = getattr(self, "_tunnel_host", None) or self.host
    sent = [header_value(host, name, v.decode("latin-1") if isinstance(v, bytes) else str(v), _contact)
            for v in values]
    return _putheader(self, header, *sent)


http.client.HTTPConnection.putheader = _send
