"""
Smart Tile Merger for Pathworlds
----------------------------------
Merges new tiles from a source folder into your main tiles folder.
Only copies tiles that are NEW or UPDATED — never deletes existing tiles.

Usage:
1. Export QTiles to a TEMPORARY folder (e.g. tiles-new)
2. Run this script to merge tiles-new into your main tiles folder
3. Only the new/changed tiles are copied — everything else untouched

python merge_tiles.py
"""

import os
import shutil

# ── SETTINGS ──────────────────────────────────────────────────────────────────
# Folder QTiles just exported to (temporary)
SOURCE_FOLDER = r"C:\Users\Joey's PC\Desktop\my-world\tiles-new\QGIS Map of World 1"

# Your main tiles folder that the website uses
TARGET_FOLDER = r"C:\Users\Joey's PC\Desktop\my-world\tiles\QGIS Map of World 1"

# ── MERGE ─────────────────────────────────────────────────────────────────────
def merge_tiles():
    if not os.path.exists(SOURCE_FOLDER):
        print(f"ERROR: Source folder not found: {SOURCE_FOLDER}")
        print("Make sure you exported QTiles to the tiles-new folder first.")
        input("Press Enter to exit...")
        return

    if not os.path.exists(TARGET_FOLDER):
        print(f"Target folder doesn't exist yet — creating it...")
        os.makedirs(TARGET_FOLDER)

    copied = 0
    skipped = 0
    updated = 0

    print(f"Merging tiles from:\n  {SOURCE_FOLDER}\ninto:\n  {TARGET_FOLDER}\n")

    for zoom in os.listdir(SOURCE_FOLDER):
        zoom_src = os.path.join(SOURCE_FOLDER, zoom)
        zoom_dst = os.path.join(TARGET_FOLDER, zoom)
        if not os.path.isdir(zoom_src):
            continue

        for x in os.listdir(zoom_src):
            x_src = os.path.join(zoom_src, x)
            x_dst = os.path.join(zoom_dst, x)
            if not os.path.isdir(x_src):
                continue
            os.makedirs(x_dst, exist_ok=True)

            for tile in os.listdir(x_src):
                src_tile = os.path.join(x_src, tile)
                dst_tile = os.path.join(x_dst, tile)

                if not os.path.exists(dst_tile):
                    shutil.copy2(src_tile, dst_tile)
                    copied += 1
                else:
                    # Replace if source is newer
                    src_time = os.path.getmtime(src_tile)
                    dst_time = os.path.getmtime(dst_tile)
                    if src_time > dst_time:
                        shutil.copy2(src_tile, dst_tile)
                        updated += 1
                    else:
                        skipped += 1

        print(f"  Zoom {zoom} done")

    print(f"\n✓ Merge complete!")
    print(f"  {copied} new tiles added")
    print(f"  {updated} existing tiles updated")
    print(f"  {skipped} tiles unchanged")
    print(f"\nYou can now delete the tiles-new folder if you want.")
    input("\nPress Enter to exit...")

merge_tiles()
