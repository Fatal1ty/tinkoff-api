.PHONY: devel test mypy

all: devel test
devel:
	pip install -e .
	pip install -r requirements-dev.txt
test: mypy
mypy:
	mypy tinkoff
