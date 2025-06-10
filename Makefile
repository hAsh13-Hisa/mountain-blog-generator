.PHONY: help install install-dev test lint format clean run

help:
	@echo "Available commands:"
	@echo "  make install      Install production dependencies"
	@echo "  make install-dev  Install all dependencies including dev"
	@echo "  make test         Run tests"
	@echo "  make lint         Run linting (flake8, mypy)"
	@echo "  make format       Format code (black, isort)"
	@echo "  make clean        Clean up temporary files"
	@echo "  make run          Run the CLI application"

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev,scheduler]"
	pre-commit install

test:
	pytest

test-cov:
	pytest --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -rf build/ dist/

run:
	python -m src.presentation.cli

# Development shortcuts
dev-setup: install-dev

check: lint test

all: format lint test