"""Endpoints a checkout adds for itself, from providers.local.json at the repo root if the file exists.

The product runs on any OpenAI-compatible endpoint. Meta's is built in; others are added in that file,
which each checkout keeps to itself:

    {"<name>": {"base_url": "https://.../v1", "key_env": "<ENV VAR WITH THE KEY>",
                "json_schema": true,        # strict json_schema output; false: json_object + schema in the prompt
                "reasoning_effort": true,   # accepts reasoning_effort
                "prices": {"<model id>": [0.0, 0.0, 0.0]}}}   # USD per 1M tokens: cached input, input, output
"""

from __future__ import annotations

import json
from pathlib import Path

from .runs import ROOT

LOCAL_FILE = ROOT / "providers.local.json"


def load(path: Path = LOCAL_FILE) -> dict:
    return json.loads(path.read_text()) if path.is_file() else {}
