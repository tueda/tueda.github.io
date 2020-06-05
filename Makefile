# Requirements: python>=3.5, poetry>=1.0 and GNU make

export PYTHONPATH=$(shell pwd)/ext

build:
	poetry run mkdocs build

install:
	poetry install

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
