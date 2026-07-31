"""
Sprite generator for the Hydration Buddy app.
Creates a beautiful anime-style girl character with smooth anti-aliased art.
She walks in, drinks water from a bottle, and walks back out.

Replace with your own Gemini-generated pixel art anytime!
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# ── Canvas Settings ──
CHAR_W = 160
CHAR_H = 280
FRAMES = 8
BG = (0, 0, 0, 0)

# ── Color Palette ──
# Skin
SKIN = (252, 218, 190)
SKIN_LIGHT = (255, 230, 210)
SKIN_SHADOW = (230, 185, 155)
SKIN_BLUSH = (255, 190, 180)

# Hair (dark brown with warm highlights)
HAIR_DARK = (40, 25, 18)
HAIR_MID = (65, 40, 28)
HAIR_LIGHT = (95, 60, 40)
HAIR_SHINE = (140, 95, 65)

# Eyes
EYE_WHITE = (255, 255, 255)
EYE_BROWN = (90, 55, 30)
EYE_DARK = (25, 18, 12)
EYE_HIGHLIGHT = (255, 255, 255)
EYELASH = (25, 18, 12)

# Face details
EYEBROW = (50, 30, 20)
LIP_COLOR = (220, 130, 130)
LIP_SHADOW = (190, 100, 100)
BLUSH = (255, 195, 185)

# Glasses
GLASS_FRAME = (40, 40, 50)

# Outfit - casual cute (pink top + dark jeans)
TOP_COLOR = (255, 180, 200)      # Soft pink
TOP_SHADOW = (230, 150, 170)
TOP_LIGHT = (255, 210, 220)
CARDIGAN = (60, 65, 80)          # Dark grey-blue
CARDIGAN_LIGHT = (85, 90, 105)

JEANS = (55, 70, 110)
JEANS_SHADOW = (40, 52, 85)
JEANS_LIGHT = (70, 88, 130)

SNEAKERS = (255, 255, 255)
SNEAKERS_ACCENT = (255, 120, 150)
SNEAKERS_SOLE = (220, 220, 220)

# Water bottle
BOTTLE = (80, 200, 180)
BOTTLE_LIGHT = (140, 230, 210)
BOTTLE_DARK = (50, 160, 140)
BOTTLE_CAP = (55, 55, 60)
WATER = (120, 200, 240)
WATER_LIGHT = (180, 230, 255)

# Accessories
SCRUNCHIE = (255, 150, 180)


def draw_ellipse(draw, cx, cy, rx, ry, color):
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color)


def draw_rounded_rect(draw, x1, y1, x2, y2, r, color):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=color)


# ══════════════════════════════════════════════════════════════════════════════
# CHARACTER DRAWING FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def draw_hair_back(draw, sway=0):
    """Long flowing hair behind the body."""
    # Main hair body
    hair_pts = [
        (45, 50), (38, 70), (32, 100), (28, 140), (30, 180),
        (35, 210), (42, 230), (55, 240),
        (105, 240), (118, 230), (125, 210), (130, 180),
        (132, 140), (128, 100), (122, 70), (115, 50),
    ]
    shifted = [(x + sway, y) for x, y in hair_pts]
    draw.polygon(shifted, fill=HAIR_DARK)

    # Shine streaks
    draw.line([(50 + sway, 70), (45 + sway, 200)], fill=HAIR_LIGHT, width=4)
    draw.line([(55 + sway, 75), (52 + sway, 180)], fill=HAIR_SHINE, width=2)
    draw.line([(110 + sway, 70), (115 + sway, 200)], fill=HAIR_LIGHT, width=4)
    draw.line([(105 + sway, 80), (108 + sway, 160)], fill=HAIR_SHINE, width=2)

    # Hair tips (wavy ends)
    for i in range(4):
        x = 45 + i * 18 + sway
        draw_ellipse(draw, x, 238, 8, 5, HAIR_DARK)


def draw_face(draw):
    """Draw the face with detailed features."""
    # Face shape (oval)
    draw_ellipse(draw, 80, 68, 30, 35, SKIN)
    # Slight jaw shape
    draw.polygon([(52, 70), (80, 102), (108, 70)], fill=SKIN)
    draw_ellipse(draw, 80, 72, 28, 32, SKIN)

    # Forehead highlight
    draw_ellipse(draw, 80, 55, 18, 10, SKIN_LIGHT)

    # ── Eyes ──
    # Left eye
    draw_ellipse(draw, 67, 68, 9, 7, EYE_WHITE)
    draw_ellipse(draw, 68, 69, 6, 5, EYE_BROWN)
    draw_ellipse(draw, 68, 70, 3, 3, EYE_DARK)
    draw_ellipse(draw, 66, 66, 2, 2, EYE_HIGHLIGHT)  # Shine
    # Upper eyelid/lash
    draw.arc([58, 60, 77, 76], start=200, end=340, fill=EYELASH, width=3)

    # Right eye
    draw_ellipse(draw, 93, 68, 9, 7, EYE_WHITE)
    draw_ellipse(draw, 92, 69, 6, 5, EYE_BROWN)
    draw_ellipse(draw, 92, 70, 3, 3, EYE_DARK)
    draw_ellipse(draw, 90, 66, 2, 2, EYE_HIGHLIGHT)
    draw.arc([83, 60, 102, 76], start=200, end=340, fill=EYELASH, width=3)

    # Eyebrows
    draw.arc([59, 54, 76, 66], start=200, end=330, fill=EYEBROW, width=3)
    draw.arc([84, 54, 101, 66], start=210, end=340, fill=EYEBROW, width=3)

    # ── Glasses ──
    draw.rounded_rectangle([55, 61, 78, 78], radius=4, outline=GLASS_FRAME, width=2)
    draw.rounded_rectangle([82, 61, 105, 78], radius=4, outline=GLASS_FRAME, width=2)
    draw.line([(78, 69), (82, 69)], fill=GLASS_FRAME, width=2)  # Bridge
    draw.line([(55, 69), (48, 66)], fill=GLASS_FRAME, width=2)  # Left arm
    draw.line([(105, 69), (112, 66)], fill=GLASS_FRAME, width=2)  # Right arm

    # Nose (subtle)
    draw.arc([76, 72, 84, 82], start=30, end=150, fill=SKIN_SHADOW, width=2)

    # Mouth / Lips
    draw_ellipse(draw, 80, 88, 6, 3, LIP_COLOR)
    draw.line([(75, 88), (85, 88)], fill=LIP_SHADOW, width=1)
    # Smile curve
    draw.arc([74, 85, 86, 92], start=10, end=170, fill=LIP_SHADOW, width=2)

    # Blush spots
    draw_ellipse(draw, 58, 80, 6, 3, BLUSH)
    draw_ellipse(draw, 102, 80, 6, 3, BLUSH)

    # Ears (partially visible)
    draw_ellipse(draw, 49, 70, 4, 6, SKIN_SHADOW)
    draw_ellipse(draw, 111, 70, 4, 6, SKIN_SHADOW)


def draw_hair_front(draw):
    """Bangs and front hair framing the face."""
    # Top volume
    draw_ellipse(draw, 80, 35, 35, 18, HAIR_DARK)

    # Bangs (side-swept)
    bang_pts = [(42, 38), (50, 32), (70, 28), (90, 28), (110, 32),
               (118, 38), (115, 55), (100, 60), (80, 62), (60, 60), (45, 55)]
    draw.polygon(bang_pts, fill=HAIR_DARK)

    # Side hair framing face
    draw.polygon([(42, 45), (38, 80), (44, 95), (52, 72), (48, 45)], fill=HAIR_DARK)
    draw.polygon([(118, 45), (122, 80), (116, 95), (108, 72), (112, 45)], fill=HAIR_DARK)

    # Hair shine on bangs
    draw.line([(65, 32), (62, 48)], fill=HAIR_SHINE, width=3)
    draw.line([(75, 30), (73, 42)], fill=HAIR_LIGHT, width=2)

    # Scrunchie / hair accessory on the side
    draw_ellipse(draw, 115, 50, 5, 5, SCRUNCHIE)


def draw_neck(draw):
    """Draw neck."""
    draw_rounded_rect(draw, 70, 98, 90, 118, 4, SKIN)
    draw.line([(78, 102), (78, 112)], fill=SKIN_SHADOW, width=1)


def draw_body_normal(draw):
    """Body with pink top and dark cardigan, arms at sides."""
    # Cardigan back
    draw_rounded_rect(draw, 38, 115, 122, 185, 8, CARDIGAN)

    # Pink top (visible in center)
    draw_rounded_rect(draw, 55, 115, 105, 175, 5, TOP_COLOR)
    draw_rounded_rect(draw, 60, 120, 100, 140, 3, TOP_LIGHT)  # Collar area

    # Cardigan lapels
    draw.polygon([(55, 115), (65, 115), (60, 165), (50, 165)], fill=CARDIGAN)
    draw.polygon([(95, 115), (105, 115), (110, 165), (100, 165)], fill=CARDIGAN)

    # Cardigan arms (sleeves)
    # Left arm
    draw_rounded_rect(draw, 30, 118, 50, 180, 6, CARDIGAN)
    draw.line([(35, 125), (33, 170)], fill=CARDIGAN_LIGHT, width=3)
    # Hand
    draw_ellipse(draw, 40, 185, 7, 6, SKIN)

    # Right arm
    draw_rounded_rect(draw, 110, 118, 130, 180, 6, CARDIGAN)
    draw.line([(125, 125), (127, 170)], fill=CARDIGAN_LIGHT, width=3)
    # Hand
    draw_ellipse(draw, 120, 185, 7, 6, SKIN)

    # Top folds/details
    draw.line([(70, 135), (68, 165)], fill=TOP_SHADOW, width=2)
    draw.line([(90, 135), (92, 165)], fill=TOP_SHADOW, width=2)


def draw_body_drinking(draw):
    """Body with right arm raised, drinking from bottle."""
    # Cardigan back
    draw_rounded_rect(draw, 38, 115, 122, 185, 8, CARDIGAN)

    # Pink top
    draw_rounded_rect(draw, 55, 115, 105, 175, 5, TOP_COLOR)
    draw_rounded_rect(draw, 60, 120, 100, 140, 3, TOP_LIGHT)

    # Cardigan lapels
    draw.polygon([(55, 115), (65, 115), (60, 165), (50, 165)], fill=CARDIGAN)
    draw.polygon([(95, 115), (105, 115), (110, 165), (100, 165)], fill=CARDIGAN)

    # Left arm (relaxed)
    draw_rounded_rect(draw, 30, 118, 50, 180, 6, CARDIGAN)
    draw.line([(35, 125), (33, 170)], fill=CARDIGAN_LIGHT, width=3)
    draw_ellipse(draw, 40, 185, 7, 6, SKIN)

    # Right arm RAISED (holding bottle to mouth)
    # Upper arm going up
    draw.polygon([(110, 118), (130, 118), (135, 95), (125, 70), (115, 75), (108, 100)],
                 fill=CARDIGAN)
    draw.line([(120, 115), (128, 82)], fill=CARDIGAN_LIGHT, width=2)
    # Hand near mouth
    draw_ellipse(draw, 125, 65, 7, 6, SKIN)

    # ── WATER BOTTLE (near mouth — clearly drinking!) ──
    # Bottle tilted toward mouth
    draw_rounded_rect(draw, 118, 35, 135, 65, 5, BOTTLE)
    draw_rounded_rect(draw, 120, 40, 133, 60, 4, BOTTLE_LIGHT)
    # Water inside
    draw_rounded_rect(draw, 121, 45, 132, 58, 3, WATER)
    draw_rounded_rect(draw, 122, 48, 131, 55, 2, WATER_LIGHT)
    # Bottle cap (near mouth)
    draw_rounded_rect(draw, 122, 30, 131, 37, 3, BOTTLE_CAP)
    # Water droplets (drinking effect)
    draw_ellipse(draw, 126, 28, 2, 2, WATER_LIGHT)
    draw_ellipse(draw, 123, 25, 1, 1, WATER)

    # Top folds
    draw.line([(70, 135), (68, 165)], fill=TOP_SHADOW, width=2)


def draw_body_holding_bottle(draw):
    """Body with bottle held at side (idle with bottle)."""
    draw_body_normal(draw)
    # Add bottle in right hand
    draw_rounded_rect(draw, 113, 170, 130, 205, 5, BOTTLE)
    draw_rounded_rect(draw, 115, 175, 128, 200, 4, BOTTLE_LIGHT)
    draw_rounded_rect(draw, 116, 180, 127, 198, 3, WATER)
    draw_rounded_rect(draw, 118, 167, 125, 172, 3, BOTTLE_CAP)


def draw_legs(draw, phase=0):
    """Draw legs with walking animation."""
    # Jeans
    offsets = [
        (0, 0), (-5, 3), (-9, 5), (-5, 3),
        (0, 0), (5, 3), (9, 5), (5, 3),
    ]
    lx, ly = offsets[phase % len(offsets)]
    rx, ry = (-lx, ly)

    # Left leg
    draw_rounded_rect(draw, 58 + lx, 178 + ly, 76 + lx, 248, 6, JEANS)
    draw.line([(65 + lx, 185 + ly), (65 + lx, 240)], fill=JEANS_LIGHT, width=2)
    draw.line([(72 + lx, 185 + ly), (72 + lx, 240)], fill=JEANS_SHADOW, width=2)

    # Right leg
    draw_rounded_rect(draw, 84 + rx, 178 + ry, 102 + rx, 248, 6, JEANS)
    draw.line([(90 + rx, 185 + ry), (90 + rx, 240)], fill=JEANS_LIGHT, width=2)
    draw.line([(98 + rx, 185 + ry), (98 + rx, 240)], fill=JEANS_SHADOW, width=2)

    # Sneakers
    # Left sneaker
    draw_rounded_rect(draw, 55 + lx, 245, 80 + lx, 262, 5, SNEAKERS)
    draw_rounded_rect(draw, 55 + lx, 258, 82 + lx, 265, 4, SNEAKERS_SOLE)
    draw.line([(60 + lx, 252), (75 + lx, 252)], fill=SNEAKERS_ACCENT, width=2)

    # Right sneaker
    draw_rounded_rect(draw, 80 + rx, 245, 105 + rx, 262, 5, SNEAKERS)
    draw_rounded_rect(draw, 78 + rx, 258, 105 + rx, 265, 4, SNEAKERS_SOLE)
    draw.line([(85 + rx, 252), (100 + rx, 252)], fill=SNEAKERS_ACCENT, width=2)


def compose_walking_frame(phase=0, flip=False):
    """Full character walking (no bottle)."""
    img = Image.new("RGBA", (CHAR_W, CHAR_H), BG)
    draw = ImageDraw.Draw(img)

    sway = int(math.sin(phase * 0.8) * 2)

    draw_hair_back(draw, sway)
    draw_legs(draw, phase)
    draw_neck(draw)
    draw_body_normal(draw)
    draw_face(draw)
    draw_hair_front(draw)

    if flip:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img


def compose_drinking_frame(arm_up=True):
    """Character drinking water (standing still)."""
    img = Image.new("RGBA", (CHAR_W, CHAR_H), BG)
    draw = ImageDraw.Draw(img)

    draw_hair_back(draw, 0)
    draw_legs(draw, 0)
    draw_neck(draw)

    if arm_up:
        draw_body_drinking(draw)
    else:
        draw_body_holding_bottle(draw)

    draw_face(draw)
    draw_hair_front(draw)

    return img


def compose_idle_frame():
    """Standing idle."""
    img = Image.new("RGBA", (CHAR_W, CHAR_H), BG)
    draw = ImageDraw.Draw(img)

    draw_hair_back(draw, 0)
    draw_legs(draw, 0)
    draw_neck(draw)
    draw_body_normal(draw)
    draw_face(draw)
    draw_hair_front(draw)

    return img


# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def generate_walk_in():
    """Walking in from right (facing left)."""
    frames = [compose_walking_frame(phase=i, flip=True) for i in range(FRAMES)]
    frames[0].save(
        "assets/walk_in.gif",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        transparency=0,
        disposal=2,
    )
    print("Created assets/walk_in.gif")


def generate_drinking():
    """Drinking water animation — arm goes up, drinks, lowers, repeats."""
    frames = []
    # Holding bottle low
    frames.append(compose_drinking_frame(arm_up=False))
    # Raising to drink
    frames.append(compose_drinking_frame(arm_up=True))
    frames.append(compose_drinking_frame(arm_up=True))
    frames.append(compose_drinking_frame(arm_up=True))
    # Lowering
    frames.append(compose_drinking_frame(arm_up=False))
    frames.append(compose_drinking_frame(arm_up=False))
    # Raising again
    frames.append(compose_drinking_frame(arm_up=True))
    frames.append(compose_drinking_frame(arm_up=True))

    frames[0].save(
        "assets/drinking.gif",
        save_all=True,
        append_images=frames[1:],
        duration=250,
        loop=0,
        transparency=0,
        disposal=2,
    )
    print("Created assets/drinking.gif")


def generate_walk_out():
    """Walking out to right (facing right)."""
    frames = [compose_walking_frame(phase=i, flip=False) for i in range(FRAMES)]
    frames[0].save(
        "assets/walk_out.gif",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        transparency=0,
        disposal=2,
    )
    print("Created assets/walk_out.gif")


def generate_idle():
    """Standing idle frame."""
    img = compose_idle_frame()
    img.save("assets/idle.png")
    print("Created assets/idle.png")


if __name__ == "__main__":
    generate_walk_in()
    generate_drinking()
    generate_walk_out()
    generate_idle()
    print("\nDone! Your character sprites are in assets/")
    print("To use your own Gemini art, just replace the files in assets/")
