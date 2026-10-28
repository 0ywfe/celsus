Scripts Muse Spark wrote during live runs on arXiv 2512.06144 (28 Oct 2026), kept as a regression corpus
for the guards. Each file name says what the guards must find in it.

- direct_yfinance.py: run 757250, attempt 2, which imports yfinance directly.
- exponent_1e12.py: run c3ab42, attempt 2, which has `1e12` (not the paper's 12).
- cut_to_54.py: run 91ed39, attempt 1, which cuts the sample to the paper's 54 (`SAMPLE_TARGET = 54`).
- calendar_months.py: run 51e7e9, attempt 1, which has months (`12`), not the paper's count.
- spec_2512.06144.json: the extractor's spec from run 51e7e9.
- notes_string_54.py: run 5d7c16, attempt 1, which mentions the paper's 54 only in a notes string.
