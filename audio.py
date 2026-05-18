import wave
import struct
import math
import random
import subprocess
import os
from settings import resource_path

def synthesize_jump(filepath="assets/jump.wav"):
    sample_rate = 22050
    duration = 0.2
    num_samples = int(duration * sample_rate)
    
    with wave.open(filepath, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(1) # 8-bit unsigned
        w.setframerate(sample_rate)
        
        frames = []
        for i in range(num_samples):
            t = i / sample_rate
            # Rising pitch sweep: 200Hz to 900Hz
            freq = 200 + 700 * (t / duration)
            val = int(127 + 60 * math.copysign(1.0, math.sin(2 * math.pi * freq * t)))
            # Volume envelope (fade out at the very end)
            envelope = 1.0 - (t / duration) ** 2
            val = int(127 + (val - 127) * envelope)
            frames.append(struct.pack('B', max(0, min(255, val))))
            
        w.writeframes(b''.join(frames))

def synthesize_slide(filepath="assets/slide.wav"):
    sample_rate = 22050
    duration = 0.3
    num_samples = int(duration * sample_rate)
    
    with wave.open(filepath, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(1)
        w.setframerate(sample_rate)
        
        frames = []
        for i in range(num_samples):
            t = i / sample_rate
            # Buzzing low pitch: 180Hz down to 100Hz
            freq = 180 - 80 * (t / duration)
            # Add some frequency modulation for a vibration feel
            freq += math.sin(2 * math.pi * 50 * t) * 10
            val = int(127 + 50 * math.copysign(1.0, math.sin(2 * math.pi * freq * t)))
            envelope = 1.0 - t / duration
            val = int(127 + (val - 127) * envelope)
            frames.append(struct.pack('B', max(0, min(255, val))))
            
        w.writeframes(b''.join(frames))

def synthesize_pickup(filepath="assets/pickup.wav"):
    sample_rate = 22050
    duration = 0.25
    num_samples = int(duration * sample_rate)
    
    with wave.open(filepath, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(1)
        w.setframerate(sample_rate)
        
        frames = []
        for i in range(num_samples):
            t = i / sample_rate
            # Perfect double-note retro chime
            # First 40% duration is Note E (659Hz), remaining is Note B (987Hz)
            freq = 659 if t < duration * 0.4 else 987
            val = int(127 + 70 * math.copysign(1.0, math.sin(2 * math.pi * freq * t)))
            envelope = 1.0 - t / duration
            val = int(127 + (val - 127) * envelope)
            frames.append(struct.pack('B', max(0, min(255, val))))
            
        w.writeframes(b''.join(frames))

def synthesize_crash(filepath="assets/crash.wav"):
    sample_rate = 22050
    duration = 0.5
    num_samples = int(duration * sample_rate)
    
    with wave.open(filepath, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(1)
        w.setframerate(sample_rate)
        
        frames = []
        for i in range(num_samples):
            t = i / sample_rate
            # White noise mixed with explosive rumble
            noise = random.uniform(-1.0, 1.0)
            envelope = (1.0 - t / duration) ** 3  # Steep curve
            val = int(127 + noise * 100 * envelope)
            frames.append(struct.pack('B', max(0, min(255, val))))
            
        w.writeframes(b''.join(frames))

def initialize_audio():
    """Ensure all assets are generated before game launch."""
    os.makedirs("assets", exist_ok=True)
    if not os.path.exists("assets/jump.wav"):
        synthesize_jump()
    if not os.path.exists("assets/slide.wav"):
        synthesize_slide()
    if not os.path.exists("assets/pickup.wav"):
        synthesize_pickup()
    if not os.path.exists("assets/crash.wav"):
        synthesize_crash()

def play_sound(sound_name):
    """Play the synthesized wave file in the background using macOS afplay."""
    sound_path = resource_path(f"assets/{sound_name}.wav")
    if os.path.exists(sound_path):
        try:
            # Popen spawns a non-blocking background shell to run afplay
            subprocess.Popen(
                ["afplay", sound_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass
