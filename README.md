# 🌌 Nebula Reveal Bot

A GitHub Actions bot that reveals **1–10 pixels per day** of a nebula photograph — one commit per pixel.

## Progress

| Stat | Value |
|------|-------|
| Pixels revealed | 15 / 4,000 |
| Completion | 0.38% |
| Total commits | 15 |
| Estimated completion | ~1y 11m |

![Current State](current_large.png)

> *The image is 80×50 pixels. Each day reveals 1–10 pixels randomly, with one commit per pixel.*

## How it works

1. **GitHub Actions** runs daily via cron
2. `reveal.py plan` picks 1–10 random unrevealed pixels for the day
3. A loop commits each pixel individually — so your commit history reflects the real count
4. Each commit updates `current_large.png` in the README

## Setup

1. Push this repo to GitHub
2. Go to **Settings → Actions → General → Workflow permissions** → set to **Read and write**
3. Trigger manually from the **Actions** tab, or wait for midnight UTC
