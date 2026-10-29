"""The operator's SEC contact reaches sec.gov and no other host (29 Oct: a builder sent it to Yale's and HEC
Lausanne's servers by copying SEC_USER_AGENT into every request)."""

import json
import subprocess
import sys
from pathlib import Path

import modal

from paper_replicator import sandbox as sandbox_module

LIB = Path(sandbox_module.__file__).parent / "sandbox_lib"
CONTACT = "Jane Tester jane@example.com"

# Runs inside a fresh interpreter with the hook loaded, as every sandbox Python process is: a local server records
# the headers each request arrives with.
CLIENT = r"""
import http.server, json, os, threading, urllib.request
import requests
import sec_contact

seen = []
class Record(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        seen.append({"ua": self.headers.get("User-Agent"), "from": self.headers.get("From")})
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *args):
        pass

server = http.server.HTTPServer(("127.0.0.1", 0), Record)
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{server.server_port}/"
contact = open(os.environ["SEC_CONTACT_FILE"]).read().strip()

requests.get(url, headers={"User-Agent": os.environ["SEC_USER_AGENT"]})           # the env var, as builders do
requests.get(url, headers={"User-Agent": "replication " + contact, "From": contact})  # the contact itself
urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": os.environ["SEC_USER_AGENT"]}))
requests.get(url, headers={"User-Agent": "Mozilla/5.0 research"})                 # an ordinary header is left alone
sec_contact.is_sec = lambda host: True                                            # now the same host stands for sec.gov
requests.get(url)                                                                 # no User-Agent of its own
requests.get(url, headers={"User-Agent": "someone else <author@university.edu>"})
print(json.dumps(seen))
"""


def received(tmp_path):
    (tmp_path / "contact").write_text(CONTACT + "\n")
    env = {"PATH": "/usr/bin:/bin", "PYTHONPATH": str(LIB), "SEC_USER_AGENT": sandbox_module.STAND_IN,
           "SEC_CONTACT_FILE": str(tmp_path / "contact")}
    out = subprocess.run([sys.executable, "-c", CLIENT], env=env, capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_other_hosts_get_a_neutral_user_agent_and_sec_gov_gets_the_contact(tmp_path):
    from_env, from_contact, by_urllib, ordinary, sec_default, sec_replaced = received(tmp_path)
    neutral = "Mozilla/5.0 (compatible; research script)"
    assert from_env == {"ua": neutral, "from": None}
    assert from_contact == {"ua": neutral, "from": neutral}
    assert by_urllib["ua"] == neutral
    assert ordinary["ua"] == "Mozilla/5.0 research"
    assert sec_default["ua"] == CONTACT and sec_replaced["ua"] == CONTACT   # sec.gov always gets the operator's


def test_sec_hosts_are_sec_gov_and_its_subdomains_only(tmp_path):
    (tmp_path / "contact").write_text(CONTACT)
    check = ("import sec_contact as s, json; print(json.dumps([s.is_sec(h) for h in "
             "['sec.gov', 'www.sec.gov', 'efts.sec.gov', 'data.sec.gov.', 'notsec.gov', 'sec.gov.example.com', "
             "'econ.yale.edu', None]]))")
    env = {"PATH": "/usr/bin:/bin", "PYTHONPATH": str(LIB), "SEC_CONTACT_FILE": str(tmp_path / "contact")}
    out = subprocess.run([sys.executable, "-c", check], env=env, capture_output=True, text=True, timeout=60)
    assert json.loads(out.stdout) == [True, True, True, True, False, False, False, False]


class Box:
    def __init__(self):
        self.files = {}
        outer = self

        class FS:
            def make_directory(self, path):
                pass

            def write_text(self, content, path):
                outer.files[path] = content

            def copy_from_local(self, local, path):
                pass

        self.filesystem = FS()


def test_the_contact_is_never_in_the_sandboxs_environment(monkeypatch, tmp_path):
    created = {}
    monkeypatch.setattr(modal.App, "lookup", staticmethod(lambda *a, **k: None))
    monkeypatch.setattr(sandbox_module, "image", lambda packages=(): ("image", packages))

    def create(**kwargs):
        created.update(kwargs)
        return Box()

    monkeypatch.setattr(modal.Sandbox, "create", staticmethod(create))
    box = sandbox_module._start(market_cache=tmp_path, env={"SEC_USER_AGENT": CONTACT}, lifetime_s=60,
                                packages=("xlrd==2.0.1",))
    assert CONTACT not in json.dumps(created.get("env")) and "secrets" not in created
    assert created["env"]["SEC_USER_AGENT"] == sandbox_module.STAND_IN
    assert created["image"] == ("image", ("xlrd==2.0.1",))
    hooks = sandbox_module.HOOKS
    assert box.files[f"{hooks}/sec_contact"] == CONTACT
    assert box.files[f"{hooks}/sitecustomize.py"].startswith("import sec_contact")
    assert {f"{hooks}/sec_contact.py", f"{hooks}/data_sources.py"} <= set(box.files)
