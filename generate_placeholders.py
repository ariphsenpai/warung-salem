#!/usr/bin/env python3
"""
Generate colored placeholder food images with text labels using PIL.
Each image is 512x512 with a food-themed gradient background and menu name.
"""
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    os.system("pip install Pillow -q")
    from PIL import Image, ImageDraw, ImageFont

IMG_DIR = "/root/.openclaw/workspace/warung-salem/assets/img"
os.makedirs(IMG_DIR, exist_ok=True)

# Menu items: (filename, display_name, category_color_rgb)
# Categories: nasi=warm orange, mie=golden, snack=brown, minuman=teal, logo=red
ITEMS = [
    ("nasi-tutug-oncom-ayam.jpg", "Nasi Tutug\nOncom Ayam", (210, 105, 30)),
    ("nasi-kangkung-ayam-sambal-merah.jpg", "Nasi Kangkung\nAyam Sambal Merah", (200, 80, 40)),
    ("nasi-tutug-oncom-telur.jpg", "Nasi Tutug\nOncom Telur", (210, 105, 30)),
    ("nasi-chicken-bbq.jpg", "Nasi\nChicken BBQ", (180, 90, 20)),
    ("nasi-chicken-teriyaki.jpg", "Nasi Chicken\nTeriyaki", (170, 100, 30)),
    ("nasi-ayam-asam-manis.jpg", "Nasi Ayam\nAsam Manis", (200, 120, 40)),
    ("nasi-ayam-penyet-cabe-ijo.jpg", "Nasi Ayam Penyet\nCabe Ijo", (100, 160, 60)),
    ("nasi-ayam-chilli-padi.jpg", "Nasi Ayam\nChilli Padi", (200, 50, 30)),
    ("nasi-ayam-suwir.jpg", "Nasi\nAyam Suwir", (190, 110, 40)),
    ("nasi-nugget-sambal-matah.jpg", "Nasi Nugget\nSambal Matah", (210, 130, 50)),
    ("nasi-goreng.jpg", "Nasi\nGoreng", (180, 100, 30)),
    ("magelangan.jpg", "Magelangan", (170, 110, 40)),
    ("nasi-orak-arik.jpg", "Nasi\nOrak Arik", (200, 150, 50)),
    ("nasi-omelet.jpg", "Nasi\nOmelet", (210, 170, 60)),
    ("mi-nyemek.jpg", "Mi\nNyemek", (190, 130, 30)),
    ("mie-dok-dok.jpg", "Mie\nDok-Dok", (200, 100, 30)),
    ("mie-tek-tek.jpg", "Mie\nTek Tek", (180, 110, 35)),
    ("mie-rebus-telur.jpg", "Mie Rebus\nTelur", (160, 120, 40)),
    ("mie-goreng-telur.jpg", "Mie Goreng\nTelur", (190, 120, 30)),
    ("mie-setan.jpg", "Mie\nSetan", (220, 40, 20)),
    ("roti-bakar-sandwich.jpg", "Roti Bakar\nSandwich", (160, 120, 60)),
    ("lumpia-beef.jpg", "Lumpia\nBeef", (180, 130, 50)),
    ("roti-bakar-choco-crunchy.jpg", "Roti Bakar\nChoco Crunchy", (120, 70, 30)),
    ("roti-bakar-tiramisu-crunchy.jpg", "Roti Bakar\nTiramisu Crunchy", (140, 100, 60)),
    ("roti-bakar-greentea-crunchy.jpg", "Roti Bakar\nGreentea Crunchy", (80, 140, 70)),
    ("roti-bakar-strawberry.jpg", "Roti Bakar\nStrawberry", (200, 60, 80)),
    ("roti-bakar-blueberry.jpg", "Roti Bakar\nBlueberry", (70, 70, 160)),
    ("es-teh.jpg", "Es Teh", (160, 100, 40)),
    ("es-nutrisari.jpg", "Es Nutrisari", (230, 150, 30)),
    ("es-bengbeng.jpg", "Es BengBeng", (100, 60, 30)),
    ("es-goodday.jpg", "Es Goodday", (120, 80, 40)),
    ("warung-salem-logo.jpg", "Warung\nSalem", (200, 30, 30)),
]

