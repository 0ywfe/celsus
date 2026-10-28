"""paper-replicator: read a paper, rerun its analysis on public data, check its numbers."""

# The product name lives here and in pyproject.toml's `name`, nowhere else.
# Everything that shows the name (CLI title, report header and footer) reads it from here.
PRODUCT_NAME = "paper-replicator"

DISCLAIMER = (
    "Not financial advice. It checks what academics published. "
    "AI can make mistakes: check the code and data in the report."
)
