include ../Makefile

BBL_FILES = \
	bulletins.bbl \
	intl-talks.bbl \
	other-talks.bbl \
	papers.bbl \
	preprints.bbl \
	proceedings.bbl \
	seminars.bbl \
	thesis.bbl \

all: $(BBL_FILES)

CLEANFILES += $(BBL_FILES)

%.bbl: ../../docs/bibtex/%.bib
	@echo "Generating $@ ...";
	@{ \
		printf '\\begin{thebibliography}{99}\n'; \
		printf '\\interlinepenalty=10000\n'; \
		printf '\\providecommand{\\ul}[1]{#1}\n'; \
		printf '\\providecommand{\\href}[2]{#2}\n'; \
		python ../../python/mdx_bibtex.py "$<"; \
		printf '\\end{thebibliography}\n'; \
	} \
	| sed 's/T\.~Ueda/\\ul{T.~Ueda}/' \
	| sed 's/Takahiro~Ueda/\\ul{Takahiro~Ueda}/' \
	| sed 's/植田~高寛/\\ul{植田~高寛}/' \
	| sed 's/Speaker:~\\ul/Speaker:~/' \
	>"$@"
