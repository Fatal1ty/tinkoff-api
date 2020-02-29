.PHONY: devel test mypy

devel:
	pip install -e .
test: mypy
mypy:
	mypy tinkoff
