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

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

lint:
	ruff check .

typecheck:
	mypy .

test:
	pytest --no-cov

coverage:
	pytest

quality: lint typecheck coverage

check: quality

format:
	ruff format .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete