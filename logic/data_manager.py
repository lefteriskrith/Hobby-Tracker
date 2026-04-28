"""
Data model and persistence layer for Hobby Tracker.

Hobby   — immutable-ish dataclass; all dates stored as ISO strings (YYYY-MM-DD).
DataManager — reads/writes a single JSON file; keeps an in-memory list as cache.

The JSON file location is resolved at startup:
  • Source run  → project root / hobbies_data.json
  • Frozen .exe → next to the executable
"""

import json
import sys
from dataclasses import asdict, dataclass, fields
from pathlib import Path


@dataclass
class Hobby:
    """A single hobby entry as stored in JSON."""

    name: str
    start_date: str        # ISO YYYY-MM-DD
    end_date: str = ""     # empty string means "still active"
    added_date: str = ""   # when the record was created
    comments: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Hobby":
        """Construct from a dict, silently dropping any unrecognised keys.

        This makes deserialization forward-compatible: loading a JSON file
        written by an older version of the app (with fewer fields) or a
        future version (with extra fields) both work without errors.
        """
        allowed = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in allowed})


class DataManager:
    """Manages CRUD operations on the hobbies JSON file.

    The in-memory list (self.hobbies) is always kept in sync with the file.
    Call reload_hobbies() when another process might have written to the file.
    """

    DATA_FILENAME = "hobbies_data.json"

    def __init__(self):
        self.data_path = self._resolve_data_path()
        self.hobbies = self._load_hobbies()

    # ── Path resolution ───────────────────────────────────────────────────────

    def _resolve_data_path(self) -> Path:
        """Return a writable path for the JSON file.

        sys.frozen is set by PyInstaller, so frozen builds store data next to
        the .exe instead of in the (read-only) internal bundle.
        """
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent / self.DATA_FILENAME
        return Path(__file__).resolve().parent.parent / self.DATA_FILENAME

    # ── Read ──────────────────────────────────────────────────────────────────

    def reload_hobbies(self) -> list:
        """Re-read the JSON file and refresh the in-memory cache."""
        self.hobbies = self._load_hobbies()
        return self.hobbies

    def _load_hobbies(self) -> list:
        if not self.data_path.exists():
            return []
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return [Hobby.from_dict(item) for item in json.load(f)]
        except (json.JSONDecodeError, KeyError):
            return []

    def get_all_hobbies(self) -> list:
        return self.hobbies

    # ── Write ─────────────────────────────────────────────────────────────────

    def save_hobby(self, hobby: Hobby) -> None:
        """Append hobby, or replace an existing one with the same name (case-insensitive)."""
        existing = next(
            (h for h in self.hobbies if h.name.lower() == hobby.name.lower()), None
        )
        if existing:
            self.hobbies.remove(existing)
        self.hobbies.append(hobby)
        self._save_to_file()

    def update_hobby(self, old_name: str, hobby: Hobby) -> None:
        """Replace the hobby whose name matches old_name (case-insensitive)."""
        for i, h in enumerate(self.hobbies):
            if h.name.lower() == old_name.lower():
                self.hobbies[i] = hobby
                self._save_to_file()
                return

    def delete_hobby(self, hobby_name: str) -> None:
        """Remove by name (case-insensitive) and persist."""
        self.hobbies = [
            h for h in self.hobbies if h.name.lower() != hobby_name.lower()
        ]
        self._save_to_file()

    # ── Internal ──────────────────────────────────────────────────────────────

    def _save_to_file(self) -> None:
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump([h.to_dict() for h in self.hobbies], f, indent=2, ensure_ascii=False)
