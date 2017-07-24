"""Python Markdown BibTeX extension."""

import re

import bibtexparser

from markdown import Extension
from markdown.preprocessors import Preprocessor


class BibTeXPreprocessor(Preprocessor):
    """Preprocessor to handle BibTeX code."""

    def __init__(self, config):
        """Construct a BibTeX preprocessor."""
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
                    result_lines = self.parse_bibtex_entry(current_block)
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

    def parse_bibtex_entry(self, lines):
        """Parse a BibTeX entry."""
        entries = bibtexparser.loads('\n'.join(lines)).entries
        if len(entries) != 1:
            return None
        entry = entries[0]

        for key in ('title', 'author'):
            if key in entry:
                entry[key] = re.sub(r'\s+', ' ', entry[key].strip())

        format_name = '_format_' + self._style + '_' + entry['ENTRYTYPE']

        if hasattr(self, format_name):
            lines = getattr(self, format_name)(entry)
            if lines:
                return [''] + [(
                    ('1. ' if i == 0 else '') + line
                ) for i, line in enumerate(lines)] + ['']

        return None

    def _format_cv_article(self, entry):
        if 'title' not in entry or 'author' not in entry:
            return None

        lines = StringList()
        lines.add('**{0}**'.format(entry['title']))
        lines.add_break()
        lines.add(_cv_author(entry))
        lines.add_break()
        lines.add(_cv_journal(entry))
        lines.add_sep()
        lines.add(_cv_preprint(entry))
        lines.add(_cv_inspire(entry))

        return lines


def _cv_author(entry):
    if 'author' not in entry:
        return None

    authors = _get_authors(entry)
    aa = []
    for i, a in enumerate(authors):
        if i == len(authors) - 2:
            a += ' and '
        elif i <= len(authors) - 3:
            a += ', '
        aa.append(a)

    s = ''.join(aa)

    s = re.sub(r'\.', '. ', s)
    s = re.sub(r'\s+', ' ', s)
    for i in range(5):
        s = re.sub(r'([A-Z])\. ([A-Z])\.', r'\1.\2.', s)

    return s


def _get_authors(entry):
    authors = re.split(r'\band\b', entry['author'])

    def normalize_author(s):
        s = s.split(',', 2)
        if len(s) == 1:
            s = s[1]
        else:
            s = s[1] + s[0]
        return s

    return [normalize_author(a) for a in authors]


def _cv_journal(entry):
    if 'journal' not in entry:
        return None
    if 'volume' not in entry:
        return None
    if 'year' not in entry:
        return None
    if 'pages' not in entry:
        return None
    s = '{0} {1} ({2}) {3}'.format(
        entry['journal'],
        entry['volume'],
        entry['year'],
        entry['pages'],
    )
    if 'doi' in entry:
        s = '[{0}](https://doi.org/{1})'.format(s, entry['doi'])
    return s


def _cv_preprint(entry):
    if 'eprint' not in entry:
        return None
    if 'archiveprefix' not in entry:
        return None

    if entry['archiveprefix'] == 'arXiv':
        if 'primaryclass' in entry:
            return '[arXiv:{0} [{1}]](https://arxiv.org/abs/{0})'.format(
                entry['eprint'],
                entry['primaryclass'],
            )

    return None


def _cv_inspire(entry):
    if 'eprint' in entry and 'archiveprefix' in entry:
        if entry['archiveprefix'] == 'arXiv':
            return (
                '[<small>[INSPIRE]</small>]'
                '(https://inspirehep.net/search?p=find+eprint+{0})'
            ).format(entry['eprint'])

    return None


class StringList(list):
    """List for strings."""

    def __init__(self, *args):
        """Construct a string list."""
        super(StringList, self).__init__(*args)
        self._clean = True
        self._sep = False
        self._break = False

    def _update(self):
        if self._sep:
            self[-1] += ','
        if self._break:
            self[-1] += '  '
        self._clean = True
        self._sep = False
        self._break = False

    def add(self, s):
        """Add a line."""
        if s:
            self._update()
            self.append(s)
            self._clean = False

    def add_sep(self):
        """Add a comma at the end of the last line."""
        if not self._clean:
            self._clean = True
            self._sep = True

    def add_break(self):
        """Add a line break."""
        if not self._clean:
            self._clean = True
            self._sep = False
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
            'style': 'cv',
        }
        super(BibTeXExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):  # noqa: N802
        """Extend the Markdown's behaviour."""
        md.preprocessors.add('bibtex', BibTeXPreprocessor(self.config), '_end')


def makeExtension(**kwargs):  # noqa: N802
    """Constructo a BibTeX extension."""
    return BibTeXExtension(**kwargs)
