"""Name check of the public directory (instruction v12 step 3; v13 step 3 = checks_v12 version plus files without an
extension, such as LICENSE, read as text): every file, searched for 尾崎, Ozaki, 原明美, Hara,
Akemi, 立花, 押, 先生, @ and 原 (each hit listed with its context, to be classed as a name or an ordinary word).
Latin terms are searched case-insensitively. What is searched, by file type:
  text (.R .csv .md .lock .txt .json, no extension): the file (UTF-8; CP932 as well);
  .xlsx: every zip member (XML) and, with openpyxl, the cells, comments and document properties;
  .rds: every string inside (values, names, attributes; R/rds_strings.R via Rscript);
  .pdf: metadata, XMP and the text of every page (pymupdf);
  .png: the text chunks (tEXt, zTXt, iTXt) and eXIf; .jpeg: the APPn and COM segments.
Bytes of binary data (numbers, pixels) are not searched as text, since they decode to arbitrary characters.
--selftest plants every term in one file of each text-bearing kind and must find all of them.

usage: python public_name_scan.py <public_root> <Rscript> [--selftest]
"""
import os, re, struct, subprocess, sys, tempfile, zipfile, zlib
sys.stdout.reconfigure(encoding="utf-8")
TERMS = ["尾崎", "Ozaki", "原明美", "Hara", "Akemi", "立花", "押", "先生", "@", "原"]
LATIN = {"Ozaki", "Hara", "Akemi"}
HERE = os.path.dirname(os.path.abspath(__file__))
TEXT_EXT = {".r", ".csv", ".md", ".lock", ".txt", ".json", ""}


def png_text(raw):
    out, i = [], 8
    while i + 8 <= len(raw):
        n, typ = struct.unpack(">I4s", raw[i:i + 8]); data = raw[i + 8:i + 8 + n]; i += 12 + n
        if typ == b"tEXt": out.append(data.decode("latin-1"))
        elif typ == b"zTXt":
            k, rest = data.split(b"\0", 1); out.append(k.decode("latin-1") + " " + zlib.decompress(rest[1:]).decode("latin-1"))
        elif typ == b"iTXt":
            k, rest = data.split(b"\0", 1); comp = rest[0]; parts = rest[2:].split(b"\0", 2)
            txt = zlib.decompress(parts[2]) if comp else parts[2]
            out.append(k.decode("latin-1") + " " + parts[0].decode("latin-1") + " " + parts[1].decode("utf-8", "ignore") + " " + txt.decode("utf-8", "ignore"))
        elif typ == b"eXIf": out.append(data.decode("latin-1"))
    return "\n".join(out)


def jpeg_text(raw):
    out, i = [], 2
    while i + 4 <= len(raw) and raw[i] == 0xFF:
        m = raw[i + 1]
        if m in (0xD9, 0xDA): break
        n = struct.unpack(">H", raw[i + 2:i + 4])[0]; seg = raw[i + 4:i + 2 + n]; i += 2 + n
        if 0xE0 <= m <= 0xEF or m == 0xFE:
            out.append(seg.decode("utf-8", "ignore")); out.append(seg.decode("cp932", "ignore"))
    return "\n".join(out)


