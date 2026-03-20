"""
Fantasy Map Tile Cutter
-----------------------
Cuts a plain PNG image into 256x256 tiles for use with Leaflet.js
No geographic coordinates needed!

Usage: python make_tiles.py
"""

import os
import math

# ── INSTALL Pillow if needed ──────────────────────────────────────────────────
try:
    from PIL import Image
except ImportError:
    print("Installing required library (Pillow)...")
    os.system("pip install Pillow")
    from PIL import Image

# ── SETTINGS ─────────────────────────────────────────────────────────────────
INPUT_IMAGE = "map.png"       # Your map file (must be in the same folder)
OUTPUT_DIR  = "tiles"         # Output folder name
MIN_ZOOM    = 5               # Minimum zoom level
MAX_ZOOM    = 8              # Maximum zoom level
TILE_SIZE   = 256             # Standard tile size in pixels

# ── TILE CUTTER ───────────────────────────────────────────────────────────────
def cut_tiles():
    if not os.path.exists(INPUT_IMAGE):
        print(f"ERROR: Could not find '{INPUT_IMAGE}'")
        print(f"Make sure your map image is named '{INPUT_IMAGE}' and is in the same folder as this script.")
        input("Press Enter to exit...")
        return

    print(f"Opening {INPUT_IMAGE}...")
    Image.MAX_IMAGE_PIXELS = None  # Allow very large images
    img = Image.open(INPUT_IMAGE).convert("RGBA")
    orig_w, orig_h = img.size
    print(f"Image size: {orig_w} x {orig_h} pixels")

    # If image is very large, resize it down to a manageable size first
    # 16384px is plenty of detail for zoom level 10
    MAX_DIMENSION = 16384
    if orig_w > MAX_DIMENSION or orig_h > MAX_DIMENSION:
        scale = MAX_DIMENSION / max(orig_w, orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        print(f"Image is very large — resizing to {new_w}x{new_h}px to fit in memory...")
        img = img.resize((new_w, new_h), Image.LANCZOS)
        print(f"Resize complete. Now cutting tiles...")

    for zoom in range(MIN_ZOOM, MAX_ZOOM + 1):
        # Number of tiles across and down at this zoom level
        num_tiles = 2 ** zoom
        target_size = num_tiles * TILE_SIZE

        print(f"\nZoom level {zoom} — resizing to {target_size}x{target_size}px ({num_tiles}x{num_tiles} tiles)...")
        resized = img.resize((target_size, target_size), Image.LANCZOS)

        tiles_made = 0
        for x in range(num_tiles):
            for y in range(num_tiles):
                # Crop this tile out of the resized image
                left   = x * TILE_SIZE
                upper  = y * TILE_SIZE
                right  = left  + TILE_SIZE
                lower  = upper + TILE_SIZE
                tile   = resized.crop((left, upper, right, lower))

                # Save to tiles/zoom/x/y.png
                tile_dir = os.path.join(OUTPUT_DIR, str(zoom), str(x))
                os.makedirs(tile_dir, exist_ok=True)
                tile_path = os.path.join(tile_dir, f"{y}.png")
                tile.save(tile_path, "PNG", optimize=True)
                tiles_made += 1

        print(f"  ✓ {tiles_made} tiles created for zoom {zoom}")

    print(f"\n✓ All done! Tiles saved to '{OUTPUT_DIR}' folder.")
    print("You can now open fantasy-map.html in your browser.")
    input("\nPress Enter to exit...")

cut_tiles()
