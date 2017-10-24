#papers.bbl:
#	@for f in ../../docs/bibtex/*.bib; do \
#		echo Generating "`basename $$f .bib`.bbl ..."; \
#		{ \
#			echo '\begin{thebibliography}{99}'; \
#			echo '\interlinepenalty=10000'; \
#			echo '\providecommand{\ul}[1]{#1}'; \
#			echo '\providecommand{\href}[2]{#2}'; \
#			python ../../ext/mdx_bibtex.py "$$f"; \
#			echo '\end{thebibliography}'; \
#		} \
#		| sed 's/T\.~Ueda/\\ul{T.~Ueda}/' \
#		| sed 's/Takahiro~Ueda/\\ul{Takahiro~Ueda}/' \
#		| sed 's/植田~高寛/\\ul{植田~高寛}/' \
#		| sed 's/Speaker:~\\ul/Speaker:~/' \
#		>"`basename $$f .bib`.bbl"; \
#	done

include ../Makefile

all: papers.bbl proceedings.bbl thesis.bbl release-notes.bbl preprints.bbl \
	intl-talks.bbl other-talks.bbl

CLEANFILES += *.bbl

%.bbl: ../../docs/bibtex/%.bib
	@echo "Generating $@ ...";
	@{ \
		echo '\begin{thebibliography}{99}'; \
		echo '\interlinepenalty=10000'; \
		echo '\providecommand{\ul}[1]{#1}'; \
		echo '\providecommand{\href}[2]{#2}'; \
		python ../../ext/mdx_bibtex.py "$<"; \
		echo '\end{thebibliography}'; \
	} \
	| sed 's/T\.~Ueda/\\ul{T.~Ueda}/' \
	| sed 's/Takahiro~Ueda/\\ul{Takahiro~Ueda}/' \
	| sed 's/植田~高寛/\\ul{植田~高寛}/' \
	| sed 's/Speaker:~\\ul/Speaker:~/' \
	>"$@"
