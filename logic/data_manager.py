"""Data persistence for hobbies."""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from dataclasses import fields


@dataclass
class Hobby:
    """Represents a hobby entry."""
    name: str
    start_date: str  # ISO format YYYY-MM-DD
    end_date: str = ""  # Optional: when hobby was stopped
    added_date: str = ""  # When it was added to the tracker
    comments: str = ""  # Optional comments about the hobby
    
    def to_dict(self):
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary while tolerating older saved fields."""
        allowed_fields = {field.name for field in fields(cls)}
        cleaned_data = {
            key: value for key, value in data.items()
            if key in allowed_fields
        }
        return cls(**cleaned_data)


class DataManager:
    """Manages hobby data persistence."""

    DATA_FILENAME = "hobbies_data.json"

    def __init__(self):
        self.data_path = self._resolve_data_path()
        self.hobbies = self._load_hobbies()

    def _resolve_data_path(self) -> Path:
        """Choose a writable JSON path for source and frozen builds."""
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent / self.DATA_FILENAME
        return Path(__file__).resolve().parent.parent / self.DATA_FILENAME

    def reload_hobbies(self):
        """Reload hobbies from disk."""
        self.hobbies = self._load_hobbies()
        return self.hobbies
    
    def _load_hobbies(self) -> list:
        """Load hobbies from file."""
        if self.data_path.exists():
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Hobby.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError):
                return []
        return []
    
    def save_hobby(self, hobby: Hobby) -> None:
        """Add and save a hobby."""
        # Check if hobby with same name already exists
        existing = next((h for h in self.hobbies if h.name.lower() == hobby.name.lower()), None)
        if existing:
            # Update existing hobby
            self.hobbies.remove(existing)
        
        self.hobbies.append(hobby)
        self._save_to_file()
    
    def get_all_hobbies(self) -> list:
        """Get all saved hobbies."""
        return self.hobbies
    
    def delete_hobby(self, hobby_name: str) -> None:
        """Delete a hobby by name."""
        self.hobbies = [h for h in self.hobbies if h.name.lower() != hobby_name.lower()]
        self._save_to_file()
    
    def update_hobby(self, old_name: str, hobby: Hobby) -> None:
        """Update an existing hobby."""
        for i, h in enumerate(self.hobbies):
            if h.name.lower() == old_name.lower():
                self.hobbies[i] = hobby
                self._save_to_file()
                return
    
    def _save_to_file(self) -> None:
        """Save hobbies to JSON file."""
        data = [hobby.to_dict() for hobby in self.hobbies]
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
