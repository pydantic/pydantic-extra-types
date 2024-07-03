.DEFAULT_GOAL := all
sources = pydantic_extra_types tests

.PHONY: install
install:
	python -m pip install -U pip
	pip install -r requirements/all.txt
	pip install -e .

.PHONY: refresh-lockfiles
refresh-lockfiles:
	@echo "Updating requirements/*.txt files using pip-compile"
	find requirements/ -name '*.txt' ! -name 'all.txt' -type f -delete
	pip-compile -q --no-emit-index-url --resolver backtracking -o requirements/linting.txt requirements/linting.in
	pip-compile -q --no-emit-index-url --resolver backtracking -o requirements/testing.txt requirements/testing.in
	pip-compile -q --no-emit-index-url --resolver backtracking --extra all -o requirements/pyproject.txt pyproject.toml
	pip install --dry-run -r requirements/all.txt

.PHONY: format
format:
	ruff check --fix $(sources)
	ruff format $(sources)

.PHONY: lint
lint:
	ruff check $(sources)
	ruff format --check $(sources)

.PHONY: mypy
mypy:
	mypy pydantic_extra_types

.PHONY: test
test:
	coverage run -m pytest --durations=10

.PHONY: testcov
testcov: test
	@echo "building coverage html"
	@coverage html

.PHONY: testcov-compile
testcov-compile: build-trace test
	@echo "building coverage html"
	@coverage html

.PHONY: all
all: lint mypy testcov

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
	rm -rf coverage.xml
	rm -rf .ruff_cache

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files --show-diff-on-failure
