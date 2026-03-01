#!/usr/bin/env python3
"""
Nebula Reveal Bot
- `python reveal.py plan`  → picks 1-10 pixels for today, saves to pixels_today.json
- `python reveal.py <idx>` → reveals one pixel, updates state/image/README (one commit per call)
"""

import json
import random
import os
import sys
from PIL import Image, ImageDraw

WIDTH = 80
HEIGHT = 50
TOTAL_PIXELS = WIDTH * HEIGHT

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
    large = img.resize((800, 500), Image.NEAREST)
    large.save("current_large.png")

def generate_readme(state):
    pct = state["pixels_revealed"] / TOTAL_PIXELS * 100
    remaining = TOTAL_PIXELS - state["pixels_revealed"]
    days_left = remaining / 5.5  # avg of 1-10 = 5.5
    years = int(days_left // 365)
    months = int((days_left % 365) // 30)

    readme = f"""# 🌌 Nebula Reveal Bot

A GitHub Actions bot that reveals **1–10 pixels per day** of a nebula photograph — one commit per pixel.

## Progress

| Stat | Value |
|------|-------|
| Pixels revealed | {state['pixels_revealed']:,} / {TOTAL_PIXELS:,} |
| Completion | {pct:.2f}% |
| Total commits | {state['total_commits']:,} |
| Estimated completion | ~{years}y {months}m |

![Current State](current_large.png)

> *The image is {WIDTH}×{HEIGHT} pixels. Each day reveals 1–10 pixels randomly, with one commit per pixel.*

## How it works

1. **GitHub Actions** runs daily via cron
2. `reveal.py plan` picks 1–10 random unrevealed pixels for the day
3. A loop commits each pixel individually — so your commit history reflects the real count
4. Each commit updates `current_large.png` in the README

## Setup

1. Push this repo to GitHub
2. Go to **Settings → Actions → General → Workflow permissions** → set to **Read and write**
3. Trigger manually from the **Actions** tab, or wait for midnight UTC
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
    count = random.randint(1, min(10, len(unrevealed)))
    chosen = random.sample(unrevealed, count)
    print(f"Planned {count} pixel(s) for today: {chosen}")
    with open("pixels_today.json", "w") as f:
        json.dump(chosen, f)

def reveal_one(pixel_index):
    pixel_index = int(pixel_index)
    state = load_state()
    pixel_data = load_pixel_data()

    if pixel_index in state["revealed"]:
        print(f"Pixel {pixel_index} already revealed, skipping.")
        return

    state["revealed"].append(pixel_index)
    state["total_commits"] += 1
    state["pixels_revealed"] = len(state["revealed"])

    x = pixel_index % WIDTH
    y = pixel_index // WIDTH
    color = pixel_data["pixels"][pixel_index]
    print(f"Pixel {pixel_index} ({x},{y}) → rgb{tuple(color)} | {state['pixels_revealed']}/{TOTAL_PIXELS} ({state['pixels_revealed']/TOTAL_PIXELS*100:.2f}%)")

    generate_image(state, pixel_data)
    generate_readme(state)
    save_state(state)
    print("Done ✨")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "plan":
        plan_day()
    else:
        reveal_one(sys.argv[1])
