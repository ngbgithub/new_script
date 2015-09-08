# This is a small, minimalist wrapper for Make around Python's distutils.

PYTHON := python3
.DEFAULT_GOAL := build

build:
	$(PYTHON) setup.py build

clean:
	find . -type f \( -name "*~" -o -name "*.pyc" \) -exec rm -vf {} \;

install:
	$(PYTHON) setup.py install

sdist:
	$(PYTHON) setup.py sdist

.PHONY: build clean install sdist

