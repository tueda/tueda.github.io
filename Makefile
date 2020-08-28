# Requirements: python>=3.5, poetry>=1.0 and GNU make

export PYTHONPATH=$(shell pwd)/python

build:
	poetry run mkdocs build

install:
	git submodule update --init
	poetry install

latex:
	poetry run make -C latex

serve:
	poetry run mkdocs serve

deploy:
	poetry run mkdocs gh-deploy --remote-branch master

mostlyclean:
	rm -rf */*.pyc
	make -C latex mostlyclean

clean:
	rm -rf site */*.pyc
	make -C latex clean

.PHONY: latex
