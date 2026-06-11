import json
import os
import pygame
from constants import DEFAULT_KEYBINDS, KEYBINDS_FILE


class KeybindManager:
    def __init__(self):
        self.binds: dict[str, str] = dict(DEFAULT_KEYBINDS)
        self.load()
        self._waiting_for: str | None = None

    def get_key(self, action: str) -> int | None:
        key_name = self.binds.get(action, "")
        try:
            return pygame.key.key_code(key_name.lower())
        except (ValueError, AttributeError):
            special = {
                "F1": pygame.K_F1, "F2": pygame.K_F2, "F3": pygame.K_F3,
                "F4": pygame.K_F4, "F5": pygame.K_F5, "F6": pygame.K_F6,
                "F7": pygame.K_F7, "F8": pygame.K_F8, "F9": pygame.K_F9,
                "F10": pygame.K_F10, "F11": pygame.K_F11, "F12": pygame.K_F12,
                "=": pygame.K_EQUALS, "-": pygame.K_MINUS, "+": pygame.K_PLUS,
            }
            return special.get(key_name)

    def is_key(self, action: str, key: int) -> bool:
        expected = self.get_key(action)
        return expected is not None and expected == key

    def start_rebind(self, action: str) -> None:
        self._waiting_for = action

    def finish_rebind(self, key: int) -> bool:
        if self._waiting_for is None:
            return False
        name = pygame.key.name(key)
        self.binds[self._waiting_for] = name
        self._waiting_for = None
        self.save()
        return True

    @property
    def is_rebinding(self) -> bool:
        return self._waiting_for is not None

    @property
    def rebinding_action(self) -> str | None:
        return self._waiting_for

    def save(self) -> None:
        os.makedirs(os.path.dirname(KEYBINDS_FILE), exist_ok=True)
        with open(KEYBINDS_FILE, "w") as f:
            json.dump(self.binds, f, indent=2)

    def load(self) -> None:
        if os.path.exists(KEYBINDS_FILE):
            try:
                with open(KEYBINDS_FILE) as f:
                    loaded = json.load(f)
                self.binds.update(loaded)
            except Exception:
                pass