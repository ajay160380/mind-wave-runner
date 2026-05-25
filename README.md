# 🦖 Mind-Wave: Classic Dino Gesture Runner

A premium, modern 8-bit Chrome Dino-style runner game built with Python and Pygame.
The unique twist? It uses your laptop's webcam and **Google MediaPipe Tasks API** to decode your real-time hand gestures in the background for ultra-smooth gameplay control!

---


## 🎮 Game Controls & Protocol

### 🖐️ Gesture Control Protocol (Webcam HUD)
The game tracks your hand in real-time using a **mathematically rotation-invariant 2D Wrist-Relative Euclidean Distance** algorithm. This ensures 100% stable tracking, completely eliminating noisy 3D depth fluctuations:

| Gesture | Action | In-Game Telemetry |
| :--- | :--- | :--- |
| **Palm Open 🖐️** <br>*(3 or 4 fingers extended)* | ☄️ **JUMP** | Dodge low and high cacti obstacles |
| **Palm Closed / Fist ✊** <br>*(0 or 1 fingers extended)* | 🏎️ **DUCK & SLIDE** | Slip under low flying Pterodactyls |
| **Relaxed Hand ✌️** <br>*(2 fingers extended)* | 🦖 **RUN** | Standard speed running state |

> [!TIP]
> The webcam PiP feed is visible globally across all states (Start Menu, Play, Game Over), allowing you to easily calibrate and align your hand before starting the run!

### ⌨️ Manual Cyber-Keyboard Fallback
If your webcam is offline, unauthorized, or detecting failure, the system instantly engages manual telemetry:
* **SPACEBAR** ➔ **JUMP**
* **DOWN ARROW** ➔ **DUCK & SLIDE**
* **UP ARROW** ➔ **UNDUCK**
* **R KEY / SPACEBAR** ➔ **REBOOT SYSTEM (RESTART / RESUME)**

---

## 💎 Advanced Game Engine Features

1. **⚡ Auto-Unduck Quick Response Override:**
   * Experience absolute arcade responsiveness. If you are currently sliding on the ground (ducking) and instantly open your palm (jump), the game engine **automatically cancels the slide and leaps into the air instantly** with zero delay!

2. **📏 Distance-Based Spawning Physics:**
   * Obstacle spawning is calculated using **actual pixel scroll distance** rather than frame time. A new obstacle is guaranteed to have a safe physical gap of **850 to 1300 pixels** from the previous one, ensuring you always have a comfortable, fair, and satisfying landing window before the next hurdle.

3. **📈 Smooth Speed Calibration:**
   * The initial game speed starts at a balanced **5.6** and ramps up gently based on your score (`+0.4` speed for every `180` points), capped at a perfectly playable maximum of **11.5**.

4. **🔊 Nostalgic 8-Bit Audiovisuals:**
   * **Parallax Scrolling:** Background clouds, parallax mountains, and dotted roads scroll at varying speeds for retro depth.
   * **Retro Particle Dust:** Grey pixelated dust puffs up under the Dino's feet when running, jumping, and sliding!
   * **8-Bit Audio Synthesizer:** Natively generates retro wave files (Jump, Slide, Pickup, Crash) upon launch.
   * **Zero Dependency Player:** Plays audio using macOS native `afplay` in background threads for lag-free performance.

---

## 🛠️ Installation & Execution

### 1. Set Up Environment & Install Dependencies
First, create your virtual environment and install the required packages:
```bash
# Initialize Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 2. Generate Graphic Assets & Play!
You can run the asset generator engine to prepare all sprite buffers and launch the game:
```bash
# Generate high-quality retro assets
python3 create_assets.py

# Launch the game
python3 main.py
```

---

## 🧬 Under The Hood (AI Telemetry)

The hand tracker module utilizes Google MediaPipe's Hand Landmarker API to capture 21 distinct 3D landmarks of your hand. 
* **Calibration Independence:** Normalizes hand size based on the absolute pixel distance between landmark `0` (wrist) and landmark `9` (MCP joint of middle finger). This guarantees the gestures work whether you are 1 foot or 6 feet away from the camera!
* **Multithreaded Performance:** OpenCV camera capture and MediaPipe inference run in a dedicated background thread, maintaining a solid, butter-smooth 60 FPS for Pygame rendering.
