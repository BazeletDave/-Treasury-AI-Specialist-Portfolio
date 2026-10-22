# GRI Institutional AI Assurance Engine (Research Prototype)

A standard library Python prototype that combines baseline learned anomaly scores with deterministic institutional policy checks.

**Important:** The statistical model fits means and standard deviations to baseline numeric observations. It is a simple unsupervised anomaly model, not a trained threat classifier, proof of security, or an independently validated production control. Baseline poisoning, missing features, untrusted input and concept drift remain open risks. Do not use this as the sole authorization control.

## Run

From this directory, execute `python -m unittest -v`.

Create a JSON array of at least three baseline records and one JSON observation. Required nonnegative numeric fields: `privilege_count`, `unapproved_tool_calls`, `unpatched_critical`, `unexpected_egress`, `missing_attestations`. Optional booleans: `production`, `human_approval`.

`python assurance.py --baseline baseline.json --input observation.json`

Output includes PASS, REVIEW or BLOCK, numeric anomaly indicators, and policy findings. Exit codes: 0 PASS, 1 REVIEW, 2 BLOCK. No external network or institutional systems are accessed.

## Limits and next work

The tool currently evaluates supplied evidence; it does not independently discover vulnerabilities, validate patch provenance, inspect live runtime memory, or enforce production deployments. Future work should add signed evidence ingestion, robust input schemas, independent vulnerability feeds, threat model tests, calibrated detection, drift assessment, review workflows and controlled CI integration. Use synthetic or explicitly authorized data only.
