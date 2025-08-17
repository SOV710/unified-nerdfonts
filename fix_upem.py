#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from fontTools.ttLib import TTFont, TTCollection
from fontTools.ttLib.scaleUpem import scale_upem

EXTS = {".ttf", ".otf", ".ttc", ".otc"}

def process_font(src: Path, dst: Path, target_upem: int) -> None:
    ext = src.suffix.lower()
    if ext in {".ttf", ".otf"}:
        font = TTFont(str(src))
        scale_upem(font, target_upem)
        font.save(str(dst))
    elif ext in {".ttc", ".otc"}:
        coll = TTCollection(str(src))
        for f in coll.fonts:
            scale_upem(f, target_upem)
        coll.save(str(dst))
    else:
        # Skip unknown extensions (shouldn't happen due to filter)
        return

def main():
    parser = argparse.ArgumentParser(
        description="Batch scale font UPM for a directory (ttf/otf/ttc/otc)."
    )
    parser.add_argument(
        "target_upm", nargs="?", type=int, default=1000,
        help="Target unitsPerEm (default: 1000)"
    )
    parser.add_argument(
        "--src-dir", default="firaCodeMono",
        help="Source directory to scan (default: firaCodeMono)"
    )
    parser.add_argument(
        "--dst-dir", default="fix_firaCodeMono",
        help="Destination directory for processed fonts (default: fix_firaCodeMono)"
    )
    args = parser.parse_args()

    src_dir = Path(args.src_dir)
    dst_dir = Path(args.dst_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)

    fonts = [p for p in src_dir.iterdir() if p.is_file() and p.suffix.lower() in EXTS]
    for src in sorted(fonts):
        out = dst_dir / src.name
        print(f"Processing: {src.name}  →  {out}  (UPM={args.target_upm})")
        try:
            process_font(src, out, args.target_upm)
        except Exception as e:
            print(f"  ! Failed: {src.name}: {e}")

    print(f"Done. Output in: {dst_dir}")

if __name__ == "__main__":
    main()
