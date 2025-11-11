# Pong — Two Player Edition 🏓

A simple **two-player Pong game** written in Python with [Pygame](https://www.pygame.org/).  
No fancy frameworks, no AI — just you, a friend, and a ball bouncing around.

---

## 🎮 Gameplay

Classic retro Pong for two people:

| Player | Keys |
|:-------|:------|
| **Left** | `W` (up), `S` (down) |
| **Right** | `↑` (up), `↓` (down) |

Other keys:
- `P` — pause / unpause  
- `R` — restart round  
- `Esc` — quit the game  

The first player to reach **10 points** wins.  
You can change the score limit inside the code (`SCORE_TO_WIN`).

---

## ⚙️ Requirements

You only need Python 3.10+ and Pygame installed:

```bash
pip install pygame
