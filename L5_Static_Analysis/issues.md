# Lab 5 — Issue Table (digital_wallet.py)

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Weak SHA-1 PIN hash (B324) | Security (High) | 14 | `hashlib.sha1` is broken and unsalted/fast, unsuitable for PINs | Salted PBKDF2-HMAC-SHA256, compared with `hmac.compare_digest` |
| `tempfile.mktemp` (B306) | Security (Medium) | 60 | Race condition: name returned without creating the file | `tempfile.mkstemp`, close the descriptor, return the path |
| Hard-coded secrets (B105) | Security (Low) | 6 | Gateway key and PIN in source | Read from environment (`GATEWAY_SECRET`, `WALLET_PIN`), demo-only defaults |
| `random` for OTP (B311) | Security (Low) | 64 | Predictable PRNG for a one-time password | `secrets.randbelow` |
| Mutable default arg (W0102) | Bug | 17 | `log=[]` shared across calls | Default `None`, create/skip inside the function |
| Global statement (W0603) | Design | 28 | `global daily_limit` | Keep limit in a `wallet_settings` dict |
| Unused argument (W0613) | Code smell | 50 | `merchantType` never used | Removed from `cashback_for` and its caller |
| camelCase names / missing docstrings (C0103, C0114, C0116) | Style | many | Not PEP 8 snake_case, no docstrings | Renamed functions/variables, added docstrings |
| E261 / E225 / E231 / E305 / E501 (Flake8) | Style | 1, 76-80 | Spacing, blank lines, line length | Reformatted; wrapped `main()` in `if __name__ == "__main__"` |

Results: Pylint 5.69 -> 10.00, Bandit 4 issues -> 0, Flake8 5 -> 0. Program output unchanged (apart from the random OTP).
