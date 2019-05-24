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

            if s[:1] == '{' and s[-1:] == '}':
                s = s[1:-1]

            if self._format == 'html':
                s = self._latex_to_unicode(s)

            entry[key] = s

        # Dispatch the entry to the method for this style and the entry type.
        format_name = ('_format_' + self._format + '_' + self._style + '_' +
                       entry['ENTRYTYPE'])
        if hasattr(self, format_name):
            lines = getattr(self, format_name)(entry)
            if lines:
                if self._format == 'html':
                    return [''] + [(
                        ('1. ' if i == 0 else '') + line
                    ) for i, line in enumerate(lines)] + ['']
                elif self._format == 'latex':
                    lines = [self._html_to_latex(l) for l in lines]
                    return (['', '\\bibitem{{{0}}}'.format(entry['ID'])] +
                            lines + [''])

        return None

    def _format_html_cv_article(self, entry):
        if 'title' not in entry or 'author' not in entry:
            return None

        lines = StringList()
        lines.add(self._cv_title(entry))
        lines.add_break()
        lines.add(self._cv_subtitle(entry))
        lines.add_break()
        lines.add(self._cv_author(entry))
        lines.add_break()
        lines.add(self._cv_journal(entry))
        lines.add_sep()
        lines.add(self._cv_preprint(entry))
        lines.cancel_sep()
        lines.add(self._cv_inspire(entry))
        lines.add(self._cv_mathscinet(entry))
        lines.add(self._cv_github(entry))
        lines.add_break()
        lines.add(self._cv_proceedings_info(entry))
        lines.cancel_sep()
        lines.add(self._cv_note(entry))

        return lines

    def _format_html_cv_inproceedings(self, entry):
        return self._format_html_cv_article(entry)

    def _format_html_cv_phdthesis(self, entry):
        if 'title' not in entry:
            return None

        lines = StringList()
        lines.add(self._cv_title(entry))
        lines.add_break()
        lines.add(self._cv_subtitle(entry))
        lines.add_break()
        lines.add(self._cv_author(entry))
        lines.add_break()
        lines.add(self._get_field(entry, 'month'))
        lines.add(self._get_field(entry, 'year'))
        lines.add_sep()
        lines.add(self._get_field(entry, 'school'))
        lines.cancel_sep()
        lines.add(self._cv_note(entry))
        lines.add(self._cv_ndl(entry))

        return lines

    def _format_html_cv_talk(self, entry):
        if 'title' not in entry:
            return None

        lines = StringList()
        lines.add(self._cv_title(entry))
        lines.add_break()
        lines.add(self._cv_subtitle(entry))
        lines.add_break()
        lines.add(self._cv_author(entry))
        lines.add_break()
        lines.add(self._cv_conftitle(entry))
        lines.add_sep()
        lines.add(self._cv_progno(entry))
        lines.add_sep()
        lines.add(self._get_field(entry, 'place'))
        lines.add_sep()
        lines.add(self._get_field(entry, 'city'))
        lines.add_sep()
        lines.add(self._get_field(entry, 'country'))
        lines.add_sep()
        lines.add(self._cv_date(entry))
        lines.cancel_sep()
        lines.add(self._cv_note(entry))
        lines.add(self._cv_cinii(entry))
        lines.add(self._cv_slides(entry))
        lines.add(self._cv_video(entry))

        return lines

    def _format_latex_cv_article(self, entry):
        if 'title' not in entry or 'author' not in entry:
            return None

        lines = StringList()
        lines.add(self._cv_author(entry))
        lines.add_sep_break()
        lines.add(self._cv_title(entry))
        lines.add_quote()
        lines.add_sep_break()
        lines.add(self._cv_journal(entry))
        lines.add_sep()
        lines.add(self._cv_preprint(entry))
        lines.add_sep_break()
        lines.add(self._cv_proceedings_info(entry))
        lines.add_period()

        return lines

    def _format_latex_cv_inproceedings(self, entry):
        return self._format_latex_cv_article(entry)

    def _format_latex_cv_phdthesis(self, entry):
        if 'title' not in entry:
            return None

        lines = StringList()
        lines.add(self._cv_author(entry))
        lines.add_sep_break()
        lines.add(self._cv_title(entry))
        lines.add_quote()
        lines.add_sep_break()
        lines.add(self._cv_subtitle(entry))
        lines.add_sep_break()
        lines.add(self._get_field(entry, 'month'))
        lines.add(self._get_field(entry, 'year'))
        lines.add_sep()
        lines.add(self._get_field(entry, 'school'))
        lines.cancel_sep()
        lines.add(self._cv_note(entry))
        lines.add_period()

        return lines

    def _format_latex_cv_talk(self, entry):
        if 'title' not in entry:
            return None

        lines = StringList()
        lines.add(self._cv_author(entry))
        lines.add_sep_break()
        lines.add(self._cv_title(entry))
        lines.add_quote()
        lines.add_sep_break()
