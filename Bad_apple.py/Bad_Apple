import json
from pathlib import Path
from rich.live import Live
from rich.console import Console
import time
import pygame
console = Console()
json_path = Path(__file__).parent / "frames.json"
music_path = Path(__file__).parent / “yes.mp3”
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)
def get_frame(i):
    key = f'frame_{i:04d}'
    return data.get(key)
pygame.mixer.init()
pygame.mixer.music.load(r"C:\Users\Kelly\Desktop\project\Bad_Apple\yes.mp3")
music_start_delay = 0.2 
pygame.mixer.music.play()
time.sleep(music_start_delay)
print("\033[?25l", end="", flush=True)
with Live(console=console, refresh_per_second=30, screen=True) as live:
    for i in range(1, 6573):
        live.update(get_frame(i))
        time.tick(30)
pygame.mixer.music.stop()
print("\033[?25h", end="", flush=True)
