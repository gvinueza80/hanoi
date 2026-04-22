# Snake Game Design Spec

**Date:** April 22, 2026  
**Purpose:** A modern, polished snake game for casual play and sharing  
**Platform:** Desktop (Windows, macOS, Linux)  
**Tech Stack:** Python 3.9+, Pygame  

---

## Overview

A graphical snake game built with Pygame featuring three distinct game modes (Arcade, Time Attack, Puzzle), progressive difficulty, power-ups, obstacles, and local multiplayer support. The game prioritizes fun, responsive gameplay, and polish over complexity.

---

## Game Modes

### Arcade Mode (Single & Multiplayer)
- **Endless gameplay** with progressive difficulty
- Difficulty increases every 5-10 seconds: snake gets faster, more obstacles spawn
- **Power-ups:** Speed Boost, Shield, Score Multiplier, Freeze Enemies (randomly spawned)
- **Scoring:** Regular food (+10), bonus food (+50)
- **End condition:** Snake hits wall, itself, or an obstacle
- **Leaderboard:** Top 5 scores saved locally
- **Multiplayer variant:** Two snakes (red/blue) on shared board; last alive wins

### Time Attack Mode (Single-Player)
- Survive within time limit (60-180 seconds, difficulty-dependent)
- More aggressive obstacle spawning than Arcade
- Difficulty spike every 10 seconds (more obstacles or faster snake)
- Goal: maximize score before time expires
- No leaderboard persistence; immediate feedback on game end

### Puzzle Mode (Single-Player)
- 10-15 pre-designed levels with fixed obstacle layouts
- **Goal:** Eat all food without hitting obstacles (or within move limit in advanced levels)
- No time pressure; player-paced progression
- Difficulty increases progressively across levels
- Replayable with personal best score tracking per level

---

## Core Game Mechanics

### Snake
- Moves in 4 directions (Arrow Keys or WASD for Player 1; WASD or configurable for Player 2)
- Cannot reverse into itself; self-collision ends game
- Grows by 1 segment per food eaten
- Base speed: 10 grid units/second; modified by difficulty and power-ups

### Food & Scoring
| Type | Points | Frequency |
|------|--------|-----------|
| Regular food | +10 | Normal spawn rate |
| Bonus food | +50 | Rare, larger visual |
| Power-up touch | Varies | Effect-based bonus |

### Power-ups (5-10 second duration)
- **Speed Boost:** Snake moves 1.5x faster
- **Shield:** Absorbs one collision (wall, obstacle, or self)
- **Score Multiplier:** All points earned are 2x for duration
- **Freeze:** All moving obstacles freeze for 5 seconds

### Obstacles (Progressive Appearance)
| Type | Behavior | Danger Level |
|------|----------|--------------|
| Static walls | Permanent, immobile | Medium (requires navigation) |
| Moving walls | Slide back-and-forth on fixed axis | High (timing required) |
| Spikes | Instant death on contact | Critical (avoid completely) |
| Spirals | Rotating obstacles | High (dynamic hazard) |

Obstacles spawn more frequently as difficulty increases, creating tighter gameplay challenges.

### Collision Detection
- **Snake + Food:** Eat and grow
- **Snake + Wall/Spike:** Game over
- **Snake + Power-up:** Activate effect (visual/audio feedback)
- **Snake + Self:** Game over
- **Two Snakes (Multiplayer):** Can pass through each other; only self-collision ends a snake

---

## Difficulty Progression

Difficulty scales **gradually and continuously** across all modes to support skill-building over time.

### Arcade Mode
- **Every 5-10 seconds:** Snake speed increases slightly, new obstacles spawn
- **Scaling curve:** Smooth, not sudden spikes
- **Plateau:** Game remains challenging but playable up to 5+ minutes

### Time Attack Mode
- **Difficulty spike every 10 seconds:** More obstacles or increased snake speed
- **Higher baseline difficulty** than Arcade (tighter play space)
- **Player goal:** Extend playtime as long as possible

### Puzzle Mode
- **Level-based progression:** Each level introduces new mechanics or tighter layouts
- **No speed pressure:** Puzzle-solving at player's pace
- **Optional move limits:** Advanced levels may include move constraints

