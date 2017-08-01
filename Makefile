# Prerequisites:
#   pip install markdown-include mkdocs mkdocs-material bibtexparser

build:
	PYTHONPATH=$$(pwd)/ext mkdocs build

serve:
	PYTHONPATH=$$(pwd)/ext mkdocs serve

clean:
	rm -rf site */*.pyc
