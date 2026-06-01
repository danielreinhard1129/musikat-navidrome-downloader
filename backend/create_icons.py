"""One-time script to generate PWA/favicon PNG icons into backend/static/."""
import math
import os
from PIL import Image, ImageDraw

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

BG = "#121212"
GREEN = "#1db954"
WHITE = "#ffffff"


def draw_music_note(draw: ImageDraw.ImageDraw, cx: float, cy: float, size: float) -> None:
    """Draw a simple eighth-note (♪) centered at (cx, cy) scaled to `size`."""
    # Notehead: filled ellipse, slightly tilted
    nh_w = size * 0.38
    nh_h = size * 0.27
    nh_x = cx - size * 0.05
    nh_y = cy + size * 0.28
    draw.ellipse(
        [nh_x - nh_w / 2, nh_y - nh_h / 2, nh_x + nh_w / 2, nh_y + nh_h / 2],
        fill=WHITE,
    )

    # Stem: vertical line from top-right of notehead upward
    stem_x = nh_x + nh_w / 2 - size * 0.03
    stem_top = cy - size * 0.32
    stem_bot = nh_y - nh_h * 0.15
    stem_w = max(2, size * 0.055)
    draw.rectangle([stem_x, stem_top, stem_x + stem_w, stem_bot], fill=WHITE)

    # Flag: curved tail at top of stem (approximated with a filled polygon)
    flag_pts = [
        (stem_x + stem_w, stem_top),
        (stem_x + stem_w + size * 0.30, stem_top + size * 0.12),
        (stem_x + stem_w + size * 0.18, stem_top + size * 0.32),
        (stem_x + stem_w, stem_top + size * 0.28),
    ]
    draw.polygon(flag_pts, fill=WHITE)


def make_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded-rectangle background
    radius = size // 5
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=BG)

    # Green circle
    pad = size * 0.10
    draw.ellipse([pad, pad, size - pad, size - pad], fill=GREEN)

    # Music note centered on the green circle
    draw_music_note(draw, size / 2, size / 2, size * 0.55)

    return img


SIZES = {
    "favicon-32.png": 32,
    "apple-touch-icon.png": 180,
    "icon-192.png": 192,
    "icon-512.png": 512,
}

for filename, px in SIZES.items():
    path = os.path.join(STATIC_DIR, filename)
    icon = make_icon(px)
    icon.save(path, "PNG")
    print(f"  created {filename} ({px}×{px})")

print("Done.")
