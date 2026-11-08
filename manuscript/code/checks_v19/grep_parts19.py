"""Search every XML part of docx files (document, headers, footers, footnotes, comments, core properties) for
patterns, on the concatenated w:t text of each paragraph (so matches across runs are found) and on the raw XML of
non-WordprocessingML parts (docProps). Prints file, part, paragraph index and a context window.
usage: python grep_parts19.py <pattern-regex> <docx> [<docx> ...]
"""
import re, sys, zipfile
from lxml import etree

sys.stdout.reconfigure(encoding="utf-8")
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def paras(root):
    for p in root.iter("{%s}p" % W):
        yield "".join(t.text or "" for t in p.iter("{%s}t" % W))


def main(pat, files):
    rx = re.compile(pat)
    total = 0
    for f in files:
        z = zipfile.ZipFile(f)
        for name in z.namelist():
            if not name.endswith(".xml"):
                continue
            data = z.read(name)
            if name.startswith("word/"):
                try:
                    root = etree.fromstring(data)
                except etree.XMLSyntaxError:
                    continue
                for i, s in enumerate(paras(root)):
                    for m in rx.finditer(s):
                        total += 1
                        a, b = max(0, m.start() - 70), min(len(s), m.end() + 70)
                        print(f"{f.rsplit('/', 1)[-1]} | {name} | p{i} | ...{s[a:b]}...")
            else:
                s = data.decode("utf-8", "replace")
                for m in rx.finditer(s):
                    total += 1
                    a, b = max(0, m.start() - 70), min(len(s), m.end() + 70)
                    print(f"{f.rsplit('/', 1)[-1]} | {name} | raw | ...{s[a:b]}...")
    print("matches:", total)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
