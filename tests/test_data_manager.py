"""
Regression tests for Hobby dataclass and DataManager persistence layer.

Each test uses a fresh temporary JSON file so the real hobbies_data.json
is never touched.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from logic.data_manager import DataManager, Hobby


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_dm(tmp_path: Path) -> DataManager:
    """Return a DataManager wired to a temp file, bypassing __init__."""
    dm = DataManager.__new__(DataManager)
    dm.data_path = tmp_path / "hobbies.json"
    dm.hobbies = []
    return dm


def _hobby(name="Guitar", start="2020-01-01", end="", comments="") -> Hobby:
    return Hobby(name=name, start_date=start, end_date=end, comments=comments)


# ---------------------------------------------------------------------------
# Hobby dataclass
# ---------------------------------------------------------------------------

class TestHobby:
    def test_roundtrip(self):
        h = _hobby("Piano", "2021-03-15", comments="love it")
        assert Hobby.from_dict(h.to_dict()) == h

    def test_from_dict_ignores_unknown_keys(self):
        data = {"name": "Drums", "start_date": "2022-06-01", "ghost_field": "ignored"}
        h = Hobby.from_dict(data)
        assert h.name == "Drums"
        assert not hasattr(h, "ghost_field")

    def test_from_dict_fills_defaults(self):
        h = Hobby.from_dict({"name": "Running", "start_date": "2023-01-01"})
        assert h.end_date == ""
        assert h.comments == ""

    def test_to_dict_contains_all_fields(self):
        h = _hobby()
        d = h.to_dict()
        for field in ("name", "start_date", "end_date", "added_date", "comments"):
            assert field in d


# ---------------------------------------------------------------------------
# DataManager — CRUD
# ---------------------------------------------------------------------------

class TestDataManagerCRUD:
    def test_save_and_reload(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("Yoga"))
        dm.reload_hobbies()
        assert len(dm.hobbies) == 1
        assert dm.hobbies[0].name == "Yoga"

    def test_save_multiple(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("A"))
        dm.save_hobby(_hobby("B"))
        dm.save_hobby(_hobby("C"))
        assert len(dm.get_all_hobbies()) == 3

    def test_save_duplicate_upserts(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("Piano", "2020-01-01"))
        dm.save_hobby(_hobby("Piano", "2021-06-15"))  # same name → overwrite
        assert len(dm.hobbies) == 1
        assert dm.hobbies[0].start_date == "2021-06-15"

    def test_save_case_insensitive_dedup(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("piano"))
        dm.save_hobby(_hobby("Piano"))
        assert len(dm.hobbies) == 1

    def test_delete(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("Guitar"))
        dm.save_hobby(_hobby("Drums"))
        dm.delete_hobby("Guitar")
        names = [h.name for h in dm.hobbies]
        assert "Guitar" not in names
        assert "Drums" in names

    def test_delete_case_insensitive(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("Guitar"))
        dm.delete_hobby("GUITAR")
        assert dm.hobbies == []

    def test_delete_nonexistent_is_noop(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("Guitar"))
        dm.delete_hobby("Violin")
        assert len(dm.hobbies) == 1

    def test_update_name(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("Guitar"))
        dm.update_hobby("Guitar", _hobby("Electric Guitar"))
        assert dm.hobbies[0].name == "Electric Guitar"

    def test_update_persists(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("Guitar"))
        dm.update_hobby("Guitar", _hobby("Bass", "2019-05-20"))
        dm.reload_hobbies()
        assert dm.hobbies[0].name == "Bass"
        assert dm.hobbies[0].start_date == "2019-05-20"

    def test_update_nonexistent_is_noop(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("Guitar"))
        dm.update_hobby("Violin", _hobby("Violin"))  # should not crash
        assert len(dm.hobbies) == 1


# ---------------------------------------------------------------------------
# DataManager — persistence
# ---------------------------------------------------------------------------

class TestDataManagerPersistence:
    def test_saves_valid_json(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("Yoga"))
        raw = json.loads(dm.data_path.read_text(encoding="utf-8"))
        assert isinstance(raw, list)
        assert raw[0]["name"] == "Yoga"

    def test_load_missing_file_returns_empty(self, tmp_path):
        dm = _make_dm(tmp_path)
        # data_path doesn't exist yet
        assert dm._load_hobbies() == []

    def test_load_corrupted_json_returns_empty(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.data_path.write_text("not valid json {{", encoding="utf-8")
        assert dm._load_hobbies() == []

    def test_reload_picks_up_external_changes(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("A"))
        # Simulate an external write
        dm.data_path.write_text(
            json.dumps([{"name": "B", "start_date": "2023-01-01"}]),
            encoding="utf-8",
        )
        dm.reload_hobbies()
        assert dm.hobbies[0].name == "B"

    def test_unicode_hobby_name(self, tmp_path):
        dm = _make_dm(tmp_path)
        dm.save_hobby(_hobby("Ζωγραφική"))  # Greek characters
        dm.reload_hobbies()
        assert dm.hobbies[0].name == "Ζωγραφική"
