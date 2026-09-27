.PHONY: help setup test test-unit test-integration test-security test-eval run-api run-frontend run-mcp run-a2a clean build-docker tf-init tf-plan

help:
	@echo "CardGuard AI - Makefile Commands"
	@echo "  setup            Install dependencies"
	@echo "  generate-data    Generate synthetic transactions and policies"
	@echo "  test             Run all test suites"
	@echo "  test-unit        Run unit tests"
	@echo "  test-eval        Run evaluation framework"
	@echo "  run-api          Start FastAPI service"
	@echo "  run-frontend     Start React analyst dashboard"
	@echo "  build-docker     Build container image"

setup:
	pip install -e .[dev]

generate-data:
	python scripts/generate_synthetic_data.py

test:
	pytest tests/

test-unit:
	pytest tests/unit/

test-integration:
	pytest tests/integration/

test-security:
	pytest tests/security/ tests/adversarial/

test-eval:
	python scripts/run_eval.py

run-api:
	uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	cd frontend && npm run dev

build-docker:
	docker build -t cardguard-ai .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
