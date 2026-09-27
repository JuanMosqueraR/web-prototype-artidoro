"""Build the Vite site for GitHub Pages (served under a project subpath) and optionally stage a local gh-pages commit.

Writes: --out (default dist/pages, git-ignored) and, with --branch-dir, a git repository in that directory
(outside this repo). Never adds a remote and never pushes. Needs Node 20.19+/22.12+ and `npm ci` already run.
Refuses to build if the site inputs have uncommitted changes, unless --allow-dirty.
"""
import argparse, glob, io, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUTS = ["index.html", "src", "public", "package.json", "package-lock.json", "vite.config.js"]


def run(cmd, cwd=ROOT, check=True):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode:
        sys.exit(f"command failed ({r.returncode}): {' '.join(map(str, cmd))}\n{r.stdout}{r.stderr}")
    return r.stdout.strip()


def read(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read()


def write(p, text):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def check_node(node):
    out = run([node, "--version"])
    major, minor = (int(x) for x in re.match(r"v(\d+)\.(\d+)", out).groups())
    if not (major > 22 or (major == 22 and minor >= 12) or (major == 20 and minor >= 19)):
        sys.exit(f"Node {out} does not satisfy Vite's engines (^20.19.0 || >=22.12.0). Pass a compatible binary with --node.")
    return out


def rewrite_for_subpath(site):
    """Turn root-absolute /assets/... into page-relative paths, so the site works under any URL prefix."""
    index = site / "index.html"
    html = read(index)
    html, n = re.subn(r"(?<![A-Za-z0-9_.\-])/assets/", "assets/", html)
    # Footer links written for a site root; #b is the routing main.js already supports.
    for old, new in (('href="/b/"', 'href="#b"'), ('href="/?motion=off"', 'href="?motion=off"')):
        if html.count(old) != 1:
            sys.exit(f"expected exactly one {old} in index.html; the page changed, update this script deliberately")
        html = html.replace(old, new)
    left = re.findall(r"""(?:href|src|srcset|poster|data-[a-z-]+)=["']/[^"']*""", html)
    if left:
        sys.exit("root-absolute references remain in index.html: " + ", ".join(sorted(set(left))))
    write(index, html)
    for css in glob.glob(str(site / "assets" / "index-*.css")):  # CSS lives in assets/, so its fonts are siblings
        text = re.sub(r"url\((['\"]?)/assets/", r"url(\1", read(css))
        if re.search(r"url\((['\"]?)/", text):
            sys.exit("root-absolute url() remains in " + css)
        write(css, text)
    for js in glob.glob(str(site / "assets" / "index-*.js")):
        if "/assets/" in read(js):
            sys.exit("a hard-coded /assets/ path exists in the JS bundle: " + js)
    write(site / ".nojekyll", "")
    return n


def stage_branch(site, branch_dir, source_commit, node_version, vite_version, dirty):
    d = Path(branch_dir).resolve()
    if d == ROOT or ROOT in d.parents:
        sys.exit("--branch-dir must be outside this repository")
    d.mkdir(parents=True, exist_ok=True)
    git = ["git", "-c", "core.autocrlf=false"]
    if not (d / ".git").exists():
        run(git + ["init", "-q", "-b", "gh-pages"], cwd=d)
    elif run(["git", "branch", "--show-current"], cwd=d) != "gh-pages":
        sys.exit(f"{d} is a git repository but not on branch gh-pages")
    for item in d.iterdir():
        if item.name != ".git":
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    shutil.copytree(site, d, dirs_exist_ok=True)
    run(git + ["add", "-A"], cwd=d)
    if subprocess.run(git + ["diff", "--cached", "--quiet"], cwd=str(d)).returncode == 0 and (d / ".git" / "refs" / "heads" / "gh-pages").exists():
        print("gh-pages already contains this exact build; nothing to commit")
        return d
    message = (
        "Publish Hero Lab static build for GitHub Pages\n\n"
        f"Source: {source_commit}{' plus UNCOMMITTED changes' if dirty else ''} (Vite {vite_version}, Node {node_version}). Paths adapted for hosting "
        "under a subpath by scripts/build-pages.py."
    )
    run(git + ["commit", "-q", "-m", message], cwd=d)
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--node", default="node", help="Node binary (default: node on PATH)")
    ap.add_argument("--out", default="dist/pages", help="output directory (default: dist/pages, git-ignored)")
    ap.add_argument("--branch-dir", help="also stage a local gh-pages commit in this directory (outside the repo)")
    ap.add_argument("--allow-dirty", action="store_true", help="build even if the site inputs have uncommitted changes")
    a = ap.parse_args()

    node_version = check_node(a.node)
    vite_js = ROOT / "node_modules" / "vite" / "bin" / "vite.js"
    if not vite_js.exists():
        sys.exit("node_modules/vite is missing; run `npm ci` first")
    vite_version = json.loads(read(ROOT / "node_modules" / "vite" / "package.json"))["version"]
    source_commit = run(["git", "rev-parse", "--short", "HEAD"])
    dirty = run(["git", "status", "--porcelain", "--"] + INPUTS)
    if dirty and not a.allow_dirty:
        sys.exit("site inputs have uncommitted changes (commit them, or pass --allow-dirty):\n" + dirty)

    out = (ROOT / a.out).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "site"
        run([a.node, str(vite_js), "build", "--outDir", str(raw), "--emptyOutDir"])
        n = rewrite_for_subpath(raw)
        out.mkdir(parents=True, exist_ok=True)
        for child in out.iterdir():  # empty it rather than delete it: Windows refuses to remove a directory in use
            shutil.rmtree(child) if child.is_dir() else child.unlink()
        shutil.copytree(raw, out, dirs_exist_ok=True)
    files = [p for p in out.rglob("*") if p.is_file()]
    print(f"built {out} from {source_commit}{' (DIRTY inputs)' if dirty else ''}: {len(files)} files, "
          f"{sum(p.stat().st_size for p in files)} bytes, {n} asset references made relative (Node {node_version}, Vite {vite_version})")

    if a.branch_dir:
        d = stage_branch(out, a.branch_dir, source_commit, node_version, vite_version, bool(dirty))
        print(f"gh-pages staged in {d}. Publish it yourself:\n"
              f"  cd \"{d}\"\n  git remote add origin <repo-url>   (once)\n  git push -u origin gh-pages\n"
              "Then Settings -> Pages -> Deploy from a branch -> gh-pages / (root). URL: https://<user>.github.io/<repo>/")


if __name__ == "__main__":
    main()
