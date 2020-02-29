.PHONY: devel test mypy

all: devel test
devel:
	pip install --upgrade pip
	pip install -e .
	pip install -r requirements-dev.txt
test: mypy flake
mypy:
	mypy tinkoff
flake:
	flake8 tinkoff
