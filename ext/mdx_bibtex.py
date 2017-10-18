"""Python Markdown BibTeX extension."""

from __future__ import unicode_literals

import re

import bibtexparser
from bibtexparser.bparser import BibTexParser

from markdown import Extension
from markdown.preprocessors import Preprocessor


class BibTeXPreprocessor(Preprocessor):
    """Preprocessor to handle BibTeX code."""

    def __init__(self, config):
        """Construct a BibTeX preprocessor."""
        self._format = config['format'].lower()
        self._style = config['style'].lower()

    def run(self, lines):
        """Do the preprocessing."""
        new_lines = []
        current_block = None
        for line in lines:
            if current_block is None:
                if line[:1] == '@' and line.find('{', 2) >= 2:
                    current_block = []
                    current_block.append(line)
                    continue
                new_lines.append(line)
            else:
                if line[:1] == '}' and not line[1:].strip():
                    current_block.append('}')
                    result_lines = self.parse_bibtex_entry(
                        '\n'.join(current_block))
                    if result_lines:
                        new_lines += result_lines
                    else:
                        new_lines += current_block
                    current_block = None
                else:
                    current_block.append(line)
                    continue
        if current_block:
            new_lines += current_block
        return new_lines

    def parse_bibtex_entry(self, string):
        """Parse a BibTeX entry."""
        # BibTeXParser considers an entry type starting with "comment" as
        # a special one and loads() returns nothing. Make a workaround.
        comment_magic = '__dont_ignore_comment__'

        string = re.sub('^@comment', '@' + comment_magic, string)

        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        entries = bibtexparser.loads(string, parser=parser).entries
        if len(entries) != 1:
            return None
        entry = entries[0]

        if entry['ENTRYTYPE'].startswith(comment_magic):
            # An empty line indicates that the parsing succeeded, but it was a
            # comment. Will be discarded by the caller.
            return ['']

        for key in entry:
            s = entry[key]

            # Canonicalize spaces.
            s = re.sub(r'\n', ' ', s)
            s = re.sub(r'\s\s+', ' ', s)

            s = _latex_to_unicode(s)

            entry[key] = s

        # Dispatch the entry to the method for this style and the entry type.
        format_name = ('_format_' + self._format + '_' + self._style + '_' +
                       entry['ENTRYTYPE'])
        if hasattr(self, format_name):
            lines = getattr(self, format_name)(entry)
            if lines:
                return [''] + [(
                    ('1. ' if i == 0 else '') + line
                ) for i, line in enumerate(lines)] + ['']

        return None

    def _format_html_cv_article(self, entry):
        if 'title' not in entry or 'author' not in entry:
            return None

        lines = StringList()
        lines.add(_cv_title(entry))
        lines.add_break()
        lines.add(_cv_subtitle(entry))
        lines.add_break()
        lines.add(_cv_author(entry))
        lines.add_break()
        lines.add(_cv_journal(entry))
        lines.add_sep()
        lines.add(_cv_preprint(entry))
        lines.cancel_sep()
        lines.add(_cv_inspire(entry))
        lines.add(_cv_github(entry))
        lines.add_break()
        lines.add(_cv_proceedings_info(entry))

        return lines

    def _format_html_cv_phdthesis(self, entry):
        if 'title' not in entry:
            return None

        lines = StringList()
        lines.add(_cv_title(entry))
        lines.add_break()
        lines.add(_cv_subtitle(entry))
        lines.add_break()
        if 'month' in entry:
            lines.add(entry['month'])
        if 'year' in entry:
            lines.add(entry['year'])
        lines.add_sep()
        if 'school' in entry:
            lines.add(entry['school'])

        return lines


def _latex_to_unicode(s):
    # Accent and special characters in LaTeX.
    simple_replacements = {
        '\\"A': u"\u00C4",
        '\\"a': u"\u00E4",
        '\\"O': u"\u00D6",
        '\\"o': u"\u00F6",
        '\\"U': u"\u00DC",
        '\\"u': u"\u00FC",
        "\\'i": u"\u00ED",
    }

    for r in simple_replacements:
        # One often writes {\"o} in BibTeX: the curly braces should be removed.
        s = s.replace('{{{0}}}'.format(r), simple_replacements[r])
        s = s.replace(r, simple_replacements[r])

    return s


