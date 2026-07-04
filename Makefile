# ==============================================================================
# PyRestKit Makefile
# ==============================================================================

PYTHON ?= python3
PIP ?= pip3

.PHONY: \
	install \
	install-dev \
	lint \
	typecheck \
	test \
	coverage \
	quality \
	check \
	format \
	clean

# ------------------------------------------------------------------------------
# Installation
# ------------------------------------------------------------------------------

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements-dev.txt

# ------------------------------------------------------------------------------
# Code Quality
# ------------------------------------------------------------------------------

lint:
	$(PYTHON) -m ruff check .

typecheck:
	$(PYTHON) -m mypy .

format:
	$(PYTHON) -m ruff format .

# ------------------------------------------------------------------------------
# Testing
# ------------------------------------------------------------------------------

test:
	$(PYTHON) -m pytest --no-cov

coverage:
	$(PYTHON) -m pytest \
		--cov=pyrestkit \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-report=xml

quality: lint typecheck coverage

check: quality

# ------------------------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------------------------

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete