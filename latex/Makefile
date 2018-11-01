# @file Makefile
#
# Makefile for typesetting LaTeX documents. Requires GNU Make 3.81 on Linux.
# See "make help".
#

define help_message
Makefile for LaTeX

Usage:
  make [<targets...>]

Targets:
  all (default):
    Create all possible documents in this directory.

  help:
    Show this message.

  clean:
    Delete all files created by this Makefile.

  mostlyclean:
    Delete only intermediate files created by this Makefile.

  dist:
    Create tar-gzipped archives for arXiv submission.

  watch:
    Watch the changes and automatically recreate documents in this directory.

  upgrade:
    Upgrade the setup.

See also:
  https://github.com/tueda/makefile4latex
endef

# The default target of this Makefile tries to create this type of files from
# all *.tex:
# - dvi
# - ps
# - pdf (default)
default_target = pdf

# The toolchain for typesetting:
# - latex_dvips
# - latex_dvipdf
# - platex_dvips
# - platex_dvipdfmx
# - uplatex_dvips
# - uplatex_dvipdfmx
# - pdflatex (default)
# - xelatex
# - lualatex
# Aliases:
# - latex -> latex_dvips
# - platex -> platex_dvips
# - uplatex -> uplatex_dvips
TOOLCHAIN = pdflatex

# Specify a commit range for latexdiff.
DIFF =

# (for debugging) Keep temporary directories if its value is non-empty.
KEEP_TEMP =

# Specify if use colors for the output:
# - always
# - none
# - auto (default)
make_colors = $(MAKE_COLORS)

# Files not to be included in a distribution.
NODISTFILES =

# Extra files to be included in a distribution.
EXTRADISTFILES =

# Files to be copied in "anc" directory in a distribution.
ANCILLARYFILES =

# Additional files to mostly-clean.
MOSTLYCLEANFILES =

# Additional files to clean.
CLEANFILES =

# Prerequisite make targets in subdirectories.
PREREQUISITE_SUBDIRS =

# Test scripts.
TESTS =

# The following variables will be guessed if empty.
TARGET =
SUBDIRS =
LATEX =
DVIPS =
DVIPDF =
PS2PDF =
GS =
BIBTEX =
SORTREF =
MAKEINDEX =
MAKEGLOSSARIES =
KPSEWHICH =
AXOHELP =
PDFCROP =
EBB =
EXTRACTBB =
LATEXPAND =
LATEXDIFF =
SOFFICE =

# Command options.
LATEX_OPT = -interaction=nonstopmode -halt-on-error
PDFLATEX_DVI_OPT = -output-format=dvi
DVIPS_OPT = -Ppdf -z
DVIPDF_OPT =
PS2PDF_OPT = -dPDFSETTINGS=/prepress -dEmbedAllFonts=true
GS_OPT =
BIBTEX_OPT =
SORTREF_OPT =
MAKEINDEX_OPT =
MAKEGLOSSARIES_OPT =
KPSEWHICH_OPT =
AXOHELP_OPT =
PDFCROP_OPT =
EBB_OPT =
EXTRACTBB_OPT =
LATEXPAND_OPT = --expand-usepackage
LATEXDIFF_OPT =
SOFFICE_OPT =

# ANSI escape code for colorization.
CL_NORMAL = [0m
CL_NOTICE = [32m
CL_WARN   = [35m
CL_ERROR  = [31m

.SUFFIXES:
.SUFFIXES: .log .pdf .odt .eps .ps .jpg .dvi .fmt .tex .cls .sty .ltx .dtx

DEPDIR = .dep
DIFFDIR = .diff

# $(call cache,VARIABLE) expands $(VARIABLE) with caching.
# See https://www.cmcrossroads.com/article/makefile-optimization-eval-and-macro-caching
cache = $(if $(is_cached-$1),,$(eval is_cached-$1 := 1)$(eval cached_val-$1 := $($1)))$(cached_val-$1)

# $(call type,EXEC-FILE) gives the path to the executable if found,
# otherwise empty.
type = $(if $(strip $1),$(strip \
	$(eval type_retval := $(shell which '$(strip $1)' 2>/dev/null)) \
	$(if $(filter-out $(firstword $(type_retval)),$(type_retval)), \
		$(eval type_retval := '$(type_retval)') \
	) \
	$(type_retval) \
))

# $(call switch,STRING,STRING1,VALUE1,STRING2,VALUE2,...) evaluates the value of
# VALUEi corresponding to the first STRINGi that matches to STRING.
# Limitation: up to 4 STRING-VALUE pairs.
switch = \
	$(if $(filter $2,$1),$3, \
		$(if $(filter $4,$1),$5, \
			$(if $(filter $6,$1),$7, \
				$(if $(filter $8,$1),$9, \
				) \
			) \
		) \
	)

# $(call pathsearch,PROG-NAME,NOERROR-IF-NOT-FOUND,NAME1,...) tries to find
# the given executable.
# Limitation: up to 7 NAMEs.
pathsearch = $(strip \
	$(eval retval := ) \
	$(call pathsearch_impl,$3,$4,$5,$6,$7,$8,$9) \
	$(if $2$(retval),,$(eval retval := \
		$(call error_message,$1 not found); \
		exit 1; :)) \
	$(retval) \
)

pathsearch_impl = \
	$(if $(retval),,$(eval retval := $(call type,$1))) \
	$(if $(retval),,$(if $(strip $2 $3 $4 $5 $6 $7 $8 $9),$(call pathsearch_impl,$2,$3,$4,$5,$6,$7,$8,$9)))

# $(target) gives all targets.
target = $(call cache,target_impl)

target_impl = $(strip \
	$(target_impl_from_ltx) \
	$(target_impl_from_tex) \
)

target_impl_from_ltx = $(srcltxfiles:.ltx=.fmt)

target_impl_from_tex = $(strip \
	$(eval retval := ) \
	$(if $(retval),,$(eval retval := $(TARGET))) \
	$(if $(retval),,$(eval retval := $(srctexfiles:.tex=.$(default_target)))) \
	$(retval) \
)

# $(target_basename) gives the result of $(basename $(target)).
target_basename = $(call cache,target_basename_impl)

target_basename_impl = $(basename $(target))

# $(srctexfiles) gives all LaTeX source files.
# They have the ".tex" file extension and
# (1) contain "documentclass", or
# (2) begin with "%&" (including a format file).
srctexfiles = $(call cache,srctexfiles_impl)

srctexfiles_impl = $(strip $(sort \
	$(shell grep documentclass -l *.tex 2>/dev/null) \
	$(shell awk 'FNR==1{if ($$0~"%&") print FILENAME;}' *.tex 2>/dev/null) \
))

# $(srcltxfiles) gives all .ltx files.
srcltxfiles = $(call cache,srcltxfiles_impl)

srcltxfiles_impl = $(wildcard *.ltx)

# $(srcdtxfiles) gives all .dtx files.
srcdtxfiles = $(call cache,srcdtxfiles_impl)

srcdtxfiles_impl = $(wildcard *.dtx)

ifneq ($(DIFF),)

# $(diff_target) gives all latexdiff target files.
diff_target = $(call cache,diff_target_impl)

diff_target_impl = $(strip $(shell \
	$(call get_rev,$(DIFF),_rev1,_rev2,false); \
	if [ -n "$$_rev1" ]; then \
		for _f in $(srctexfiles); do \
			if [ -z "$$_rev2" ]; then \
				if git show "$$_rev1:./$$_f" >/dev/null 2>&1; then \
					echo $${_f%.*}-diff.$(default_target); \
				fi; \
			else \
				if git show "$$_rev1:./$$_f" >/dev/null 2>&1 && git show "$$_rev2:./$$_f" >/dev/null 2>&1; then \
					echo $${_f%.*}-diff.$(default_target); \
				fi ; \
			fi; \
		done; \
	fi \
))

# $(call get_rev,REV-STR,REV1-VAR,REV2-VAR) decomposes the given Git revision(s)
# into 2 variables.
# $(call get_rev,REV-STR,REV1-VAR,REV2-VAR,false) performs the same but without
# checking the revision string.
get_rev = \
	$(if $4,, \
		if [ -z "$1" ]; then \
			$(call error_message,Git revision not given); \
			exit 1; \
		fi; \
	) \
	$2=; \
	$3=; \
	if expr "$1" : '[^.]\{1,\}\.\.[^.]' >/dev/null; then \
		$2=$$(expr "$1" : '\([^.]\{1,\}\)\.\.'); \
		$3=$$(expr "$1" : '[^.]\{1,\}\.\.\(.\{1,\}\)'); \
	elif expr "$1" : '[^.]\{1,\}\.\.$$' >/dev/null; then \
		$2=$$(expr "$1" : '\([^.]\{1,\}\)\.\.'); \
	else \
		$2="$1"; \
	fi

endif

# $(subdirs) gives all subdirectories.
subdirs = $(call cache,subdirs_impl)

subdirs_impl = $(strip \
	$(eval retval := ) \
	$(if $(retval),,$(eval retval := $(SUBDIRS))) \
	$(if $(retval),,$(eval retval := $(dir $(wildcard */Makefile)))) \
	$(retval) \
)

# $(init_toolchain) initializes the toolchain.
init_toolchain = $(call cache,init_toolchain_impl)

init_toolchain_impl = $(strip \
	$(eval $(init_toolchain_$(TOOLCHAIN))) \
	$(if $(typeset_mode),,$(error unknown TOOLCHAIN=$(TOOLCHAIN))) \
)

init_toolchain_latex = \
	$(init_toolchain_latex_dvips)

init_toolchain_latex_dvips = \
	$(eval typeset_mode = dvips) \
	$(eval tex_format = latex)

init_toolchain_latex_dvipdf = \
	$(eval typeset_mode = dvipdf) \
	$(eval tex_format = latex)

init_toolchain_platex = \
	$(init_toolchain_platex_dvips)

init_toolchain_platex_dvips = \
	$(eval typeset_mode = dvips) \
	$(eval tex_format = platex) \
	$(eval LATEX = platex) \
	$(eval BIBTEX = pbibtex) \
	$(eval MAKEINDEX = mendex)

init_toolchain_platex_dvipdfmx = \
	$(eval typeset_mode = dvipdf) \
	$(eval tex_format = platex) \
	$(eval LATEX = platex) \
	$(eval DVIPDF = dvipdfmx) \
	$(eval BIBTEX = pbibtex) \
	$(eval MAKEINDEX = mendex)

init_toolchain_uplatex = \
	$(init_toolchain_uplatex_dvips)

init_toolchain_uplatex_dvips = \
	$(eval typeset_mode = dvips) \
	$(eval tex_format = uplatex) \
	$(eval LATEX = uplatex) \
	$(eval BIBTEX = upbibtex) \
	$(eval MAKEINDEX = upmendex)

init_toolchain_uplatex_dvipdfmx = \
	$(eval typeset_mode = dvipdf) \
	$(eval tex_format = uplatex) \
	$(eval LATEX = uplatex) \
	$(eval DVIPDF = dvipdfmx) \
	$(eval BIBTEX = upbibtex) \
	$(eval MAKEINDEX = upmendex)

init_toolchain_pdflatex = \
	$(eval typeset_mode = pdflatex) \
	$(eval tex_format = pdflatex) \
	$(eval LATEX = pdflatex)

init_toolchain_xelatex = \
	$(eval typeset_mode = pdflatex) \
	$(eval tex_format = xelatex) \
	$(eval LATEX = xelatex)

init_toolchain_lualatex = \
	$(eval typeset_mode = pdflatex) \
	$(eval tex_format = lualatex) \
	$(eval LATEX = lualatex) \
	$(eval BIBTEX = upbibtex) \
	$(eval MAKEINDEX = upmendex)

# The typeset mode: "dvips" or "dvipdf" or "pdflatex".
typeset_mode =

# The TeX format.
tex_format =

# $(call pathsearch2,PROG-NAME,VAR-NAME,NAME1,...) is basically pathsearch after
# calling init_toolchain.
pathsearch2 = $(strip \
	$(init_toolchain) \
	$(call pathsearch,$1,,$($2),$3,$4,$5,$6,$7,$8,$9) \
)

# $(latex)
latex = $(call cache,latex_impl)

latex_impl = $(strip \
	$(latex_noopt) $(LATEX_OPT) \
	$(if $(findstring -recorder,$(LATEX_OPT)),,-recorder) \
)

latex_noopt = $(call cache,latex_noopt_impl)

latex_noopt_impl = $(call pathsearch2,latex,LATEX,latex)

# $(dvips)
dvips = $(call cache,dvips_impl) $(DVIPS_OPT)

dvips_impl = $(call pathsearch2,dvips,DVIPS,dvips,dvipsk)

# $(dvipdf)
dvipdf = $(call cache,dvipdf_impl) $(DVIPDF_OPT)

dvipdf_impl = $(call pathsearch2,dvipdf,DVIPDF,dvipdf,dvipdfm,dvipdfmx)

# $(ps2pdf)
ps2pdf = $(call cache,ps2pdf_impl) $(PS2PDF_OPT)

ps2pdf_impl = $(call pathsearch2,ps2pdf,PS2PDF,ps2pdf)

# $(gs)
gs = $(call cache,gs_impl) $(GS_OPT)

gs_impl = $(call pathsearch2,gs,GS,gs,gswin32,gswin64,gsos2)

# $(bibtex)
bibtex = $(call cache,bibtex_impl) $(BIBTEX_OPT)

bibtex_impl = $(call pathsearch2,bibtex,BIBTEX,bibtex)

# $(sortref)
sortref = $(call cache,sortref_impl) $(SORTREF_OPT)

sortref_impl = $(call pathsearch2,sortref,SORTREF,sortref)

# $(makeindex)
makeindex = $(call cache,makeindex_impl) $(MAKEINDEX_OPT)

makeindex_impl = $(call pathsearch2,makeindex,MAKEINDEX,makeindex)

# $(makeglossaries)
makeglossaries = $(call cache,makeglossaries_impl) $(MAKEGLOSSARIES_OPT)

makeglossaries_impl = $(call pathsearch2,makeglossaries,MAKEGLOSSARIES,makeglossaries)

# $(kpsewhich)
kpsewhich = $(call cache,kpsewhich_impl) $(KPSEWHICH_OPT)

kpsewhich_impl = $(call pathsearch2,kpsewhich,KPSEWHICH,kpsewhich)

# $(axohelp)
axohelp = $(call cache,axohelp_impl) $(AXOHELP_OPT)

axohelp_impl = $(call pathsearch2,axohelp,AXOHELP,axohelp)

# $(pdfcrop)
pdfcrop = $(call cache,pdfcrop_impl) $(PDFCROP_OPT)

pdfcrop_impl = $(call pathsearch2,pdfcrop,PDFCROP,pdfcrop)

# $(ebb)
ebb = $(call cache,ebb_impl) $(EBB_OPT)

ebb_impl = $(call pathsearch2,ebb,EBB,ebb)

# $(extractbb)
extractbb = $(call cache,extractbb_impl) $(EXTRACTBB_OPT)

extractbb_impl = $(call pathsearch2,extractbb,EXTRACTBB,extractbb)

# $(latepand)
latexpand = $(call cache,latexpand_impl) $(LATEXPAND_OPT)

latexpand_impl = $(call pathsearch2,latexpand,LATEXPAND,latexpand)

# $(latepand)
latexdiff = $(call cache,latexdiff_impl) $(LATEXDIFF_OPT)

latexdiff_impl = $(call pathsearch2,latexdiff,LATEXDIFF,latexdiff)

# $(soffice)
soffice = $(call cache,soffice_impl) $(SOFFICE_OPT)

soffice_impl = $(call pathsearch2,soffice,SOFFICE, \
	soffice, \
	/cygdrive/c/Program Files/LibreOffice 6/program/soffice, \
	/cygdrive/c/Program Files (x86)/LibreOffice 6/program/soffice, \
	/cygdrive/c/Program Files/LibreOffice 5/program/soffice, \
	/cygdrive/c/Program Files (x86)/LibreOffice 5/program/soffice, \
	/cygdrive/c/Program Files/LibreOffice 4/program/soffice, \
	/cygdrive/c/Program Files (x86)/LibreOffice 4/program/soffice \
)

# $(Makefile) gives the name of this Makefile.
Makefile = $(call cache,Makefile_impl)

Makefile_impl = $(firstword $(MAKEFILE_LIST))

# $(mostlycleanfiles) gives all intermediately generated files, to be deleted by
# "make mostlyclean".
#   .aux - LaTeX auxiliary file
#   .auxlock - TikZ externalization aux file lock
#   .ax1 - axodraw2 auxiliary (axohelp input) file
#   .ax2 - axohelp output file
#   .bbl - BibTeX output file
#   .blg - BibTeX log file
#   .end - ?
#   .fls - LaTeX recorder file
#   .fmt - TeX format file
#   .glg - glossary log file
#   .glo - glossary entries
#   .gls - glossary output
#   .glsdefs - glossary output
#   .idx - index entries
#   .ilg - index log file
#   .ind - index output
#   .ist - index style file
#   .lof - list of figures
#   .log - (La)TeX log file
#   .lot - list of tables
#   .nav - Beamer navigation items
#   .out - Beamer outlines
#   .snm - Beamer page labels
#   .spl - by elsarticle class
#   .toc - table of contents
#   .*.vrb - Beamer verbatim materials
#   .xdy - by xindy
#   Notes.bib - by revtex package
#   _ref.tex - by sortref
#   .bmc - by dviout
#   .pbm - by dviout
#   -eps-converted-to.pdf - by epstopdf
mostlycleanfiles = $(call cache,mostlycleanfiles_impl)

mostlycleanfiles_impl = $(wildcard $(strip \
	$(srctexfiles:.tex=.aux) \
	$(srctexfiles:.tex=.auxlock) \
	$(srctexfiles:.tex=.ax1) \
	$(srctexfiles:.tex=.ax2) \
	$(srctexfiles:.tex=.bbl) \
	$(srctexfiles:.tex=.blg) \
	$(srctexfiles:.tex=.end) \
	$(srctexfiles:.tex=.fls) \
	$(srctexfiles:.tex=.fmt) \
	$(srctexfiles:.tex=.glg) \
	$(srctexfiles:.tex=.glo) \
	$(srctexfiles:.tex=.gls) \
	$(srctexfiles:.tex=.glsdefs) \
	$(srctexfiles:.tex=.idx) \
	$(srctexfiles:.tex=.ilg) \
	$(srctexfiles:.tex=.ind) \
	$(srctexfiles:.tex=.ist) \
	$(srctexfiles:.tex=.lof) \
	$(srctexfiles:.tex=.log) \
	$(srctexfiles:.tex=.lot) \
	$(srctexfiles:.tex=.nav) \
	$(srctexfiles:.tex=.out) \
	$(srctexfiles:.tex=.snm) \
	$(srctexfiles:.tex=.spl) \
	$(srctexfiles:.tex=.toc) \
	$(srctexfiles:.tex=.*.vrb) \
	$(srctexfiles:.tex=.xdy) \
	$(srctexfiles:.tex=Notes.bib) \
	$(srctexfiles:.tex=_ref.tex) \
	$(srcltxfiles:.ltx=.log) \
	*.bmc \
	*.pbm \
	*-eps-converted-to.pdf \
	*/*-eps-converted-to.pdf \
	$(srctexfiles:.tex=-figure*.dpth) \
	$(srctexfiles:.tex=-figure*.log) \
	$(srctexfiles:.tex=-figure*.md5) \
	$(srctexfiles:.tex=-figure*.pdf) \
	$(srctexfiles:.tex=-diff.dvi) \
	$(srctexfiles:.tex=-diff.ps) \
	$(srctexfiles:.tex=-diff.pdf) \
	$(MOSTLYCLEANFILES) \
))

# $(cleanfiles) gives all generated files to be deleted by "make clean".
cleanfiles = $(call cache,cleanfiles_impl)

cleanfiles_impl = $(wildcard $(strip \
	$(srctexfiles:.tex=.tar.gz) \
	$(srctexfiles:.tex=.pdf) \
	$(srctexfiles:.tex=.ps) \
	$(srctexfiles:.tex=.eps) \
	$(srctexfiles:.tex=.dvi) \
	$(srcltxfiles:.ltx=.fmt) \
	$(srcdtxfiles:.dtx=.cls) \
	$(srcdtxfiles:.dtx=.sty) \
	$(CLEANFILES) \
	$(mostlycleanfiles) \
))

# $(call colorize,COMMAND-WITH-COLOR,COMMAND-WITHOUT-COLOR) invokes the first
# command when coloring is enabled, otherwise invokes the second command.
colorize = \
	if [ "$(make_colors)" = "always" ]; then \
		$1; \
	elif [ "$(make_colors)" = "none" ]; then \
		$2; \
	else \
		if [ -t 1 ]; then \
			$1; \
		else \
			$2; \
		fi; \
	fi

# $(call notification_message,MESSAGE) prints a notification message.
notification_message = \
	$(call colorize, \
		printf "\033$(CL_NOTICE)$1\033$(CL_NORMAL)\n" >&2 \
	, \
		echo "Error: $1" >&2 \
	)

# $(call warning_message,MESSAGE) prints a warning message.
warning_message = \
	$(call colorize, \
		printf "\033$(CL_WARN)Warning: $1\033$(CL_NORMAL)\n" >&2 \
	, \
		echo "Error: $1" >&2 \
	)

# $(call error_message,MESSAGE) prints an error message.
error_message = \
	$(call colorize, \
		printf "\033$(CL_ERROR)Error: $1\033$(CL_NORMAL)\n" >&2 \
	, \
		echo "Error: $1" >&2 \
	)

# $(call exec,COMMAND) invokes the command with checking the exit status.
# $(call exec,COMMAND,false) invokes the command but skips the check.
exec = \
	$(if $(and $(findstring not found,$1),$(findstring exit 1,$1)), \
		$1 \
	, \
		failed=false; \
		$(call colorize, \
			printf "\033$(CL_NOTICE)$1\033$(CL_NORMAL)\n"; \
			exec 3>&1; \
			pipe_status=`{ { $1 3>&- 4>&-; echo $$? 1>&4; } | \
					 $(colorize_output) >&3; } 4>&1`; \
			exec 3>&-; \
			[ "$$pipe_status" = 0 ] || failed=: \
		, \
			echo "$1"; \
			$1 || failed=: \
		) \
		$(if $2,,; $(check_failed)) \
	)

# $(check_failed)
check_failed = $$failed && { [ -n "$dont_delete_on_failure" ] || rm -f $@; exit 1; }; :

# $(colorize_output) gives sed commands for colorful output.
# Errors:
#   "! ...": TeX
#   "I couldn't open database file ...": BibTeX
#   "I found no database files---while reading file ...": BibTeX
#   "I found no \bibstyle command---while reading file ...": BibTeX
#   "I found no \citation commands---while reading file ...": BibTeX
# Warnings:
#   "LaTeX Warning ...": \@latex@warning
#   "Package Warning ...": \PackageWarning or \PackageWarningNoLine
#   "Class Warning ...": \ClassWarning or \ClassWarningNoLine
#   "No file ...": \@input{filename}
#   "No pages of output.": TeX
#   "Underfull ...": TeX
#   "Overfull ...": TeX
#   "Warning-- ...": BibTeX
colorize_output = \
	sed 's/^\(!.*\|I couldn.t open database file.*\|I found no database files---while reading file.*\|I found no .bibstyle command---while reading file.*\|I found no .citation commands---while reading file.*\)/\$\$\x1b$(CL_ERROR)\1\$\$\x1b$(CL_NORMAL)/; \
	     s/^\(LaTeX[^W]*Warning.*\|Package[^W]*Warning.*\|Class[^W]*Warning.*\|No file.*\|No pages of output.*\|Underfull.*\|Overfull.*\|Warning--.*\)/\$\$\x1b$(CL_WARN)\1\$\$\x1b$(CL_NORMAL)/'

# $(call cmpver,VER1,OP,VER2) compares the given two version numbers.
cmpver = { \
	cmpver_ver1_="$1"; \
	cmpver_ver2_="$3"; \
	$(call cmpver_fmt_,cmpver_ver1_); \
	$(call cmpver_fmt_,cmpver_ver2_); \
	$(if $(filter -eq,$2), \
		[ $$cmpver_ver1_ = $$cmpver_ver2_ ]; \
	, \
		$(if $(filter -ne,$2), \
			[ $$cmpver_ver1_ != $$cmpver_ver2_ ]; \
		, \
			cmpver_small_=`{ echo $$cmpver_ver1_; echo $$cmpver_ver2_; } | sort | head -1`; \
			$(if $(filter -le,$2),[ $$cmpver_small_ = $$cmpver_ver1_ ];) \
			$(if $(filter -lt,$2),[ $$cmpver_small_ = $$cmpver_ver1_ ] && [ $$cmpver_ver1_ != $$cmpver_ver2_ ];) \
			$(if $(filter -ge,$2),[ $$cmpver_small_ = $$cmpver_ver2_ ];) \
			$(if $(filter -gt,$2),[ $$cmpver_small_ = $$cmpver_ver2_ ] && [ $$cmpver_ver1_ != $$cmpver_ver2_ ];) \
		) \
	) \
	}

# $(call cmpver_fmt_,VAR)
cmpver_fmt_ = \
	$1=`expr "$$$1" : '[^0-9]*\([0-9][0-9]*\(\.[0-9][0-9]*\)*\)' | sed 's/\./ /g'`; \
	$1=`printf '%05d' $$$1`

##

ifeq ($(DIFF),)

all: $(target)

else

all: $(diff_target)

endif

help: export help_message1 = $(help_message)
help:
	@echo "$$help_message1"

dvi: $(target_basename:=.dvi)

ps: $(target_basename:=.ps)

eps: $(target_basename:=.eps)

pdf: $(target_basename:=.pdf)

dist: $(target_basename:=.tar.gz)

fmt: $(target_basename:=.fmt)

ifneq ($(subdirs),)

$(target_basename:=.dvi) \
$(target_basename:=.ps) \
$(target_basename:=.eps) \
$(target_basename:=.pdf): | prerequisite

prerequisite:
	@for dir in $(subdirs); do \
		if $(MAKE) -n -C $$dir $(PREREQUISITE_SUBDIRS) >/dev/null 2>&1; then \
			$(MAKE) -C $$dir $(PREREQUISITE_SUBDIRS); \
		fi; \
	done; :

endif

mostlyclean:
	@for dir in $(subdirs); do \
		if $(MAKE) -n -C $$dir mostlyclean >/dev/null 2>&1; then \
			$(MAKE) -C $$dir mostlyclean; \
		fi; \
	done; :
	@$(if $(mostlycleanfiles),$(call exec,rm -f $(mostlycleanfiles)))
	@$(if $(wildcard $(DEPDIR) $(DIFFDIR)),$(call exec,rm -rf $(DEPDIR) $(DIFFDIR)))

clean:
	@for dir in $(subdirs); do \
		if $(MAKE) -n -C $$dir clean >/dev/null 2>&1; then \
			$(MAKE) -C $$dir clean; \
		fi; \
	done; :
	@$(if $(cleanfiles),$(call exec,rm -f $(cleanfiles)))
	@$(if $(wildcard $(DEPDIR) $(DIFFDIR)),$(call exec,rm -rf $(DEPDIR) $(DIFFDIR)))

check:
	@for dir in $(subdirs); do \
		if $(MAKE) -n -C $$dir check >/dev/null 2>&1; then \
			$(MAKE) -C $$dir check; \
		fi; \
	done
	@for test in $(TESTS); do \
		if [ -f "$$test" ]; then \
			$(call exec,./$$test); \
		else \
			$(call exec,$$test); \
		fi; \
	done

# The "watch" mode. Try .log instead of .pdf/.dvi files, otherwise make would
# continuously try to typeset for sources previously failed.
watch:
	@echo "Watching for $(srctexfiles:.tex=.$(default_target)). Press Ctrl+C to quit"
	@while :; do \
		if $(MAKE) -q -s $(srctexfiles:.tex=.log); then :; else \
			time $(MAKE) -s $(srctexfiles:.tex=.log); \
		fi; \
		sleep 1; \
	done

# Upgrade files in the setup. (Be careful!)
# When the current directory is a Git repository and doesn't have the .gitignore
# file, this target downloads that of the Makefile4LaTeX repository. It also
# tries to upgrade some other files on Gist.
upgrade:
	@if $(call have_url,Makefile,https://github.com/tueda/makefile4latex); then \
		$(call upgrade,Makefile,https://raw.githubusercontent.com/tueda/makefile4latex/master/Makefile); \
	fi
	@if $(call have_url,.gitignore,https://github.com/tueda/makefile4latex) \
			|| { [ -d .git ] && [ ! -f .gitignore ]; }; then \
		$(call upgrade,.gitignore,https://raw.githubusercontent.com/tueda/makefile4latex/master/.gitignore); \
	fi
	@if $(call have_url,axodraw2e.sty,https://gist.github.com/tueda/5d8a7ff9181ef630160703606f449597); then \
		$(call upgrade,axodraw2e.sty,https://gist.githubusercontent.com/tueda/5d8a7ff9181ef630160703606f449597/raw/axodraw2e.sty); \
	fi
	@if $(call have_url,beamer-setup.sty,https://gist.github.com/tueda/80320d5a756e4800b59e50d6da995765); then \
		$(call upgrade,beamer-setup.sty,https://gist.githubusercontent.com/tueda/80320d5a756e4800b59e50d6da995765/raw/beamer-setup.sty); \
	fi
	@if $(call have_url,my-JHEP.bst,https://gist.github.com/tueda/515c813ad4dc42d8558a20aef94a83c9); then \
		$(call upgrade,my-JHEP.bst,https://gist.githubusercontent.com/tueda/515c813ad4dc42d8558a20aef94a83c9/raw/my-JHEP.bst); \
	fi
	@if $(call have_url,JHEP.bst,https://gist.github.com/tueda/515c813ad4dc42d8558a20aef94a83c9); then \
		$(call upgrade,JHEP.bst,https://gist.githubusercontent.com/tueda/515c813ad4dc42d8558a20aef94a83c9/raw/my-JHEP.bst); \
	fi
	@if $(call have_url,my-iopart-num.bst,https://gist.github.com/tueda/e256d86c9f340f3693419a4cd1311edb); then \
		$(call upgrade,my-iopart-num.bst,https://gist.githubusercontent.com/tueda/e256d86c9f340f3693419a4cd1311edb/raw/my-iopart-num.bst); \
	fi
	@if $(call have_url,iopart-num.bst,https://gist.github.com/tueda/e256d86c9f340f3693419a4cd1311edb); then \
		$(call upgrade,iopart-num.bst,https://gist.githubusercontent.com/tueda/e256d86c9f340f3693419a4cd1311edb/raw/my-iopart-num.bst); \
	fi

# $(call have_url,FILE,URL) checks if the URL is contained in the file.
have_url = grep -q '$2' '$1' >/dev/null 2>&1

# $(call upgrade,FILE,URL) tries to upgrade the given file.
upgrade = \
	wget '$2' -O '$1.tmp' && { \
		if diff -q '$1' '$1.tmp' >/dev/null 2>&1; then \
			$(call notification_message,$1 is up-to-date); \
			rm -f '$1.tmp'; \
		else \
			mv -v '$1.tmp' '$1'; \
			$(call notification_message,$1 is updated); \
		fi; \
		:; \
	}

FORCE:

.PHONY : all check clean dist dvi eps fmt help mostlyclean pdf ps prerequisite upgrade watch FORCE

# $(call typeset,LATEX-COMMAND) tries to typeset the document.
# $(call typeset,LATEX-COMMAND,false) doesn't delete the output file on failure.
typeset = \
	rmfile=$@; \
	rmauxfile=; \
	$(if $2,rmfile=;dont_delete_on_failure=1;) \
	oldfile_prefix=$*.tmp$$$$; \
	trap 'rm -f $$rmfile $$rmauxfile $$oldfile_prefix*' 0 1 2 3 15; \
	failed=false; \
	if [ -f '$@' ]; then \
		need_latex=$(if $(filter-out %.ref %.bib %.bst %.idx %.glo,$?),:,false); \
		need_bibtex=$(if $(filter %.bib %.bst,$?),:,false); \
		need_sortref=$(if $(filter %.ref,$?),:,false); \
		need_makeindex=$(if $(filter %.idx,$?),:,false); \
		need_makeglossaries=$(if $(filter %.glo,$?),:,false); \
		need_axohelp=$(if $(filter %.ax2,$?),:,false); \
		if $$need_sortref || $$need_bibtex; then \
			[ ! -f '$*.aux' ] && need_latex=:; \
		fi; \
	else \
		need_latex=:; \
		need_bibtex=false; \
		need_sortref=false; \
		need_makeindex=false; \
		need_makeglossaries=false; \
		need_axohelp=false; \
	fi; \
	$(call do_latex,$1,false); \
	if $$failed && $(check_noreffile); then \
		need_sortref=:; \
		failed=false; \
	else \
		$(check_failed); \
	fi; \
	for i in 1 2 3 4 5; do \
		$(do_bibtex); \
		$(do_sortref); \
		$(do_makeindex); \
		$(do_makeglossaries); \
		$(do_axohelp); \
		$(call do_latex,$1); \
	done; \
	touch $@; \
	rmfile=; \
	$(call mk_fls_dep,$@,$*.fls); \
	$(call mk_blg_dep,$@,$*.blg); \
	$(check_reffile) && $(call mk_ref_dep,$@,$(<:.tex=.ref)); \
	:

# $(call do_backup,FILE) creates a backup file.
do_backup = \
	[ -f '$1' ] && cp '$1' "$$oldfile_prefix$(suffix $1)"

# $(call check_modified,FILE) checks if the file was modified in comparison with
# the backup file.
check_modified = \
	$(call check_modified_impl,"$$oldfile_prefix$(suffix $1)",'$1')

check_modified_impl = \
	if [ -f $1 ] || [ -f $2 ]; then \
		if diff -q -N $1 $2 >/dev/null 2>&1; then \
			false; \
		else \
			:; \
		fi; \
	else \
		false; \
	fi

# $(call do_latex,LATEX-COMMAND)
# $(call do_latex,LATEX-COMMAND,false) skips the check.
do_latex = \
	if $$need_latex; then \
		need_latex=false; \
		$(call do_backup,$*.aux); \
		$(call do_backup,$*.toc); \
		$(call do_backup,$*.lof); \
		$(call do_backup,$*.lot); \
		$(call do_backup,$*.idx); \
		$(call do_backup,$*.glo); \
		$(call do_backup,$*.ax1); \
		$(call exec,$1 $<,$2); \
		if $(call check_modified,$*.aux); then \
			$(check_bblfile) && need_bibtex=:; \
			$(check_reffile) && need_sortref=:; \
			$(check_glsfile) && need_makeglossaries=:; \
		else \
			$(check_nobblfile) && need_bibtex=:; \
		fi; \
		if $(call check_modified,$*.idx); then \
			$(check_indfile) && need_makeindex=:; \
		fi; \
		if $(call check_modified,$*.glo); then \
			$(check_glsfile) && need_makeglossaries=:; \
		fi; \
		if $(call check_modified,$*.ax1); then \
			$(check_ax2file) && need_axohelp=:; \
		fi; \
		{ $(check_rerun) || $(call check_modified,$*.toc) || $(call check_modified,$*.lof) || $(call check_modified,$*.lot); } && need_latex=:; \
	fi

# $(do_bibtex)
do_bibtex = \
	if $$need_bibtex; then \
		need_bibtex=false; \
		$(call do_backup,$*.bbl); \
		rmauxfile=$*.bbl; \
		$(call exec,$(bibtex) $(<:.tex=)); \
		rmauxfile=; \
		$(call check_modified,$*.bbl) && need_latex=:; \
	fi

# $(do_sortref)
do_sortref = \
	if $$need_sortref; then \
		need_sortref=false; \
		$(call do_backup,$*_ref.tex); \
		$(call exec,$(sortref) $< $(<:.tex=.ref)); \
		$(call check_modified,$*_ref.tex) && need_latex=:; \
	fi

# $(do_makeindex)
do_makeindex = \
	if $$need_makeindex; then \
		need_makeindex=false; \
		$(call do_backup,$*.ind); \
		$(call exec,$(makeindex) $(<:.tex=)); \
		$(call check_modified,$*.ind) && need_latex=:; \
	fi

# $(do_makeglossaries)
do_makeglossaries = \
	if $$need_makeglossaries; then \
		need_makeglossaries=false; \
		$(call do_backup,$*.gls); \
		$(call exec,$(makeglossaries) $(<:.tex=)); \
		$(call check_modified,$*.gls) && need_latex=:; \
	fi

# $(do_axohelp)
do_axohelp = \
	if $$need_axohelp; then \
		need_axohelp=false; \
		$(call do_backup,$*.ax2); \
		$(call exec,$(axohelp) $(<:.tex=)); \
		$(call check_modified,$*.ax2) && need_latex=:; \
	fi

# $(call do_kpsewhich,FULLPATH-DEST-VAR,FILE)
do_kpsewhich = \
	fullpath_kpsewhich_impl=`$(kpsewhich) "$2"`; \
	if [ -z "$$fullpath_kpsewhich_impl" ]; then \
		$(call error_message,$2 not found); \
		exit 1; \
	fi; \
	$1=$$fullpath_kpsewhich_impl

# $(call mk_fls_dep,TARGET,FLS-FILE) saves dependencies from a .fls file.
mk_fls_dep = \
	if [ -f '$2' ]; then \
		mkdir -p $(DEPDIR); \
		{ \
			for f in `grep INPUT '$2' | sed 's/INPUT *\(\.\/\)\?//' | sort | uniq`; do \
				case $$f in \
					*:*|/*) ;; \
					*.fmt) ;; \
					*) [ -f "$$f" ] && echo "$1 : \$$(wildcard $$f)";; \
				esac; \
			done; \
		} >$(DEPDIR)/$1.fls.d; \
	fi

# $(call mk_blg_dep,TARGET,BLG-FILE) saves dependencies from a .blg file.
mk_blg_dep = \
	if [ -f '$2' ]; then \
		mkdir -p $(DEPDIR); \
		{ \
			for f in `{ grep 'Database file [^:]*:' '$2'; grep 'The style file:' '$2'; } | sed 's/[^:]*://'`; do \
				[ -f "$$f" ] && echo "$1 : \$$(wildcard $$f)"; \
			done; \
		} >$(DEPDIR)/$1.blg.d; \
	fi

# $(call mk_ref_dep,TARGET,REF-FILE) saves dependencies from a .ref file.
mk_ref_dep = \
	if [ -f '$2' ]; then \
		mkdir -p $(DEPDIR); \
		echo '$1: $2' >$(DEPDIR)/$1.ref.d; \
	fi

check_noreffile = grep "File \`$*_ref.tex' not found" $*.log >/dev/null 2>&1

check_bblfile = grep '$*.bbl' $*.log >/dev/null 2>&1

check_nobblfile = grep 'No file $*.bbl' $*.log >/dev/null 2>&1

check_reffile = grep '$*_ref.tex' $*.log >/dev/null 2>&1

check_indfile = grep '$*.ind' $*.log >/dev/null 2>&1

check_glsfile = grep '$*.gls' $*.log >/dev/null 2>&1

# axodraw2.sty uses primitive control sequences for reading .ax2 file, instead
# of \input, without writing any jobname.ax2 in the log file. So we look for
# jobname.ax1; if it is found in the log file, it means axodraw2.sty tries to
# read jobname.ax2.
check_ax2file = grep '$*.ax1' $*.log >/dev/null 2>&1

check_rerun = grep 'Rerun' $*.log | grep -v 'Package: rerunfilecheck\|rerunfilecheck.sty' >/dev/null 2>&1

#NOTE: xelatex doesn't work with -output-format=dvi.

.tex.dvi:
	@$(init_toolchain)
	@$(call switch,$(typeset_mode), \
		dvips, \
		$(call typeset,$(latex)), \
		dvipdf, \
		$(call typeset,$(latex)), \
		pdflatex, \
		$(call typeset,$(latex) $(PDFLATEX_DVI_OPT)), \
	)

.tex.ps:
	@$(init_toolchain)
	@$(call switch,$(typeset_mode), \
		dvips, \
		$(call typeset,$(latex)) && $(call exec,$(dvips) $*), \
		dvipdf, \
		$(call typeset,$(latex)) && $(call exec,$(dvips) $*), \
		pdflatex, \
		$(call typeset,$(latex) $(PDFLATEX_DVI_OPT)), \
	)

.tex.pdf:
	@$(init_toolchain)
	@$(call switch,$(typeset_mode), \
		dvips, \
		$(call typeset,$(latex)) && $(call exec,$(dvips) $*) && $(call exec,$(ps2pdf) $*.ps $*.pdf), \
		dvipdf, \
		$(call typeset,$(latex)) && $(call exec,$(dvipdf) $*), \
		pdflatex, \
		$(call typeset,$(latex)), \
	)

# This always updates the timestamp of the target (.log).
.tex.log:
	@$(init_toolchain)
	@touch $@
	@$(call switch,$(default_target), \
		dvi, \
		$(call switch,$(typeset_mode), \
			dvips, \
			$(call typeset,$(latex),false), \
			dvipdf, \
			$(call typeset,$(latex),false), \
			pdflatex, \
			$(call typeset,$(latex) $(PDFLATEX_DVI_OPT),false), \
		), \
		ps, \
		$(call switch,$(typeset_mode), \
			dvips, \
			$(call typeset,$(latex),false) && $(call exec,$(dvips) $*), \
			dvipdf, \
			$(call typeset,$(latex),false) && $(call exec,$(dvips) $*), \
			pdflatex, \
			$(call typeset,$(latex) $(PDFLATEX_DVI_OPT),false), \
		), \
		pdf, \
		$(call switch,$(typeset_mode), \
			dvips, \
			$(call typeset,$(latex),false) && $(call exec,$(dvips) $*) && $(call exec,$(ps2pdf) $*.ps $*.pdf), \
			dvipdf, \
			$(call typeset,$(latex),false) && $(call exec,$(dvipdf) $*), \
			pdflatex, \
			$(call typeset,$(latex),false), \
		) \
	)

.dvi.eps:
	@$(init_toolchain)
	@trap 'rm -f $*.tmp.ps $*.tmp.pdf' 0 1 2 3 15; \
	$(call exec,$(dvips) -o $*.tmp.ps $<); \
	$(call exec,$(gs) -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress -dEPSCrop -o $*.tmp.pdf $*.tmp.ps); \
	if $(call cmpver,`$(gs) --version`,-lt,9.15); then \
		$(call exec,$(gs) -sDEVICE=epswrite -o $@ $*.tmp.pdf); \
	else \
		$(call exec,$(gs) -sDEVICE=eps2write -o $@ $*.tmp.pdf); \
	fi

# Experimental (TeXLive)
.ltx.fmt:
	@$(init_toolchain)
	@$(call exec,$(latex_noopt) -ini -jobname='$*' '&$(notdir $(basename $(latex_noopt))) $<\dump')
	@$(call exec,rm -f $*.pdf)

# Experimental (TeXLive)
#
# Example:
#   $ cat foo.tex
#   %&foo
#   \documentclass{beamer}
#   \begin{document}
#   \begin{frame}
#   Your presentation here.
#   \end{frame}
#   \end{document}
#   $ make clean
#   $ time make foo.pdf
#   $ make clean
#   $ time { make foo.fmt && make foo.pdf; }
#
# Note: axodraw2 checks if .ax2 file exists when loaded, which becomes a problem
#   if one includes it in a format file: whether or not .ax2 file exists is
#   stores in a format file.
#
.tex.fmt:
	@$(init_toolchain)
	@$(call exec,$(latex_noopt) -ini -jobname='$*' '&$(tex_format)' mylatexformat.ltx '$<')
	@$(call exec,rm -f $*.pdf)

.dtx.cls:
	@$(call exec,$(latex_noopt) $(basename $<).ins)

.dtx.sty:
	@$(call exec,$(latex_noopt) $(basename $<).ins)

.odt.pdf:
	@$(call exec,$(soffice) --headless --nologo --nofirststartwizard --convert-to pdf $<)

# A distribution (for arXiv) needs to include
# 1. The main tex file.
# 2. Files that the main tex file depends on, except
#    - files with absolute paths, which are considered as system files,
#    - files created by LaTeX during typesetting, e.g., *.aux files,
#    - *.ax2 file unless "\pdfoutput=1" is explicitly used.
#    This default behaviour may be overwritten by EXTRADISTFILES and
#    NODISTFILES.
# 3. "PoSlogo.pdf" without "\pdfoutput=1" most likely indicates that
#    "PoSLogo.ps" should be also included for the PoS class.
# 4. 00README.XXX file if exists, and
#    - Files listed in 00README.XXX with "ignore".
#    See https://arxiv.org/help/00README
# 5. Files listed in ANCILLARYFILES are included under a subdirectory "anc".
#    See https://arxiv.org/help/ancillary_files
%.tar.gz: %.$(default_target)
	@tmpdir=tmp$$$$; \
	mkdir $$tmpdir || exit 1; \
	$(if $(KEEP_TEMP),,trap 'rm -rf $$tmpdir' 0 1 2 3 15;) \
	pdfoutput=false; \
	if head -5 "$*.tex" | sed 's/%.*//' | grep -q '\pdfoutput=1'; then \
		pdfoutput=:; \
	fi; \
	if [ ! -f '$*.fls' ]; then \
		$(call error_message,$*.fls not found. Delete $*.$(default_target) and then retry); \
		exit 1; \
	fi; \
	dep_files=; \
	for f in `grep INPUT '$*.fls' | sed 's/^INPUT *//' | sed '/^kpsewhich/d' | sed 's|^\.\/||' | sort | uniq`; do \
		case $$f in \
			*:*|/*|*.aux|*.lof|*.lot|*.nav|*.out|*.spl|*.toc|*.vrb|*-eps-converted-to.pdf) ;; \
			*) \
				case $$f in \
					*.ax2) \
						$$pdfoutput || continue; \
						;; \
					PoSlogo.pdf) \
						if $$pdfoutput; then :; else \
							if [ -f PoSlogo.ps ]; then \
								$(call add_dist,PoSlogo.ps,$$tmpdir,dep_files); \
							fi; \
						fi; \
						;; \
				esac; \
				$(call add_dist,$$f,$$tmpdir,dep_files); \
		esac; \
	done; \
	for ff in $(EXTRADISTFILES); do \
		$(call do_kpsewhich,f,$$ff); \
		cp "$$f" "$$tmpdir/" || exit 1; \
		dep_files="$$dep_files $$f"; \
	done; \
	if [ -f 00README.XXX ]; then \
		cp "00README.XXX" "$$tmpdir/" || exit 1; \
		dep_files="$$dep_files 00README.XXX"; \
		for f in `grep ignore 00README.XXX | sed 's/ *ignore *$$//'`; do \
			cp --parents "$$f" "$$tmpdir/" || rsync -R "$$f" "$$tmpdir" || exit 1; \
			dep_files="$$dep_files $$f"; \
		done; \
	fi; \
	for f in $(ANCILLARYFILES); do \
		[ -d "$$tmpdir/anc" ] || mkdir "$$tmpdir/anc"; \
		cp "$$f" "$$tmpdir/anc/" || exit 1; \
		dep_files="$$dep_files $$f"; \
	done; \
	mkdir -p $(DEPDIR); \
	{ \
		for f in $$dep_files; do \
			echo "$@ : \$$(wildcard $$f)"; \
		done; \
	} >$(DEPDIR)/$@.d; \
	cd $$tmpdir || exit 1; \
	$(call exec,tar cfv - * | gzip -9 -n >$@,false); \
	cd .. || exit 1; \
	$(check_failed); \
	mv $$tmpdir/$@ $@

# $(call add_dist,FILE,TMPDIR,DEP_FILES_VAR)
add_dist = { \
		tmp_ok=:; \
		for tmp_ff in $(NODISTFILES); do \
			if [ "x$1" = "x$$tmp_ff" ]; then \
				tmp_ok=false; \
				break; \
			fi; \
		done; \
		if $$tmp_ok; then \
			tmp_d=`dirname "$1"`; \
			mkdir -p "$2/$$tmp_d"; \
			cp "$1" "$2/$$tmp_d" || exit 1; \
			$3="$$$3 $1"; \
		fi; \
		:; \
	}

ifneq ($(DIFF),)

# Take a LaTeX-diff of two Git revisions (or a Git revision and the current
# working copy) given in the DIFF variable and typeset the resultant document.
# Limitation: though DIFF=rev1..rev2 is supported, the original LaTeX source
# file needs to exist as long as we want to use the rule *.tex -> *-diff.*.
%-diff.$(default_target): %.tex FORCE
	@$(call get_rev,$(DIFF),_rev1,_rev2); \
	if [ -n "$$_rev1" ]; then \
		if git cat-file -e "$$_rev1" 2>/dev/null; then :; else \
			$(call error_message,invalid revision: $$_rev1); \
			exit 1; \
		fi; \
		if git show "$$_rev1:./$<" >/dev/null 2>&1; then :; else \
			$(call error_message,$< not in $$_rev1); \
			exit 1; \
		fi; \
	fi; \
	if [ -n "$$_rev2" ]; then \
		if git cat-file -e "$$_rev2" 2>/dev/null; then :; else \
		$(call error_message,invalid revision: $$_rev2); \
			exit 1; \
		fi; \
		if git show "$$_rev2:./$<" >/dev/null 2>&1; then :; else \
			$(call error_message,$< not in $$_rev2); \
			exit 1; \
		fi; \
	fi; \
	_tmpdir=tmp$$$$; \
	$(if $(KEEP_TEMP),,trap 'rm -rf $$_tmpdir' 0 1 2 3 15;) \
	_git_root=$$(git rev-parse --show-cdup).; \
	_git_prefix=$$(git rev-parse --show-prefix); \
	if [ -z "$$_rev2" ]; then \
		$(call expand_latexdiff_repo,$$_rev1); \
		$(MAKE) -f $(Makefile) $*.tar.gz || exit 1; \
		mkdir $$_tmpdir; \
		(cd $$_tmpdir && tar xfz ../$(DIFFDIR)/$$_rev1/$$_git_prefix/$*.tar.gz); \
		(cd $$_tmpdir && tar xfz ../$*.tar.gz); \
		cp $(DIFFDIR)/$$_rev1/$$_git_prefix/$*-expanded.tex $$_tmpdir/$*-expanded-old.tex; \
		$(call expand_latex_source,$<,$$_tmpdir/$*-expanded-new.tex); \
		$(call latexdiff_insubdir,$$_tmpdir,$<,$*-expanded-old.tex,$*-expanded-new.tex,$*-diff.tex,$*-diff.$(default_target),$(DIFF)..); \
	else \
		$(call expand_latexdiff_repo,$$_rev1); \
		$(call expand_latexdiff_repo,$$_rev2); \
		mkdir $$_tmpdir; \
		(cd $$_tmpdir && tar xfz ../$(DIFFDIR)/$$_rev1/$$_git_prefix/$*.tar.gz); \
		(cd $$_tmpdir && tar xfz ../$(DIFFDIR)/$$_rev2/$$_git_prefix/$*.tar.gz); \
		cp $(DIFFDIR)/$$_rev1/$$_git_prefix/$*-expanded.tex $$_tmpdir/$*-expanded-old.tex; \
		cp $(DIFFDIR)/$$_rev2/$$_git_prefix/$*-expanded.tex $$_tmpdir/$*-expanded-new.tex; \
		$(call latexdiff_insubdir,$$_tmpdir,$<,$*-expanded-old.tex,$*-expanded-new.tex,$*-diff.tex,$*-diff.$(default_target),$(DIFF)); \
	fi

# $(call expand_latexdiff_repo,REVISION)
# Uses: $*, $$_git_root, $$_git_prefix
expand_latexdiff_repo = \
	mkdir -p $(DIFFDIR); \
	if [ -d $(DIFFDIR)/$1 ]; then \
		git -C $(DIFFDIR)/$1 fetch origin; \
		case $1 in \
			*HEAD*) \
				git -C $(DIFFDIR)/$1 reset --hard origin/$1; \
				;; \
			*) \
				git -C $(DIFFDIR)/$1 reset --hard $1; \
				;; \
		esac; \
	else \
		git clone $$_git_root $(DIFFDIR)/$1; \
		git -C $(DIFFDIR)/$1 checkout $1; \
	fi; \
	rm -f $(DIFFDIR)/$1/$$_git_prefix/$(Makefile); \
	cp $(Makefile) $(DIFFDIR)/$1/$$_git_prefix/$(Makefile); \
	$(MAKE) -C $(DIFFDIR)/$1/$$_git_prefix -f $(Makefile) $*.tar.gz || exit 1; \
	(cd $(DIFFDIR)/$1/$$_git_prefix && $(call expand_latex_source,$*.tex,$*-expanded.tex))

# $(call expand_latex_source,IN-TEX-FILE,OUT-TEX-FILE) expands a LaTeX source.
# Optionally a .bbl file is also expanded if exists.
expand_latex_source = { \
	_tmp_latexexpand_fbody="$1"; \
	_tmp_latexexpand_fbody=$${_tmp_latexexpand_fbody%.*}; \
	if [ -f "$$_tmp_latexexpand_fbody.bbl" ]; then \
		$(call exec,$(latexpand) --expand-bbl "$$_tmp_latexexpand_fbody.bbl" "$1" >"$2"); \
	else \
		$(call exec,$(latexpand) --expand-usepackage "$1" >"$2"); \
	fi \
}

# $(call latexdiff_insubdir,DIRECTORY,ORIG-TEX-FILE,OLD-TEX-FILE,NEW-TEX-FILE,TEMP-DIFF-TEX-FILE,TARGET-FILE,REVISIONS)
# performs latexdiff and then make for the target-diff file.
# When --math-markup=N is not given in LATEXDIFF_OPT, this code repeats
# the process with decreasing --math-markup from 3 to 0 until it succeeds.
latexdiff_insubdir = \
	rm -f $1/$2; \
	cp $(Makefile) $1/$(Makefile); \
	[ -f .latex.mk ] && cp .latex.mk $1/ ;\
	$(if $(findstring --math-markup=,$(LATEXDIFF_OPT)), \
		(cd $1 && $(call exec,$(latexdiff) $3 $4 >$5)) || exit 1; \
		$(MAKE) -C $1 -f $(Makefile) $6 || exit 1; \
	, \
		(cd $1 && $(call exec,$(latexdiff) --math-markup=3 $3 $4 >$5)) || exit 1; \
		if $(MAKE) -C $1 -f $(Makefile) $6; then :; else \
			(cd $1 && $(call exec,$(latexdiff) --math-markup=2 $3 $4 >$5)) || exit 1; \
			if $(MAKE) -C $1 -f $(Makefile) $6; then :; else \
				(cd $1 && $(call exec,$(latexdiff) --math-markup=1 $3 $4 >$5)) || exit 1; \
				if $(MAKE) -C $1 -f $(Makefile) $6; then :; else \
					(cd $1 && $(call exec,$(latexdiff) --math-markup=0 $3 $4 >$5)) || exit 1; \
					$(MAKE) -C $1 -f $(Makefile) || exit 1; \
				fi; \
			fi; \
		fi; \
	) \
	mv $1/$6 .; \
	if [ -f "$6" ]; then \
		$(call notification_message,$6 generated for $7); \
	else \
		exit 1; \
	fi

endif

-include $(DEPDIR)/*.d
-include ~/.latex.mk
-include .latex.mk
