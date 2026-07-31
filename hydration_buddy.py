"""
Hydration Buddy - Desktop Water Reminder App
=============================================
A beautiful notification popup that slides up from the bottom-right corner,
featuring an animated character that walks in, reminds you to drink water,
and walks back out.

Usage:
    python hydration_buddy.py

The app runs silently and pops up every 2 minutes from the bottom-right.
"""

import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

# ── Configuration ────────────────────────────────────────────────────────────
REMINDER_INTERVAL_MS = 45 * 60 * 1000   # 45 minutes
SNOOZE_INTERVAL_MS = 10 * 60 * 1000     # 10 minutes
WALK_SPEED = 6                           # Pixels per animation tick
ANIM_TICK_MS = 30                        # ms between animation ticks
SPRITE_FRAME_MS = 200                    # ms between sprite frames
SLIDE_SPEED = 14                         # Pixels per slide-up tick

POPUP_WIDTH = 420
POPUP_HEIGHT = 500
SPEECH_TEXT = "💧 Time to drink water!"

# Support both normal run and PyInstaller bundled .exe
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


# ── Color Theme ──────────────────────────────────────────────────────────────
BG_DARK = "#1a1b2e"
BG_CARD = "#252742"
BG_CANVAS = "#f8f9fc"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#a0a8c0"
ACCENT_GREEN = "#2dd4a8"
ACCENT_ORANGE = "#ff8c42"
ACCENT_BLUE = "#64b5f6"
BORDER_GLOW = "#3d5afe"


# ── Sprite Loader ────────────────────────────────────────────────────────────
class SpriteSheet:
    """Loads an animated GIF or static PNG and provides frames."""

    def __init__(self, path, scale=1):
        self.frames = []
        self._index = 0
        if not os.path.exists(path):
            return
        img = Image.open(path)
        try:
            while True:
                frame = img.copy().convert("RGBA")
                if scale != 1:
                    new_w = int(frame.width * scale)
                    new_h = int(frame.height * scale)
                    frame = frame.resize((new_w, new_h), Image.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(frame))
                img.seek(img.tell() + 1)
        except EOFError:
            pass
        if not self.frames:
            frame = img.convert("RGBA")
            if scale != 1:
                new_w = int(frame.width * scale)
                new_h = int(frame.height * scale)
                frame = frame.resize((new_w, new_h), Image.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(frame))

    @property
    def valid(self):
        return len(self.frames) > 0

    def next_frame(self):
        if not self.frames:
            return None
        frame = self.frames[self._index % len(self.frames)]
        self._index += 1
        return frame

    def reset(self):
        self._index = 0

    @property
    def width(self):
        return self.frames[0].width() if self.frames else 0

    @property
    def height(self):
        return self.frames[0].height() if self.frames else 0


