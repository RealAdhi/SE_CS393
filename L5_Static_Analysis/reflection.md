# Lab 5 — Reflection

1. **Which issues were the easiest to fix and why?** Flake8 spacing/blank-line findings and Pylint naming/docstring findings: they are mechanical, local edits with no behaviour change.
2. **Did the tools report any false positives?** Bandit B105 flagged the demo gateway key and B311 flagged `random` for what is only a demo OTP; both are still worth fixing in a real wallet, so they were treated as real. The unused `merchantType` was genuine, not a false positive.
3. **How would you integrate these tools into a real workflow?** Run Flake8/Pylint/Bandit as pre-commit hooks and as a required CI job on every pull request, failing the build on Bandit High/Medium findings or a Pylint score below a threshold (e.g. 9.5).
4. **What tangible improvements did you see?** Pylint rose from 5.69 to 10.00, all security findings were removed (PIN hashing, temp files, OTP randomness, secrets out of source), and the code became consistent and documented, making it easier to read and review.