# Food emoji/icon unicode for visual appeal
FOOD_ICONS = {
    "nasi": "🍚",
    "ayam": "🍗",
    "mie": "🍜",
    "mi": "🍜",
    "roti": "🍞",
    "es": "🧊",
    "lumpia": "🥟",
    "magelangan": "🍛",
    "warung": "🔥",
}

def get_icon(name):
    name_lower = name.lower()
    for key, icon in FOOD_ICONS.items():
        if key in name_lower:
            return icon
    return "🍽️"

def create_food_image(filename, label, base_color):
    """Create an attractive food placeholder image."""
    W, H = 512, 512
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    r, g, b = base_color
    for y in range(H):
        ratio = y / H
        # Darker at top, lighter at bottom with warm tones
        cr = int(r * 0.6 + r * 0.4 * ratio)
        cg = int(g * 0.5 + g * 0.5 * ratio)
        cb = int(b * 0.4 + b * 0.6 * ratio)
        cr = min(255, cr)
        cg = min(255, cg)
        cb = min(255, cb)
        draw.line([(0, y), (W, y)], fill=(cr, cg, cb))
    
    # Add a subtle circular plate in center
    plate_r = 180
    cx, cy = W // 2, H // 2 - 10
    # Plate shadow
    draw.ellipse([cx - plate_r - 5, cy - plate_r + 20, cx + plate_r + 5, cy + plate_r + 30],
                 fill=(max(0, r - 60), max(0, g - 60), max(0, b - 60)))
    # Plate
    draw.ellipse([cx - plate_r, cy - plate_r, cx + plate_r, cy + plate_r],
                 fill=(245, 242, 235))
    # Plate inner ring
    draw.ellipse([cx - plate_r + 15, cy - plate_r + 15, cx + plate_r - 15, cy + plate_r - 15],
                 fill=(250, 248, 243))
    # Plate center (food area) - slightly tinted
    food_r = plate_r - 40
    draw.ellipse([cx - food_r, cy - food_r, cx + food_r, cy + food_r],
                 fill=(min(255, r + 40), min(255, g + 60), min(255, b + 40)))
    
    # Add some visual texture dots to simulate food
    import random
    random.seed(hash(filename))
    for _ in range(60):
        fx = cx + random.randint(-food_r + 20, food_r - 20)
        fy = cy + random.randint(-food_r + 20, food_r - 20)
        # Check if inside circle
        if (fx - cx)**2 + (fy - cy)**2 < (food_r - 20)**2:
            dot_r = random.randint(3, 12)
            shade = random.randint(-30, 30)
            dot_color = (
                max(0, min(255, r + 40 + shade)),
                max(0, min(255, g + 60 + shade + random.randint(-10, 10))),
                max(0, min(255, b + 40 + shade))
            )
            draw.ellipse([fx - dot_r, fy - dot_r, fx + dot_r, fy + dot_r], fill=dot_color)
    
    # Add text label at bottom
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_small = font_large
    
    # Semi-transparent bar at bottom for text
    bar_h = 90
    for y in range(H - bar_h, H):
        alpha = (y - (H - bar_h)) / bar_h * 0.85
        for x in range(W):
            orig = img.getpixel((x, y))
            blended = tuple(int(orig[i] * (1 - alpha) + 0 * alpha) for i in range(3))
            img.putpixel((x, y), blended)
    
    # Draw text
    lines = label.split("\n")
    y_start = H - bar_h + 15
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_large)
        tw = bbox[2] - bbox[0]
        tx = (W - tw) // 2
        ty = y_start + i * 35
        # Shadow
        draw.text((tx + 1, ty + 1), line, fill=(0, 0, 0), font=font_large)
        draw.text((tx, ty), line, fill=(255, 255, 255), font=font_large)
    
    # "Warung Salem" watermark at top
    wm = "Warung Salem"
    bbox = draw.textbbox((0, 0), wm, font=font_small)
    wmw = bbox[2] - bbox[0]
    draw.text(((W - wmw) // 2, 12), wm, fill=(255, 255, 255, 180), font=font_small)
    
    # Save
    filepath = os.path.join(IMG_DIR, filename)
    img.save(filepath, "JPEG", quality=85)
    return filepath

print("Generating 32 food placeholder images...")
for i, (fn, label, color) in enumerate(ITEMS, 1):
    path = create_food_image(fn, label, color)
    print(f"  [{i:2d}/32] ✅ {fn}")

print(f"\nAll 32 images saved to {IMG_DIR}")
