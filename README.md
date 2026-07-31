# Hydration Buddy 💧

A cute desktop companion that reminds you to drink water every 45 minutes with an animated character.

## How it works

1. A notification popup **slides up** from the bottom-right corner
2. An animated girl character **walks onto the screen** with a speech bubble: *"Time to drink water!"*
3. Two buttons appear:
   - **Yes I drank water** → logs a glass, resets the 45-minute timer
   - **Snooze** → reminder comes back in 10 minutes
4. The character walks off screen, the popup slides down, and the countdown begins again

## Quick Start

```bash
pip install -r requirements.txt
python hydration_buddy.py
```

The app auto-generates character sprites on first run.

## Custom Sprites

To use your own character art, replace the files in `assets/`:
- `assets/walk_in.gif` — walking in animation
- `assets/drinking.gif` — drinking water animation
- `assets/walk_out.gif` — walking out animation
- `assets/idle.png` — standing still frame

Re-run the app — it picks up custom sprites automatically.

## Project Structure

```
AI_Hydration_buddy/
├── hydration_buddy.py     # Main app (Tkinter + Pillow)
├── generate_sprites.py    # Character sprite generator
├── requirements.txt
├── README.md
└── assets/                # Sprite sheets
    ├── walk_in.gif
    ├── drinking.gif
    ├── walk_out.gif
    └── idle.png
```

## Requirements

- Python 3.8+
- Pillow (for image/GIF handling)
- Tkinter (included with Python on Windows)
