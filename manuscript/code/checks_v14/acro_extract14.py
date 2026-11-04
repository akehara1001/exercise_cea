"""Plain-text extraction for the ARS acronym check (WRITING_RULES 13): abstract = the four structured paragraphs without
their labels; body = Introduction to the end of Conclusion, headings included as plain lines; paragraphs separated by
blank lines. Each file is checked on its own as the body scope (abstract and main text are separate scopes, as in v13).
The method is validated by reproducing the v13 reports (checks_v13/out/acronyms_abs13.txt, acronyms_body13.txt).
usage: python acro_extract14.py <manuscript.docx> <abstract_out.txt> <body_out.txt>
"""
import sys
import docx

LABELS = ("Purpose", "Methods", "Results", "Conclusion")


def main(src, abs_out, body_out):
    P = [p.text for p in docx.Document(src).paragraphs]
    a0, i0, ack = P.index("Abstract"), P.index("Introduction"), P.index("Acknowledgments")
    ab = [t for t in P[a0 + 1:i0] if t.startswith(tuple(l + " " for l in LABELS))]
    assert len(ab) == 4
    ab = [t.split(" ", 1)[1] for t in ab]
    body = [t for t in P[i0:ack] if t.strip()]
    open(abs_out, "w", encoding="utf-8").write("\n\n".join(ab) + "\n")
    open(body_out, "w", encoding="utf-8").write("\n\n".join(body) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:4])
