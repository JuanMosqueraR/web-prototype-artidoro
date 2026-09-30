"""Build the publishable copy of deliverables/presentacion-artidoro.html for a claude.ai Artifact.

The Artifact viewer adds its own html/head/body skeleton, only loads fonts it can reach and resolves
images relative to the page. This script:
  - removes the document skeleton and the local-only meta tags;
  - inlines the three woff2 fonts as data: URIs;
  - copies every referenced image next to the page (assets/ for public/assets, capturas/ for QA captures)
    and rewrites the ../ paths to those flat folders.

Writes: --out (default dist/presentation-artifact, git-ignored), replacing it entirely. Reads nothing
outside this repo and never publishes: publishing is a manual Artifact call that uses the printed
page path and the files map (JSON on the last line).
"""
import argparse, base64, io, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "deliverables" / "presentacion-artidoro.html"
SKELETON = [
    "<!doctype html>\n", '<html lang="es">\n', "<head>\n", '<meta charset="utf-8">\n',
    '<meta name="viewport" content="width=device-width,initial-scale=1">\n',
    '<meta name="robots" content="noindex">\n', "</head>\n", "<body>\n", "</body>\n", "</html>\n",
]
FONTS = ["chivo-regular.woff2", "chivo-bold.woff2", "barlow-condensed-800.woff2"]
IMAGE_DIRS = {"../public/assets/": ("public/assets", "assets"), "../qa/": ("qa", "capturas")}


def read(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read()


def write(p, text):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def build(out):
    page = read(SOURCE)
    for tag in SKELETON:
        if page.count(tag) != 1:
            sys.exit(f"expected exactly one {tag.strip()!r} in {SOURCE.name}; update SKELETON if the page changed")
        page = page.replace(tag, "")
    page = re.sub(r"<!--\n  Presentación para la reunión.*?-->\n",
                  f"<!-- Copia publicable generada por scripts/{Path(__file__).name} desde deliverables/{SOURCE.name}. -->\n",
                  page, count=1, flags=re.S)
    page = page.replace("(() => {\n  const stage", "(() => {\n  document.documentElement.lang = 'es';\n  const stage", 1)

    for font in FONTS:
        ref = f"url('../public/assets/{font}')"
        if page.count(ref) != 1:
            sys.exit(f"font reference not found once: {ref}")
        data = base64.b64encode((ROOT / "public" / "assets" / font).read_bytes()).decode()
        page = page.replace(ref, f"url(data:font/woff2;base64,{data})")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    files = {}
    for prefix, (src_root, dest) in IMAGE_DIRS.items():
        for ref in sorted(set(re.findall(re.escape(prefix) + r"([\w./-]+?\.(?:png|webp|jpg))", page))):
            src = ROOT / src_root / ref
            if not src.is_file():
                sys.exit(f"missing image: {src}")
            name = Path(ref).name
            published = f"{dest}/{name}"
            if published in files and files[published] != str(src):
                sys.exit(f"two images would publish as {published}")
            (out / dest).mkdir(exist_ok=True)
            shutil.copy2(src, out / published)
            files[published] = str((out / published).resolve())
            page = page.replace(prefix + ref, published)
    if "../" in page:
        sys.exit("unresolved ../ reference left in the page")

    target = out / "propuesta-artidoro.html"
    write(target, page)
    return target, files


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "dist" / "presentation-artifact"))
    out = Path(ap.parse_args().out).resolve()
    target, files = build(out)
    size = sum(Path(p).stat().st_size for p in files.values())
    print(f"page: {target} ({target.stat().st_size} bytes)")
    print(f"images: {len(files)} files, {size} bytes")
    print(json.dumps(files, ensure_ascii=False))


if __name__ == "__main__":
    main()