# ── Main Application ─────────────────────────────────────────────────────────
class HydrationBuddy:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hydration Buddy")
        self.root.overrideredirect(True)  # No title bar — clean popup
        self.root.attributes("-topmost", True)
        self.root.configure(bg=BG_DARK)

        # Position: bottom-right (initially below screen)
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.popup_x = self.screen_w - POPUP_WIDTH - 20
        self.popup_y_hidden = self.screen_h + 10
        self.popup_y_shown = self.screen_h - POPUP_HEIGHT - 60  # Above taskbar

        self.root.geometry(
            f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{self.popup_x}+{self.popup_y_hidden}"
        )

        # ── Load sprites ──
        self.walk_in_sprite = SpriteSheet(os.path.join(ASSETS_DIR, "walk_in.gif"))
        self.drinking_sprite = SpriteSheet(os.path.join(ASSETS_DIR, "drinking.gif"))
        self.walk_out_sprite = SpriteSheet(os.path.join(ASSETS_DIR, "walk_out.gif"))
        self.idle_sprite = SpriteSheet(os.path.join(ASSETS_DIR, "idle.png"))
        self.has_sprites = self.walk_in_sprite.valid

        # ── Build UI ──
        self._build_ui()

        # ── State ──
        self.char_x = POPUP_WIDTH + 50  # Start off-screen right
        self.target_x = 140              # Walk to center-left
        self.state = "hidden"
        self.current_y = self.popup_y_hidden
        self._anim_id = None
        self._sprite_id = None
        self._reminder_id = None
        self._slide_id = None
        self.water_count = 0

        # Start timer
        self._schedule_reminder(REMINDER_INTERVAL_MS)

    def _build_ui(self):
        # ── Glowing border ──
        self.border_frame = tk.Frame(self.root, bg=BORDER_GLOW, padx=2, pady=2)
        self.border_frame.pack(fill="both", expand=True)

        self.main_frame = tk.Frame(self.border_frame, bg=BG_DARK)
        self.main_frame.pack(fill="both", expand=True)

        # ── Header ──
        header = tk.Frame(self.main_frame, bg=BG_DARK)
        header.pack(fill="x", padx=15, pady=(12, 0))

        tk.Label(
            header, text="💧 Hydration Buddy",
            bg=BG_DARK, fg=TEXT_PRIMARY,
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left")

        self.counter_label = tk.Label(
            header, text="🥤 0",
            bg=BG_DARK, fg=ACCENT_BLUE,
            font=("Segoe UI", 11, "bold"),
        )
        self.counter_label.pack(side="right")

        # Close button
        close_btn = tk.Label(
            header, text="✕", bg=BG_DARK, fg=TEXT_SECONDARY,
            font=("Segoe UI", 12), cursor="hand2",
        )
        close_btn.pack(side="right", padx=(0, 12))
        close_btn.bind("<Button-1>", lambda e: self._on_snooze())

        # ── Speech bubble ──
        self.speech_frame = tk.Frame(self.main_frame, bg=BG_CARD, padx=10, pady=6)
        self.speech_frame.pack(fill="x", padx=15, pady=(10, 5))

        self.speech_label = tk.Label(
            self.speech_frame, text="",
            bg=BG_CARD, fg=TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
            pady=4,
        )
        self.speech_label.pack()

        # ── Canvas for character ──
        canvas_w = POPUP_WIDTH - 34
        canvas_h = 295
        self.canvas = tk.Canvas(
            self.main_frame,
            width=canvas_w,
            height=canvas_h,
            bg=BG_CANVAS,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(padx=15, pady=5)

        # Floor line
        floor_y = canvas_h - 8
        self.floor_y = floor_y
        self.canvas.create_line(0, floor_y, canvas_w, floor_y, fill="#d0d8e8", width=2)
        # Shadow under character position
        self.canvas.create_oval(120, floor_y - 5, 270, floor_y + 5, fill="#e0e4ec", outline="")

        # Character image
        self.char_item = self.canvas.create_image(
            POPUP_WIDTH, floor_y - 2, anchor="sw",
            image=self.idle_sprite.frames[0] if self.has_sprites else None,
        )

        # ── Buttons ──
        self.btn_frame = tk.Frame(self.main_frame, bg=BG_DARK)
        self.btn_frame.pack(pady=(10, 12))

        self.drink_btn = tk.Button(
            self.btn_frame,
            text="  ✅  Yes, I drank water!  ",
            bg=ACCENT_GREEN, fg="#1a1b2e",
            activebackground="#25b890", activeforeground="#1a1b2e",
            font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2", bd=0, pady=10,
            command=self._on_drank,
        )

        self.snooze_btn = tk.Button(
            self.btn_frame,
            text="  ⏰  Snooze  ",
            bg=ACCENT_ORANGE, fg="white",
            activebackground="#e07730", activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2", bd=0, pady=10,
            command=self._on_snooze,
        )

        # Hidden until notification
        self.drink_btn.pack_forget()
        self.snooze_btn.pack_forget()

        # ── Status ──
        self.status_label = tk.Label(
            self.main_frame, text="",
            bg=BG_DARK, fg=TEXT_SECONDARY,
            font=("Segoe UI", 9),
        )
        self.status_label.pack(pady=(0, 8))

    # ── Slide Animations ─────────────────────────────────────────────────────
    def _slide_in(self):
        """Slide popup up from below screen."""
        self.state = "sliding_in"
        self.current_y = self.popup_y_hidden
        self._do_slide_in()

    def _do_slide_in(self):
        if self.state != "sliding_in":
            return
        self.current_y -= SLIDE_SPEED
        if self.current_y <= self.popup_y_shown:
            self.current_y = self.popup_y_shown
            self.root.geometry(f"+{self.popup_x}+{self.current_y}")
            # Start character walking in from the right
            self.state = "walk_in"
            self.char_x = POPUP_WIDTH + 50
            self.walk_in_sprite.reset()
            self._animate_walk_in()
            return
        self.root.geometry(f"+{self.popup_x}+{self.current_y}")
        self._slide_id = self.root.after(16, self._do_slide_in)

    def _slide_out(self, callback):
        """Slide popup down below screen."""
        self.state = "sliding_out"
        self._do_slide_out(callback)

    def _do_slide_out(self, callback):
        if self.state != "sliding_out":
            return
        self.current_y += SLIDE_SPEED
        if self.current_y >= self.popup_y_hidden:
            self.current_y = self.popup_y_hidden
            self.root.geometry(f"+{self.popup_x}+{self.current_y}")
            self.state = "hidden"
            callback()
            return
        self.root.geometry(f"+{self.popup_x}+{self.current_y}")
        self._slide_id = self.root.after(16, lambda: self._do_slide_out(callback))

    # ── Character Animations ─────────────────────────────────────────────────
    def _animate_walk_in(self):
        """Character walks from right to left."""
        if self.state != "walk_in":
            return
        self.char_x -= WALK_SPEED  # Move left
        if self.char_x <= self.target_x:
            self.char_x = self.target_x
            self.state = "showing"
            self._show_reminder_ui()
            self._animate_idle()
            return

        if self.has_sprites:
            frame = self.walk_in_sprite.next_frame()
            self.canvas.itemconfigure(self.char_item, image=frame)
        self.canvas.coords(self.char_item, self.char_x, self.floor_y - 2)
        self._anim_id = self.root.after(ANIM_TICK_MS, self._animate_walk_in)

    def _animate_idle(self):
        """Loop drinking animation while showing reminder."""
        if self.state != "showing":
            return
        if self.has_sprites and self.drinking_sprite.valid:
            frame = self.drinking_sprite.next_frame()
            self.canvas.itemconfigure(self.char_item, image=frame)
        self.canvas.coords(self.char_item, self.char_x, self.floor_y - 2)
        self._sprite_id = self.root.after(SPRITE_FRAME_MS, self._animate_idle)

    def _animate_walk_out(self, callback):
        """Character walks out to the right (back where she came from)."""
        if self.state != "walk_out":
            return
        self.char_x += WALK_SPEED  # Exit to the right
        if self.char_x > POPUP_WIDTH + 150:
            # Character exited, now slide popup down
            self._slide_out(callback)
            return

        if self.has_sprites:
            frame = self.walk_out_sprite.next_frame()
            self.canvas.itemconfigure(self.char_item, image=frame)
        self.canvas.coords(self.char_item, self.char_x, self.floor_y - 2)
        self._anim_id = self.root.after(ANIM_TICK_MS, lambda: self._animate_walk_out(callback))

    # ── Notification Flow ────────────────────────────────────────────────────
    def _schedule_reminder(self, delay_ms):
        if self._reminder_id:
            self.root.after_cancel(self._reminder_id)
        self._reminder_id = self.root.after(delay_ms, self._trigger_notification)

    def _trigger_notification(self):
        """Slide in from the bottom-right."""
        self.root.deiconify()
        self._slide_in()

    def _show_reminder_ui(self):
        self.speech_label.config(text=SPEECH_TEXT)
        self.drink_btn.pack(side="left", padx=8)
        self.snooze_btn.pack(side="left", padx=8)

    def _hide_reminder_ui(self):
        self.speech_label.config(text="")
        self.drink_btn.pack_forget()
        self.snooze_btn.pack_forget()

    def _start_walk_out(self, next_delay_ms):
        """Character walks out, popup slides down, timer restarts."""
        if self._sprite_id:
            self.root.after_cancel(self._sprite_id)
        self._hide_reminder_ui()
        self.state = "walk_out"
        self.walk_out_sprite.reset()

        def on_hidden():
            self._schedule_reminder(next_delay_ms)

        self._animate_walk_out(on_hidden)

    # ── Button Handlers ──────────────────────────────────────────────────────
    def _on_drank(self):
        self.water_count += 1
        self.counter_label.config(text=f"🥤 {self.water_count}")
        self._start_walk_out(REMINDER_INTERVAL_MS)

    def _on_snooze(self):
        self._start_walk_out(SNOOZE_INTERVAL_MS)

    # ── Run ───────────────────────────────────────────────────────────────────
    def run(self):
        self.root.geometry(
            f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{self.popup_x}+{self.popup_y_hidden}"
        )
        self.root.mainloop()


# ── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Auto-generate sprites if missing
    if not os.path.exists(os.path.join(ASSETS_DIR, "walk_in.gif")):
        print("Sprites not found. Generating...")
        try:
            import generate_sprites
            generate_sprites.generate_walk_in()
            generate_sprites.generate_drinking()
            generate_sprites.generate_walk_out()
            generate_sprites.generate_idle()
        except Exception as e:
            print(f"Warning: Could not generate sprites: {e}")

    app = HydrationBuddy()
    app.run()
