# Requirements: python>=3.7, poetry>=1.7 and GNU make

export PYTHONPATH=$(shell pwd)/python

build:
	poetry run mkdocs build

install:
	git submodule update --init
	poetry install --no-root

latex:
	poetry run make -C latex

serve:
	poetry run mkdocs serve

deploy:
	@if [ -z "$$GITHUB_ACTIONS" ]; then \
		echo 'NOTE: "make deploy" was invoked outside GitHub Actions.'; \
		while true; do \
			read -p "Do you wish to continue to deploy? (y/n)" yn; \
			case $$yn in \
				[Yy]*) echo 'User chose to continue.'; break;; \
				[Nn]*) echo 'User chose to discontinue.'; exit 1;; \
				*) echo 'Please answer yes or no.';; \
			esac; \
		done; \
	fi
	poetry run mkdocs gh-deploy --remote-branch master

mostlyclean:
	rm -rf */*.pyc
	make -C latex mostlyclean

clean:
	rm -rf site */*.pyc
	make -C latex clean

.PHONY: latex
