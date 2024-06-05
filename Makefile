setup-dev: setup-python setup-pre-commit

setup-python:
	pip install --force-reinstall -e .[dev]

setup-pre-commit:
	pre-commit install

lint:
	pre-commit run --all-files

test:
	pytest -s -v tests
