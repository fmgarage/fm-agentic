#!/usr/bin/env python3
"""Regeneriert alle Referenzdateien dieses Skills von help.claris.com:

  references/functions.md      — alle Funktionen (EN-Name | slug, nach Kategorie)
  references/script-steps.md   — alle Script Steps (EN-Name | slug, nach Kategorie)
  references/mapping-de-en.md  — Deutsch | English | slug

Quelle: die MadCap-Flare-TOC der Claris-Hilfe (server-seitig statisch):
  https://help.claris.com/{locale}/pro-help/Data/Tocs/main_toc.js        (Baum)
  https://help.claris.com/{locale}/pro-help/Data/Tocs/main_toc_ChunkN.js (Titel)
Slugs sind sprachneutral — das de/en-Mapping ist ein Join über den Slug.

Aufruf im Skill-Verzeichnis:  python3 scripts/update.py
Benötigt nur Python 3 (stdlib) und Internetzugang.
"""
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
REFS = BASE / "references"
TOC = "https://help.claris.com/{}/pro-help/Data/Tocs/{}"
CHUNK_ENTRY = re.compile(
    r"'/content/(?P<slug>[a-z0-9\-_]+)\.html':\{i:\[(?P<i>\d+)\],"
    r"t:\['(?P<title>.*?)'\],b:"
)


def fetch(locale, name):
    url = TOC.format(locale, name)
    print(f"  … {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


def load_toc(locale):
    """Liefert (tree, idx) — idx: TOC-Index → (slug, Titel)."""
    main = fetch(locale, "main_toc.js")
    numchunks = int(re.search(r"numchunks:(\d+)", main).group(1))
    idx = {}
    for k in range(numchunks):
        chunk = fetch(locale, f"main_toc_Chunk{k}.js")
        for m in CHUNK_ENTRY.finditer(chunk):
            idx[int(m.group("i"))] = (
                m.group("slug"),
                m.group("title").replace("\\'", "'"),
            )
    tree_src = main[main.index("tree:") + 5:]
    tree_src = re.sub(r"\}\)\s*;?\s*$", "", tree_src)
    tree_src = re.sub(r"([nic]):", r'"\1":', tree_src)  # Baum enthält keine Strings
    return json.loads(tree_src), idx


def find_node(node, idx, title):
    slug_title = idx.get(node.get("i"))
    if slug_title and slug_title[1] == title:
        return node
    for child in node.get("n", []):
        hit = find_node(child, idx, title)
        if hit:
            return hit
    return None


def build_index(tree, idx, node_title, out_name, doc_title):
    node = find_node(tree, idx, node_title)
    if not node:
        sys.exit(f"TOC-Knoten '{node_title}' nicht gefunden — Struktur prüfen.")
    lines = [
        f"# {doc_title}",
        f"<!-- generiert {date.today().isoformat()} von scripts/update.py "
        f"aus der Claris-Hilfe-TOC — nicht von Hand editieren -->",
        "",
        "Format: `Name | slug` — Doku-URL: "
        "`https://help.claris.com/markdown/{en|de}/pro-help/<slug>.md`",
    ]
    collected = {}
    for cat in node.get("n", []):
        cat_st = idx.get(cat.get("i"))
        entries = [idx[e["i"]] for e in cat.get("n", []) if e.get("i") in idx]
        if not cat_st or not entries:
            continue
        lines += ["", f"## {cat_st[1]}", ""]
        for slug, title in entries:
            lines.append(f"{title} | {slug}")
            collected[slug] = title
    (REFS / out_name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: {out_name} — {len(collected)} Einträge")
    return collected


def build_mapping(de_idx, func_slugs, step_slugs):
    de_by_slug = {slug: title for slug, title in de_idx.values()}

    def section(header, slugs):
        rows = ["", f"## {header}", "", "Deutsch | English | slug"]
        missing = []
        pairs = []
        for slug, en in slugs.items():
            de = de_by_slug.get(slug)
            (pairs if de else missing).append((de, en, slug) if de else slug)
        for de, en, slug in sorted(pairs, key=lambda p: p[0].lower()):
            rows.append(f"{de} | {en} | {slug}")
        if missing:
            rows.append(f"\n<!-- ohne de-Titel: {', '.join(missing)} -->")
        return rows

    out = [
        "# FileMaker de/en-Mapping — Funktionen und Script Steps",
        f"<!-- generiert {date.today().isoformat()} von scripts/update.py "
        f"aus der Claris-Hilfe-TOC (de/en) — nicht von Hand editieren -->",
        "",
        "Format: `Deutsch | English | slug` — Doku-URL: "
        "`https://help.claris.com/markdown/{en|de}/pro-help/<slug>.md`",
    ]
    out += section("Funktionen", func_slugs)
    out += section("Script Steps", step_slugs)
    (REFS / "mapping-de-en.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    n = sum(1 for s in {**func_slugs, **step_slugs} if s in de_by_slug)
    print(f"OK: mapping-de-en.md — {n} von {len(func_slugs) + len(step_slugs)} gemappt")


if __name__ == "__main__":
    REFS.mkdir(exist_ok=True)
    print("Lade englische TOC …")
    tree, en_idx = load_toc("en")
    funcs = build_index(tree, en_idx, "Functions reference",
                        "functions.md", "FileMaker Pro — Funktionen (EN-Namen)")
    steps = build_index(tree, en_idx, "Script steps reference",
                        "script-steps.md", "FileMaker Pro — Script Steps (EN-Namen)")
    print("Lade deutsche TOC …")
    _, de_idx = load_toc("de")
    build_mapping(de_idx, funcs, steps)
