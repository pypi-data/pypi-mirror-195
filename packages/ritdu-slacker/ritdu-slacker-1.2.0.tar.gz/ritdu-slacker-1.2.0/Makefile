PYTHON = $(shell which python)

help:
	@echo "---------------HELP-----------------"
	@echo "To dev the project type make dev"
	@echo "To build the project type make build"
	@echo "To install the project type make install"
	@echo "To format the project type make fmt"
	@echo "To clean the project type make clean"
	@echo "------------------------------------"

install:
	pip install pip wheel --upgrade
	pip install .

install-dev:
	pip install pip wheel --upgrade
	pip install '.[develop]'

build:
	python setup.py build

check:
	python setup.py check --strict

clean:
	git clean -fd

clean-dist:
	rm -rf dist/*

dev: vscode fmt install-dev

.PHONY: dist
dist: check
	python setup.py sdist

fmt:
	python -m black .

test:
	python setup.py test

publish: clean-dist dist
	python -m twine upload dist/*

vscode:
	@mkdir -p .vscode
	@echo "{\"python.defaultInterpreterPath\": \"$(PYTHON)\", \"python.terminal.activateEnvInCurrentTerminal\": true}" > .vscode/settings.json