#        lines.add(self._cv_subtitle(entry))
#        lines.add_sep_break()
        lines.add(self._cv_conftitle(entry))
        lines.add_sep()
        lines.add(self._cv_progno(entry))
        lines.add_sep()
        lines.add(self._get_field(entry, 'place'))
        lines.add_sep()
        lines.add(self._get_field(entry, 'city'))
        lines.add_sep()
        lines.add(self._get_field(entry, 'country'))
        lines.add_sep()
        lines.add(self._cv_date(entry))
        lines.cancel_sep()
        lines.add(self._cv_note(entry))
        lines.add_period()

        return lines

    def _latex_to_unicode(self, s):
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
            # One often writes {\"o} in BibTeX: the curly braces should be
            # removed.
            s = s.replace('{{{0}}}'.format(r), simple_replacements[r])
            s = s.replace(r, simple_replacements[r])

        return s

    def _html_to_latex(self, s):
        s = s.replace('&nbsp;', '~')
        s = s.replace('&ndash;', '--')
        s = s.replace('&thinsp;', '')
        s = s.replace('&#39;', "'")
        s = re.sub(r'  $', r' \\\\', s)
        return s

    def _ndashify(self, s):
        # Smart "dash". Don't apply it for URLs.
        months = (
            r'January|February|March|April|May|June|'
            r'July|August|September|October|November|December'
        )

        return re.sub(
            r'(\d|' + months + r')-(\d|' + months + r')',
            r'\1&ndash;\2', s)

    def _apostrophify(self, s):
        # Single "'" is presumably an apostrophe. SmartyPants has a problem
        # for it. To avoid the problem, "'" needs to be replaced. Don't apply
        # it for math expressions, which may contain derivatives.
        if s.count("'") == 1:
            s = s.replace("'", '&#39;')
        return s

    def _canonicalize_author(self, s):
        # "bbb, aaa" -> "aaa bbb".
        s = s.split(',', 2)

        if len(s) == 1:
            s = s[0]
        else:
            s = s[1] + ' ' + s[0]

        # Handle spaces in an author name.
        s = re.sub(r'\.', '. ', s)
        s = re.sub(r'\s+', ' ', s)
        for _ in range(5):
            s = re.sub(r'([A-Z])\. ([A-Z])\.', r'\1.\2.', s)
        s = s.strip().replace(' ', '&nbsp;')

        return s

    def _canonicalize_date(self, s):
        months = (
            r'January|February|March|April|May|June|'
            r'July|August|September|October|November|December'
        )

        # Example: April 1-May 5, 2000 -> 1 April-5 May 2000
        m = re.search(
            r'(' + months + r')\s+(\d+)-(' + months + ')\s+(\d+)\s*,\s*(\d+)',
            s)
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

        # Example: April 1, 2000 -> 1 April 2000
        m = re.search(r'(' + months + r')\s+(\d+)\s*,\s*(\d+)', s)
        if m:
            s = '{0}{1} {2} {3}{4}'.format(
                s[:m.start()],
                m.group(2),
                m.group(1),
                m.group(3),
                s[m.end():]
            )

        s = self._ndashify(s)
        return s

    def _get_field(self, entry, field):
        if field not in entry:
            return None
        return entry[field]

    def _get_authors(self, entry):
        """Read the authors in an entry and return a list of strings."""
        authors = re.split(r'\band\b', entry['author'])

        return [self._canonicalize_author(a) for a in authors]

    def _make_bf(self, text):
        if self._format == 'html':
            return '**{0}**'.format(text.strip())
        elif self._format == 'latex':
            return r'{{\bfseries {0}}}'.format(text)

    def _make_it(self, text):
        if self._format == 'html':
            return ' *{0}* '.format(text.strip())
        elif self._format == 'latex':
            return r'{{\itshape {0}\/}}'.format(text)

    def _make_link(self, text, url):
        if self._format == 'html':
            return '[{0}]({1})'.format(text, url)
        elif self._format == 'latex':
            return r'\href{{{0}}}{{{1}}}'.format(url, text)

    def _make_button(self, text, url):
        return '[<small>[{0}]</small>]({1})'.format(text, url)

    def _cv_title(self, entry):
        if 'title' not in entry:
            return None

        if self._format == 'html':
            return self._make_bf(entry['title'])
        elif self._format == 'latex':
            return entry['title']

    def _cv_subtitle(self, entry):
        if 'subtitle' not in entry:
            return None

        return '(' + self._make_it(entry['subtitle'] + '&thinsp;') + ')'

    def _cv_author(self, entry):
        if 'author' not in entry:
            return None

        def has_cjk(string):
            import unicodedata
            for c in string:
                name = unicodedata.name(c)
                if ('CJK UNIFIED' in name or 'HIRAGANA' in name or
                        'KATAKANA' in name):
                    return True
            return False

        authors = self._get_authors(entry)

        if any(has_cjk(a) for a in authors):
            return ', '.join(authors)
        else:
            aa = []
            for i, a in enumerate(authors):

                # Join it by a comma or "and".
                if i == len(authors) - 2:
                    a += ' and '
                elif i <= len(authors) - 3:
                    a += ', '
                aa.append(a)
            return ''.join(aa)

    def _cv_journal(self, entry):
        if 'journal' not in entry:
            return None
        if 'year' not in entry:
            return None
        if 'pages' not in entry:
            return None

        # Canonicalize spaces.
        s = entry['journal']
        s = s.replace('.', '. ')
        s = re.sub(r'\s\s+', ' ', s)
        if self._format == 'latex':
            s += ' '
            s = s.replace(r'. ', r'.\ ')

        s = self._make_it(s)

        if 'volume' in entry:
            s = '{0}{1} ({2}) {3}'.format(
                s,
                self._make_bf(entry['volume']),
                entry['year'],
                entry['pages'],
            )
        else:
            s = '{0} ({1}) {2}'.format(
                s,
                entry['year'],
                entry['pages'],
            )
        s = self._ndashify(s)
        s = self._apostrophify(s)
        if 'doi' in entry:
            s = self._make_link(s, 'https://doi.org/' + entry['doi'])
        return s

    def _cv_preprint(self, entry):
        if 'eprint' not in entry:
            return None
        if 'archiveprefix' not in entry:
            return None

        if entry['archiveprefix'] == 'arXiv':
            if entry['eprint'].find('/') >= 0:
                return self._make_link(
                    'arXiv:' + entry['eprint'],
                    'https://arxiv.org/abs/' + entry['eprint']
                )
            if 'primaryclass' in entry:
                return self._make_link(
                    'arXiv:{0} [{1}]'.format(
                        entry['eprint'],
                        entry['primaryclass'],
                    ),
                    'https://arxiv.org/abs/' + entry['eprint']
                )

        return None

    def _cv_inspire(self, entry):
        if 'slaccitation' in entry:
            # This BibTex entry most likely is taken from INSPIRE-HEP.
            if 'eprint' in entry and 'archiveprefix' in entry:
                if entry['archiveprefix'] == 'arXiv':
                    return self._make_button(
                        'INSPIRE',
                        ('https://inspirehep.net/search?'
                         'p=find+eprint+{0}'.format(entry['eprint']))
                    )

        if 'inspirehep' in entry:
            return self._make_button(
                'INSPIRE',
                'https://inspirehep.net/search?p=find+{0}'.format(
                    entry['inspirehep'])
            )

        return None

    def _cv_mathscinet(self, entry):
        if 'mr' in entry:
            return self._make_button(
                'MathSciNet',
                'https://mathscinet.ams.org/mathscinet-getitem?mr={0}'.format(
                    entry['mr'])
            )
        return None

    def _cv_github(self, entry):
        if 'github' in entry:
            return self._make_button(
                'GitHub',
                'https://github.com/{0}'.format(entry['github'])
            )

    def _cv_cinii(self, entry):
        if 'cinii' in entry:
            return self._make_button(
                'CiNii',
                'https://ci.nii.ac.jp/naid/{0}'.format(entry['cinii'])
            )

    def _cv_ndl(self, entry):
        if 'ndl' in entry:
            return self._make_button(
                'NDL',
                'https://id.ndl.go.jp/bib/{0}'.format(entry['ndl'])
            )

    def _cv_slides(self, entry):
        if 'slidesurl' in entry:
            return self._make_button(
                'Slides',
                entry['slidesurl']
            )
        if 'speakerdeck' in entry:
            if entry['speakerdeck'].endswith('.pdf'):
                # TODO: Is this a permalink?
                return self._make_button(
                    'Slides',
                    ('https://speakerd.s3.amazonaws.com/'
                     'presentations/{0}'.format(entry['speakerdeck']))
                )
            else:
                return self._make_button(
                    'Slides',
                    'https://speakerdeck.com/{0}'.format(entry['speakerdeck'])
                )

    def _cv_video(self, entry):
        if 'youtube' in entry:
            return self._make_button(
                'Video',
                'https://www.youtube.com/watch?v={0}'.format(entry['youtube'])
            )

    def _cv_proceedings_info(self, entry):
        if 'booktitle' not in entry:
            return None

        # Example: Proceedings, Conference name: place, date
        m = re.search('Proceedings,(.*):([^:]*)$', entry['booktitle'])
        if m:
            confname = m.group(1).strip()
            confplace = m.group(2).strip()  # also date

            if 'confurl' in entry:
                confname = self._make_link(confname, entry['confurl'])

            confplace = self._canonicalize_date(confplace)

            s = 'Proceedings for {0}, {1}'.format(confname, confplace)

            if 'speaker' in entry:
                s += ' (Speaker:&nbsp;{0})'.format(
                    self._canonicalize_author(entry['speaker']))

            return s

        return None

    def _cv_conftitle(self, entry):
        if 'conftitle' not in entry:
            return None

        s = entry['conftitle']
        if 'confabbr' in entry:
            s += ' (' + entry['confabbr'] + ')'
        if 'confurl' in entry:
            s = self._make_link(s, entry['confurl'])

        return s

    def _cv_date(self, entry):
        if 'date' not in entry:
            return None
        return self._canonicalize_date(entry['date'])

    def _cv_progno(self, entry):
        if 'progno' not in entry:
            return None
        s = entry['progno']
        if 'progurl' in entry:
            s = self._make_link(s, entry['progurl'])
        return s

    def _cv_note(self, entry):
        if 'note' not in entry:
            return None
        return '({0})'.format(entry['note'])


