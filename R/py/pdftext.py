"""Normalised full text of a PDF with page lookup, for regex extraction of reported values."""
import re
import bisect
import pymupdf

DROP_LINES = re.compile(r"^(The New England Journal of Medicine is produced by|Downloaded from nejm\.org|"
                        r"Author Manuscript$|Lancet Oncol\. Author manuscript)")


class PdfText:
    def __init__(self, path):
        doc = pymupdf.open(path)
        parts, starts, pos = [], [], 0
        for page in doc:
            lines = [ln for ln in page.get_text().splitlines() if not DROP_LINES.match(ln.strip())]
            t = "\n".join(lines) + "\n"
            t = t.replace("\xad", "").replace("​", "").replace(" ", " ").replace(" ", " ")
            t = re.sub(r"(?<=[a-z])-\n(?=[a-z])", "", t)      # hyphenation at line ends
            t = re.sub(r"\s+", " ", t)
            starts.append(pos)
            parts.append(t)
            pos += len(t)
        self.text = "".join(parts)
        self.starts = starts

    def page_of(self, offset):
        return bisect.bisect_right(self.starts, offset)

    def find(self, pattern, flags=0):
        """First match of pattern: (match, page). Raises if absent."""
        m = re.search(pattern, self.text, flags)
        if m is None:
            raise LookupError(f"pattern not found: {pattern}")
        return m, self.page_of(m.start())
