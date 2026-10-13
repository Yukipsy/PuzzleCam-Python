from pathlib import Path
import pygame


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOUND_DIR = PROJECT_ROOT / "assets" / "sounds"


class SoundManager:
    def __init__(self):
        self.enabled = True
        self.sounds = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            self.sounds = {
                "countdown": self.load_sound("countdown.wav"),
                "shutter": self.load_sound("shutter.wav"),
                "correct": self.load_sound("correct.wav"),
                "wrong": self.load_sound("wrong.wav"),
                "shatter": self.load_sound("shatter.wav"),
            }

        except Exception as error:
            print(f"[Sound] Audio disabled: {error}")
            self.enabled = False

    def load_sound(self, filename):
        path = SOUND_DIR / filename

        if not path.exists():
            print(f"[Sound] Missing: {path.name}")
            return None

        return pygame.mixer.Sound(str(path))

    def play(self, name):
        if not self.enabled:
            return

        sound = self.sounds.get(name)

        if sound is not None:
            sound.play()

    def close(self):
        if pygame.mixer.get_init():
            pygame.mixer.stop()