# Prerequisites:
#   pip install mkdocs mkdocs-material bibtexparser

build:
	PYTHONPATH=$$(pwd)/ext mkdocs build

serve:
	PYTHONPATH=$$(pwd)/ext mkdocs serve

clean:
	rm -rf site */*.pyc