---

## Local Multiplayer (Two-Player Arcade)

### Setup
- **Player 1 (Red Snake):** Arrow Keys for movement
- **Player 2 (Blue Snake):** WASD for movement
- Shared board with shared obstacles and progressive difficulty

### Win Conditions
- Last snake remaining alive wins
- Snakes can pass through each other but cannot occupy same space
- Both snakes affected equally by shared obstacles and difficulty spikes

### Food & Power-up Sharing
- Any food or power-up can be eaten by either snake (first to reach it wins)
- Power-ups apply only to the snake that touches them
- Scoring displayed separately for each player

---

## Technical Architecture

### Game Structure (Unified Game Loop)
```
Main Game Class
├── Mode Manager (tracks/switches between modes)
├── Game State (current mode, score, difficulty, etc.)
├── Entity Manager (snake, food, obstacles, power-ups)
├── Collision System (detection and resolution)
├── Rendering System (UI, sprites, animations)
└── Input Handler (keyboard, single/multiplayer)
```

### Project Layout
```
snake/
├── main.py                 # Entry point
├── game.py                 # Main Game class and loop
├── entities.py             # Snake, Food, PowerUp, Obstacle classes
├── modes.py                # Arcade, TimeAttack, Puzzle mode logic
├── collision.py            # Collision detection & physics
├── ui.py                   # Rendering and HUD
├── config.py               # Constants and settings
├── assets/
│   ├── sprites/            # PNG images
│   ├── sounds/             # WAV audio files
│   └── levels/             # JSON puzzle definitions
├── data/
│   └── high_scores.json    # Persistent leaderboard
├── requirements.txt
└── README.md
```

### Dependencies
- **pygame** — graphics, input, audio, game loop

### Data Persistence
- High scores saved to `data/high_scores.json` (top 5 per mode)
- Puzzle level definitions stored as JSON for easy creation/modification
- No external database; JSON files handle all persistence

---

## Success Criteria

### Core Gameplay
- [ ] Snake moves smoothly with no input lag
- [ ] Collision detection is pixel-perfect and reliable
- [ ] All three game modes are fully playable
- [ ] Arcade mode difficulty progression feels fair and engaging
- [ ] Power-ups spawn, activate, and expire correctly
- [ ] Obstacles render and collide properly
- [ ] High scores persist and display correctly

### Multiplayer
- [ ] Two snakes render simultaneously without visual overlap issues
- [ ] Both players' inputs respond immediately
- [ ] Shared game state (obstacles, food) updates consistently for both
- [ ] Win detection (last snake alive) works correctly

### Polish
- [ ] Responsive input (no perceptible lag)
- [ ] Clear, readable UI (score, mode, difficulty indicator)
- [ ] Visual contrast is good; colors distinguish snakes, obstacles, food
- [ ] Sound effects provide clear feedback (eat, collision, power-up)
- [ ] Menu system for mode/difficulty selection
- [ ] Pause functionality during gameplay
- [ ] Game-over screen shows final score and replay option

### Testing
- Manual playthrough of each mode with various difficulties
- Two-player Arcade test with simultaneous play
- Power-up activation and duration validation
- Collision edge cases (narrow corridors, corners)
- High score save/load verification

---

## Future Enhancements (Out of Scope)

These are not part of this design but could be added later:
- Online multiplayer (would require network code)
- Mobile version (different input/screen constraints)
- Procedurally generated puzzle levels
- Leaderboard rankings with dates
- Customizable difficulty settings
- Themes/visual skins

---

## Assumptions & Constraints

- **Single PC, local play only** — no network multiplayer
- **Window size:** Fixed resolution (800x600 or configurable)
- **Grid-based movement:** Snake moves on discrete grid squares (not pixel-smooth)
- **Frame rate:** Locked at ~60 FPS for consistent gameplay
- **No mobile support** — keyboard/gamepad input only
- **No external networking** — all data stored locally

---

## Open Questions (None)

All design decisions have been finalized in the brainstorming phase.
