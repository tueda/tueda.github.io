include ../Makefile

all: papers.bbl proceedings.bbl thesis.bbl software-documents.bbl \
	preprints.bbl intl-talks.bbl other-talks.bbl

CLEANFILES += *.bbl

%.bbl: ../../docs/bibtex/%.bib
	@echo "Generating $@ ...";
	@{ \
		printf '\\begin{thebibliography}{99}\n'; \
		printf '\\interlinepenalty=10000\n'; \
		printf '\\providecommand{\\ul}[1]{#1}\n'; \
		printf '\\providecommand{\\href}[2]{#2}\n'; \
		python ../../ext/mdx_bibtex.py "$<"; \
		printf '\\end{thebibliography}\n'; \
	} \
	| sed 's/T\.~Ueda/\\ul{T.~Ueda}/' \
	| sed 's/Takahiro~Ueda/\\ul{Takahiro~Ueda}/' \
	| sed 's/植田~高寛/\\ul{植田~高寛}/' \
	| sed 's/Speaker:~\\ul/Speaker:~/' \
	>"$@"
