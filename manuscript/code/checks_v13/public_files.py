"""File list of the public directory (sha256, first 16) with the change since the v12 list
(checks_v12/out/public_files.txt): added, removed, changed, or unchanged. The .git directory is left out.
usage: python public_files.py <public_root> <v12 list> <out>
"""
import hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")


def main(root, old, out):
    prev = dict(reversed(l.split(None, 1)) for l in open(old, encoding="utf-8").read().splitlines() if l.strip())
    prev = {k.strip(): v for k, v in prev.items()}
    now = {}
    for dp, dns, fs in os.walk(root):
        dns[:] = [d for d in dns if d != ".git"]
        for f in fs:
            p = os.path.join(dp, f)
            now[os.path.relpath(p, root).replace("\\", "/")] = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    rows, n = [], {"added": 0, "removed": 0, "changed": 0, "unchanged": 0}
    for f in sorted(set(prev) | set(now)):
        st = "removed" if f not in now else "added" if f not in prev else "changed" if now[f] != prev[f] else "unchanged"
        n[st] += 1
        rows.append(f"{now.get(f, '-' * 16)}  {st:9}  {f}")
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(rows) + "\n")
    print(f"v12 {len(prev)} files; now {len(now)} files;", n)
    for r in rows:
        if " unchanged " not in r:
            print(r)


if __name__ == "__main__":
    main(*sys.argv[1:4])
