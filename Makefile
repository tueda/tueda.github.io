# Requirements: uv>=0.9 and GNU make>=3.81

export PYTHONPATH := $(CURDIR)/python

build:
	uv run mkdocs build --strict

install:
	git submodule update --init
	uv sync

latex:
	uv run make -C latex

serve:
	uv run mkdocs serve

mostlyclean:
	rm -rf */*.pyc
	make -C latex mostlyclean

clean:
	rm -rf site */*.pyc
	make -C latex clean

.PHONY: build install latex serve mostlyclean clean
