.PHONY: evals evals-roundtrip

# Run the idm-standards plugin eval harness (audit-only). See evals/README.md.
evals:
	python evals/run_evals.py

# Run the eval harness including the audit -> fix -> audit round-trip (slower, more tokens).
evals-roundtrip:
	python evals/run_evals.py --roundtrip