def texts(path, rscript):
    ext = os.path.splitext(path)[1].lower()
    raw = open(path, "rb").read()
    if ext in TEXT_EXT:
        return [("utf-8", raw.decode("utf-8", "ignore")), ("cp932", raw.decode("cp932", "ignore"))]
    if ext == ".xlsx":
        z = zipfile.ZipFile(path)
        out = [(f"zip:{i.filename}", z.read(i.filename).decode("utf-8", "ignore")) for i in z.infolist()]
        from openpyxl import load_workbook
        wb = load_workbook(path)
        p = wb.properties
        out.append(("properties", " | ".join(f"{k}={getattr(p, k)}" for k in
                    ("creator", "lastModifiedBy", "title", "subject", "description", "keywords", "category"))))
        cells = []
        for ws in wb.worksheets:
            cells.append(ws.title)
            for row in ws.iter_rows():
                for c in row:
                    if c.value is not None: cells.append(str(c.value))
                    if c.comment is not None: cells.append(c.comment.text + " " + (c.comment.author or ""))
        out.append(("cells", "\n".join(cells)))
        return out
    if ext == ".rds":
        with tempfile.TemporaryDirectory() as d:
            o = os.path.join(d, "s.txt")
            r = subprocess.run([rscript, os.path.join(HERE, "rds_strings.R"), path, o], capture_output=True, text=True)
            assert os.path.exists(o), (path, r.stderr[-400:])
            return [("rds strings", open(o, encoding="utf-8", errors="ignore").read())]
    if ext == ".pdf":
        import fitz
        d = fitz.open(path)
        return [("metadata", " | ".join(f"{k}={v}" for k, v in (d.metadata or {}).items())),
                ("xmp", d.get_xml_metadata() or ""), ("text", "\n".join(pg.get_text() for pg in d))]
    if ext == ".png":
        return [("png text chunks", png_text(raw))]
    if ext in (".jpg", ".jpeg"):
        return [("jpeg APPn/COM", jpeg_text(raw))]
    raise SystemExit(f"no reader for {path}")


def count(term, s):
    return len(re.findall(re.escape(term), s, flags=re.I if term in LATIN else 0))


def scan(rootdir, rscript):
    res, ctx, n = {}, [], 0
    for dp, dns, fs in os.walk(rootdir):
        dns[:] = [d for d in dns if d != ".git"]
        for f in sorted(fs):
            p = os.path.join(dp, f); n += 1
            rel = os.path.relpath(p, rootdir).replace("\\", "/")
            T = texts(p, rscript)
            for t in TERMS:
                best = max((count(t, s), lab) for lab, s in T)
                if best[0]:
                    res.setdefault(rel, {})[t] = best
            for lab, s in T:
                if lab == "cp932" and any(l == "utf-8" for l, _ in T):
                    continue
                for m in re.finditer("尾崎|原明美|立花|押|先生|原|ozaki|hara|akemi|@", s, flags=re.I):
                    ctx.append((rel, lab, m.group(0), s[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")))
    return n, res, ctx


def main():
    rootdir, rscript = sys.argv[1], sys.argv[2]
    if "--selftest" in sys.argv:
        d = tempfile.mkdtemp()
        planted = " ".join(TERMS).replace("Hara", "HARA")
        open(os.path.join(d, "planted.csv"), "w", encoding="utf-8").write(planted)
        open(os.path.join(d, "PLANTED"), "w", encoding="utf-8").write(planted)
        from openpyxl import Workbook
        wb = Workbook(); wb.active["A1"] = planted; wb.properties.creator = "Akemi"; wb.save(os.path.join(d, "planted.xlsx"))
        subprocess.run([rscript, "-e", f"saveRDS(list(a = 1, note = enc2utf8('{planted}')), '{d.replace(os.sep, '/')}/planted.rds')"], check=True)
        _, res, _ = scan(d, rscript)
        for f in ("planted.csv", "PLANTED", "planted.xlsx", "planted.rds"):
            miss = [t for t in TERMS if t not in res.get(f, {})]
            print(f"selftest {f}: terms not found: {miss}")
            assert not miss
        return
    n, res, ctx = scan(rootdir, rscript)
    print(f"files scanned: {n}")
    tot = {t: 0 for t in TERMS}
    for rel, h in sorted(res.items()):
        print(f"  {rel}: " + ", ".join(f"{t}={k} ({lab})" for t, (k, lab) in h.items()))
        for t, (k, _) in h.items():
            tot[t] += k
    print("totals (largest view per file):", tot)
    seen = set()
    for rel, lab, g, c in ctx:
        key = (rel, g.lower(), c)
        if key not in seen:
            seen.add(key)
            print(f"CTX {rel} [{lab}] {g!r}: …{c}…")


if __name__ == "__main__":
    main()