def _ndashify(s):
    # Smart "dash". Don't apply it for URLs.
    months = (
        r'January|February|March|April|May|June|'
        r'July|August|September|October|November|December'
    )

    return re.sub(
        r'(\d|' + months + r')-(\d|' + months + r')',
        r'\1&ndash;\2', s)


def _apostrophify(s):
    # Single "'" is presumably an apostrophe. SmartyPants has a problem
    # for it. To avoid the problem, "'" needs to be replaced. Don't apply it
    # for math expressions, which may contain derivatives.
    if s.count("'") == 1:
        s = s.replace("'", '&#39;')
    return s


def _canonicalize_author(s):
    # "bbb, aaa" -> "aaa bbb".
    s = s.split(',', 2)

    if len(s) == 1:
        s = s[0]
    else:
        s = s[1] + s[0]

    # Handle spaces in an author name.
    s = re.sub(r'\.', '. ', s)
    s = re.sub(r'\s+', ' ', s)
    for j in range(5):
        s = re.sub(r'([A-Z])\. ([A-Z])\.', r'\1.\2.', s)
    s = s.strip().replace(' ', '&nbsp;')

    return s


def _canonicalize_date(s):
    months = (
        r'January|February|March|April|May|June|'
        r'July|August|September|October|November|December'
    )

    # Example: April 1-May 5, 2000 -> 1 April-5 May 2000
    m = re.search(
        r'(' + months + r')\s+(\d+)-(' + months + ')\s+(\d+)\s*,\s*(\d+)', s)
    if m:
        s = '{0}{1} {2}-{3} {4} {5}{6}'.format(
            s[:m.start()],
            m.group(2),
            m.group(1),
            m.group(4),
            m.group(3),
            m.group(5),
            s[m.end():]
        )

    # Example: April 1-5, 2000 -> 1-5 April 2000
    m = re.search(r'(' + months + r')\s+(\d+-\d+)\s*,\s*(\d+)', s)
    if m:
        s = '{0}{1} {2} {3}{4}'.format(
            s[:m.start()],
            m.group(2),
            m.group(1),
            m.group(3),
            s[m.end():]
        )

    s = _ndashify(s)
    return s


def _get_authors(entry):
    """Read the authors in an entry and return a list of strings."""
    authors = re.split(r'\band\b', entry['author'])

    return [_canonicalize_author(a) for a in authors]


def _make_link(text, url):
    return '[<small>[{0}]</small>]({1})'.format(text, url)


def _cv_title(entry):
    if 'title' not in entry:
        return None

    return '**{0}**'.format(entry['title'])


def _cv_subtitle(entry):
    if 'subtitle' not in entry:
        return None

    return '(*{0}*&thinsp;)'.format(entry['subtitle'])


def _cv_author(entry):
    if 'author' not in entry:
        return None

    authors = _get_authors(entry)
    aa = []
    for i, a in enumerate(authors):

        # Join it by a comma or "and".
        if i == len(authors) - 2:
            a += ' and '
        elif i <= len(authors) - 3:
            a += ', '
        aa.append(a)

    return ''.join(aa)


def _cv_journal(entry):
    if 'journal' not in entry:
        return None
    if 'year' not in entry:
        return None
    if 'pages' not in entry:
        return None
    if 'volume' in entry:
        s = '{0} **{1}** ({2}) {3}'.format(
            entry['journal'],
            entry['volume'],
            entry['year'],
            entry['pages'],
        )
    else:
        s = '{0} ({1}) {2}'.format(
            entry['journal'],
            entry['year'],
            entry['pages'],
        )
    s = _ndashify(s)
    s = _apostrophify(s)
    if 'doi' in entry:
        s = '[{0}](https://doi.org/{1})'.format(s, entry['doi'])
    return s


