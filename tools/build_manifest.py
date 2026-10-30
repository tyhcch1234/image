#!/usr/bin/env python3
"""Rebuild thumbnails + data/images.json from collections/*/meta.json.

Usage:  python3 tools/build_manifest.py
Add a new collection:  put images in collections/<slug>/, write meta.json, run this.
"""
import json
import os
from datetime import date

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLL = os.path.join(ROOT, "collections")
EXT = (".png", ".jpg", ".jpeg", ".webp")
THUMB_W = 760


def human(n):
    for i, unit in enumerate(("B", "KB", "MB", "GB")):
        if n < 1024 or i == 3:
            return ("%d %s" % (n, unit)) if (n >= 10 or i == 0) else ("%.1f %s" % (n, unit))
        n /= 1024.0


def build():
    collections = []
    for slug in sorted(os.listdir(COLL)):
        cdir = os.path.join(COLL, slug)
        if not os.path.isdir(cdir):
            continue
        meta_path = os.path.join(cdir, "meta.json")
        meta = {}
        if os.path.exists(meta_path):
            with open(meta_path, encoding="utf-8") as fh:
                meta = json.load(fh)

        titles = meta.get("titles", {})
        tdir = os.path.join(cdir, "thumbs")
        os.makedirs(tdir, exist_ok=True)

        items = []
        for name in sorted(os.listdir(cdir)):
            if not name.lower().endswith(EXT):
                continue
            path = os.path.join(cdir, name)
            im = Image.open(path)
            w, h = im.size
            stem = os.path.splitext(name)[0]
            tname = stem + ".jpg"
            tpath = os.path.join(tdir, tname)
            if (not os.path.exists(tpath)) or os.path.getmtime(tpath) < os.path.getmtime(path):
                th = im.convert("RGB")
                if th.width > THUMB_W:
                    th = th.resize((THUMB_W, round(th.height * THUMB_W / th.width)), Image.LANCZOS)
                th.save(tpath, "JPEG", quality=84, optimize=True)
            items.append({
                "title": titles.get(name, stem),
                "src": "%s/%s/%s" % ("collections", slug, name),
                "thumb": "%s/%s/thumbs/%s" % ("collections", slug, tname),
                "w": w,
                "h": h,
                "ratio": "%.4g : %.4g" % (w / h, 1),
                "size": human(os.path.getsize(path)),
            })

        pdf = meta.get("pdf")
        collections.append({
            "slug": slug,
            "title": meta.get("title", slug),
            "subtitle": meta.get("subtitle", ""),
            "desc": meta.get("desc", ""),
            "date": meta.get("date", ""),
            "items": items,
            "pdf": ("collections/%s/%s" % (slug, pdf)) if pdf else None,
            "pdf_label": meta.get("pdf_label", "合集 PDF"),
        })

    data = {
        "updated": date.today().isoformat(),
        "count": sum(len(c["items"]) for c in collections),
        "collections": collections,
    }
    out = os.path.join(ROOT, "data", "images.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print("wrote %s — %d collections, %d images" % (out, len(collections), data["count"]))


if __name__ == "__main__":
    build()