class StringList(list):
    """List for strings."""

    def __init__(self, *args):
        """Construct a string list."""
        super(StringList, self).__init__(*args)
        self._clean = True
        self._sep = False
        self._cancel_sep = False
        self._break = False
        self._quote = False

    def _update(self):
        if self._sep and not self._cancel_sep:
            self[-1] += ','
        if self._quote:
            self[-1] = '``' + self[-1] + "''"
        if self._break:
            self[-1] += '  '
        self._clean = True
        self._sep = False
        self._cancel_sep = False
        self._break = False
        self._quote = False

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

    def add_sep_break(self):
        """Add a commna and a line break."""
        if not self._clean:
            self._clean = True
            self._sep = True
            self._cancel_sep = False
            self._break = True
        elif self._sep:
            self._sep = True
            self._cancel_sep = False
            self._break = True

    def add_quote(self):
        """Add a quote to the last line."""
        if not self._clean:
            self._quote = True

    def add_period(self):
        """Add a period at the end of the last line."""
        if self:
            if self._quote:
                self[-1] = '``' + self[-1] + ".''"
            elif self[-1][-1] != '.':
                self[-1] += '.'
        self._clean = True
        self._sep = False
        self._cancel_sep = False
        self._break = False
        self._quote = False


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


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] [--] files..'
    )
    parser.add_argument('--format',
                        action='store',
                        default='latex',
                        help='set the format (default: latex)',
                        metavar='FORMAT')
    parser.add_argument('--style',
                        action='store',
                        default='cv',
                        help='set the style (default: cv)',
                        metavar='STYLE')
    parser.add_argument('files',
                        nargs='*',
                        type=argparse.FileType('r'),
                        help=argparse.SUPPRESS)
    args = parser.parse_args()

    pp = BibTeXPreprocessor({
        'format': args.format,
        'style': args.style,
    })

    for f in args.files:
        lines = pp.run([l.decode('UTF-8').rstrip() for l in f.readlines()])
        for l in lines:
            print(l.encode('UTF-8'))
