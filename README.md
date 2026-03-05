# 🌌 Nebula Reveal Bot

A GitHub Actions bot that reveals **50 pixels per commit, 1–10 commits per day** of a nebula photograph.

## Progress

| Stat | Value |
|------|-------|
| Pixels revealed | 50 / 300,502 |
| Completion | 0.017% |
| Total commits | 1 |
| Estimated completion | ~2y 12m |

![Current State](current_large.png)

> *The image is 694×433 pixels (300,502 total). Each commit reveals 50 pixels, with 1–10 commits per day.*

## How it works

1. **GitHub Actions** runs daily via cron
2. `reveal.py plan` picks 1–10 random batches for the day
3. Each batch of 50 pixels gets its own commit
4. The nebula slowly emerges over ~3 years ✨