def _cv_preprint(entry):
    if 'eprint' not in entry:
        return None
    if 'archiveprefix' not in entry:
        return None

    if entry['archiveprefix'] == 'arXiv':
        if entry['eprint'].find('/') >= 0:
            return '[arXiv:{0}](https://arxiv.org/abs/{0})'.format(
                entry['eprint'],
            )
        if 'primaryclass' in entry:
            return '[arXiv:{0} [{1}]](https://arxiv.org/abs/{0})'.format(
                entry['eprint'],
                entry['primaryclass'],
            )

    return None


def _cv_inspire(entry):
    if 'eprint' in entry and 'archiveprefix' in entry:
        if entry['archiveprefix'] == 'arXiv':
            if ('primaryclass' in entry and
                    entry['primaryclass'] in ('hep-lat', 'hep-ph', 'hep-th')):
                return _make_link(
                    'INSPIRE',
                    'https://inspirehep.net/search?p=find+eprint+{0}'.format(
                        entry['eprint'])
                )

    if 'inspirehep' in entry:
        return _make_link(
            'INSPIRE',
            'https://inspirehep.net/search?p=find+{0}'.format(
                entry['inspirehep'])
        )

    return None


def _cv_github(entry):
    if 'github' in entry:
        return _make_link(
            'GitHub',
            'https://github.com/{0}'.format(entry['github'])
        )


def _cv_proceedings_info(entry):
    if 'booktitle' not in entry:
        return None

    # Example: Proceedings, Conference name: place, date
    m = re.search('Proceedings,(.*):([^:]*)$', entry['booktitle'])
    if m:
        confname = m.group(1).strip()
        confplace = m.group(2).strip()  # also date

        if 'confurl' in entry:
            confname = '[{0}]({1})'.format(confname, entry['confurl'])

        confplace = _canonicalize_date(confplace)

        s = 'Proceedings for {0}, {1}'.format(confname, confplace)

        if 'speaker' in entry:
            s += ' (Speaker:&nbsp;{0})'.format(
                _canonicalize_author(entry['speaker']))

        return s

    return None


class StringList(list):
    """List for strings."""

    def __init__(self, *args):
        """Construct a string list."""
        super(StringList, self).__init__(*args)
        self._clean = True
        self._sep = False
        self._cancel_sep = False
        self._break = False

    def _update(self):
        if self._sep and not self._cancel_sep:
            self[-1] += ','
        if self._break:
            self[-1] += '  '
        self._clean = True
        self._sep = False
        self._cancel_sep = False
        self._break = False

    def add(self, s):
        """Add a line."""
        if s:
            self._update()
            self.append(s.strip())
            self._clean = False

    def add_sep(self):
        """Add a comma at the end of the last line."""
        if not self._clean:
            self._clean = True
            self._sep = True
            self._cancel_sep = False

    def cancel_sep(self):
        """Remove a comma from the end of the last line."""
        if self._sep:
            self._cancel_sep = True

    def add_break(self):
        """Add a line break."""
        if not self._clean:
            self._clean = True
            self._sep = False
            self._cancel_sep = False
            self._break = True
        elif self._sep:
            self._sep = False
            self._cancel_sep = False
            self._break = True

    def add_period(self):
        """Add a period at the end of the last line."""
        if not self._clean:
            self._clean = True
            self._sep = False
            self._break = False
            if self:
                self[-1] += '.'


class BibTeXExtension(Extension):
    """BibTeX extension."""

    def __init__(self, **kwargs):
        """Construct a BibTeX extension."""
        self.config = {
            'format': 'html',
            'style': 'cv',
        }
        super(BibTeXExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):  # noqa: N802
        """Extend the Markdown's behaviour."""
        md.preprocessors.add('bibtex', BibTeXPreprocessor(self.config), '_end')


def makeExtension(**kwargs):  # noqa: N802
    """Constructo a BibTeX extension."""
    return BibTeXExtension(**kwargs)
