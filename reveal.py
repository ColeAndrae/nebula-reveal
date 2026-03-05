#!/usr/bin/env python3
"""
Nebula Reveal Bot - High Resolution Edition
- `python reveal.py plan`  → picks 1-10 batches for today, saves to pixels_today.json
- `python reveal.py <idx>` → reveals 50 pixels around idx, updates state/image/README
"""

import json
import random
import os
import sys
from PIL import Image, ImageDraw

WIDTH = 694
HEIGHT = 433
TOTAL_PIXELS = WIDTH * HEIGHT
PIXELS_PER_COMMIT = 50

def load_state():
    if os.path.exists("state.json"):
        with open("state.json") as f:
            return json.load(f)
    return {"revealed": [], "total_commits": 0, "pixels_revealed": 0}

def load_pixel_data():
    with open("pixel_data.json") as f:
        return json.load(f)

def save_state(state):
    with open("state.json", "w") as f:
        json.dump(state, f, indent=2)

def generate_image(state, pixel_data):
    pixels = pixel_data["pixels"]
    revealed_set = set(state["revealed"])
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    for idx in revealed_set:
        x = idx % WIDTH
        y = idx // WIDTH
        r, g, b = pixels[idx]
        draw.point((x, y), fill=(r, g, b))
    img.save("current.png")
    # Save display version at 2x
    large = img.resize((WIDTH * 2, HEIGHT * 2), Image.NEAREST)
    large.save("current_large.png")

def generate_readme(state):
    pct = state["pixels_revealed"] / TOTAL_PIXELS * 100
    remaining = TOTAL_PIXELS - state["pixels_revealed"]
    days_left = remaining / (5.5 * PIXELS_PER_COMMIT)
    years = int(days_left // 365)
    months = int((days_left % 365) // 30)

    readme = f"""# 🌌 Nebula Reveal Bot

A GitHub Actions bot that reveals **{PIXELS_PER_COMMIT} pixels per commit, 1–10 commits per day** of a nebula photograph.

## Progress

| Stat | Value |
|------|-------|
| Pixels revealed | {state['pixels_revealed']:,} / {TOTAL_PIXELS:,} |
| Completion | {pct:.3f}% |
| Total commits | {state['total_commits']:,} |
| Estimated completion | ~{years}y {months}m |

![Current State](current_large.png)

> *The image is {WIDTH}×{HEIGHT} pixels ({TOTAL_PIXELS:,} total). Each commit reveals {PIXELS_PER_COMMIT} pixels, with 1–10 commits per day.*

## How it works

1. **GitHub Actions** runs daily via cron
2. `reveal.py plan` picks 1–10 random batches for the day
3. Each batch of {PIXELS_PER_COMMIT} pixels gets its own commit
4. The nebula slowly emerges over ~3 years ✨
"""
    with open("README.md", "w") as f:
        f.write(readme)

def plan_day():
    state = load_state()
    revealed_set = set(state["revealed"])
    unrevealed = [i for i in range(TOTAL_PIXELS) if i not in revealed_set]

    if not unrevealed:
        print("COMPLETE")
        with open("pixels_today.json", "w") as f:
            json.dump([], f)
        return

    # Each entry in the plan is a starting index for a batch of PIXELS_PER_COMMIT
    num_batches = random.randint(1, 10)
    # Pick num_batches * PIXELS_PER_COMMIT random pixels
    count = min(num_batches * PIXELS_PER_COMMIT, len(unrevealed))
    chosen = random.sample(unrevealed, count)
    # Split into batches
    batches = [chosen[i:i+PIXELS_PER_COMMIT] for i in range(0, len(chosen), PIXELS_PER_COMMIT)]
    print(f"Planned {len(batches)} batch(es) of {PIXELS_PER_COMMIT} pixels each today")
    with open("pixels_today.json", "w") as f:
        json.dump(batches, f)

def reveal_batch(batch_index):
    batch_index = int(batch_index)
    state = load_state()
    pixel_data = load_pixel_data()

    with open("pixels_today.json") as f:
        batches = json.load(f)

    batch = batches[batch_index]
    new_pixels = [p for p in batch if p not in state["revealed"]]

    if not new_pixels:
        print(f"Batch {batch_index} already revealed, skipping.")
        return

    state["revealed"].extend(new_pixels)
    state["total_commits"] += 1
    state["pixels_revealed"] = len(state["revealed"])

    print(f"Batch {batch_index}: revealed {len(new_pixels)} pixels | {state['pixels_revealed']:,}/{TOTAL_PIXELS:,} ({state['pixels_revealed']/TOTAL_PIXELS*100:.3f}%)")

    generate_image(state, pixel_data)
    generate_readme(state)
    save_state(state)
    print("Done ✨")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "plan":
        plan_day()
    else:
        reveal_batch(sys.argv[1])
