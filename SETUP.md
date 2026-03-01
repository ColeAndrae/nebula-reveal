# 🚀 Setup Guide

## Step 1: Create a new GitHub repo

Go to github.com/new and create a **public** repo (e.g. `nebula-reveal`).

## Step 2: Push this folder to GitHub

```bash
cd nebula-bot
git init
git add .
git commit -m "🌌 Initial commit - let the reveal begin"
git remote add origin https://github.com/YOUR_USERNAME/nebula-reveal.git
git branch -M main
git push -u origin main
```

## Step 3: Enable workflow write permissions

In your repo on GitHub:
1. Go to **Settings** → **Actions** → **General**
2. Under "Workflow permissions", select **Read and write permissions**
3. Click **Save**

## Step 4: Watch it run!

- The bot runs automatically every day at **midnight UTC**
- You can also trigger it manually: go to **Actions** → **Daily Nebula Reveal** → **Run workflow**
- Each run reveals 1–5 random pixels and commits the updated image

## Customizing

- **Change schedule**: Edit `cron: '0 0 * * *'` in `.github/workflows/daily-reveal.yml`
- **Change pixels per day**: Edit `random.randint(1, 5)` in `reveal.py`
- **Use a different image**: Replace `nebula_target.webp`, update dimensions in `reveal.py`, and re-run the pixel extraction step

## File structure

```
nebula-bot/
├── .github/
│   └── workflows/
│       └── daily-reveal.yml   # GitHub Actions cron job
├── reveal.py                  # Main script - picks & reveals pixels
├── pixel_data.json            # Target pixel color data (80x50)
├── nebula_target.png          # The target image (80x50 scaled)
├── nebula_target.webp         # Original uploaded image
├── current.png                # Current state (80x50) - updated each commit
├── current_large.png          # Current state (800x500) - shown in README
├── state.json                 # Tracks which pixels have been revealed
├── requirements.txt
└── README.md                  # Auto-generated progress page
```
