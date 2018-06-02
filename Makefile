# Prerequisites:
#   pip install markdown-include mkdocs mkdocs-material bibtexparser

build:
	PYTHONPATH=$$(pwd)/ext mkdocs build

serve:
	PYTHONPATH=$$(pwd)/ext mkdocs serve

deploy:
	PYTHONPATH=$$(pwd)/ext mkdocs gh-deploy --remote-branch master

clean:
	rm -rf site */*.pyc
	make -C latex clean
