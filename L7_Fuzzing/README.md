# Lab 7 — Fuzzing for Input Validation Bugs (Thermostat Control)

- `before/` — original `thermostat_control.py` + completed Hypothesis tests (fail on original)
- `thermostat_control.py` — hardened version (returns `None` on invalid input; validates type, format, range, NaN/inf)
- `test_thermostat_control.py` — Hypothesis tests (`st.text() | st.none()`) for all three functions
- `step*.txt` — captured terminal output; `Lab7_Fuzzing_Report.pdf` — the same as a PDF

Bugs found by fuzzing: `None` input (TypeError/AttributeError), empty string / empty elements (ValueError), missing `:` separator, non-numeric minute (ValueError), plus unvalidated ranges and `nan`/`inf`.

Run: `pip install hypothesis pytest` then `python -m pytest test_thermostat_control.py`.
