# 🐍 RetroSnake

[![Built with Python](https://img.shields.io/badge/Built%20with-Python-306998?logo=python&logoColor=white)](https://www.python.org/)
[![Game Ready](https://img.shields.io/badge/Status-Final%20v1.0.0-brightgreen)](https://github.com/your-repo/RetroSnake/releases)
[![Sound FX](https://img.shields.io/badge/Sound-Enabled-blueviolet)](assets/)
[![Leaderboard](https://img.shields.io/badge/Leaderboard-Top%205-lightgrey)](leaderboard.json)

> **"Classic gaming. Clean execution. No filler."**  
> — *Omnis Lux Capital*

---

## 🎮 What Is RetroSnake?

RetroSnake is a modern twist on the classic arcade game — complete with:

- Smooth animation
- Sound effects
- Power-ups
- Real-time leaderboard
- Clean pause + restart logic

Crafted from scratch in Python using `pygame`, with a minimalist retro aesthetic and fully modular code.

---

## 🚀 Features

- **Responsive Keyboard Controls**
- **Animated Background** with sine wave glow
- **Eat Food to Grow**
- **Random Power-Ups** that boost score
- **Real-Time Leaderboard** (Top 5 only)
- **Pause / Resume / Restart** via ESC
- **Full Audio FX** for gameplay events
- **Clean UX** and portable build

---

## 🛠️ Tech Stack

- `Python 3.10+`
- `pygame` (2.0+)
- JSON for saving leaderboard
- WAV files for retro sound effects

---

## 📁 File Structure

RetroSnake/

├── assets/               # Audio files

│   ├── eat.wav

│   ├── game_over.wav

│   ├── menu_click.wav

│   └── powerup.wav

├── leaderboard.json      # Top 5 highscores

├── highscore.txt         # Session best

├── main.py               # Core game loop

└── README.md             # This file

---

## 🧠 Design Philosophy

- Built to **feel vintage**, run modern
- Engineered with **clarity and simplicity**
- No bloat. No clutter. **Pure gameplay.**

---

## ✅ How to Play

| Key       | Action             |
|-----------|--------------------|
| `↑ ↓ ← →` | Move snake         |
| `ESC`     | Pause / Restart    |
| `Enter`   | Save leaderboard   |

- Collect food: `+10 points`
- Grab power-ups: `+25 points`
- Avoid hitting yourself!
- Your score is saved only if it’s a **Top 5**.

---

## 🔊 Audio Not Working?

Make sure you have:

- `.wav` files in `assets/`
- `pygame.mixer` initialized properly
- Your system audio enabled

---

## 📦 Release Info

- **Final Release:** `v1.0.0`
- **Status:** Stable, fully tested
- ✅ Versioned using semantic format: `v1.0.0`, `v1.1.0`, etc.

---

## 🔒 License

Open-source for **learning, remixing, and inspiration**.  
Respect the work, and give credit where it’s due.

---

> **Built by Omnis Lux Capital.**  
> *Let there be light.*
