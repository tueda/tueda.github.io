# Requirements: python>=3.11, poetry>=2.0 and GNU make

export PYTHONPATH=$(shell pwd)/python

build:
	poetry run mkdocs build --strict

install:
	git submodule update --init
	poetry install --no-root --no-interaction

latex:
	poetry run make -C latex

serve:
	poetry run mkdocs serve

mostlyclean:
	rm -rf */*.pyc
	make -C latex mostlyclean

clean:
	rm -rf site */*.pyc
	make -C latex clean

.PHONY: latex
