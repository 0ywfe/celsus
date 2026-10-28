import sys
from pathlib import Path

# Lets the tests import fake_api.py from this folder.
sys.path.insert(0, str(Path(__file__).parent))
