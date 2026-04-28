"""
Smoke tests — verify the app can be imported and core objects constructed
without errors.  No display / tkinter window is created here.
"""

from pathlib import Path


def test_import_config():
    import config
    assert hasattr(config, "COLORS")
    assert hasattr(config, "FONTS")
    assert hasattr(config, "MESSAGES")
    assert hasattr(config, "WINDOW_WIDTH")
    assert hasattr(config, "WINDOW_HEIGHT")


def test_colors_have_required_keys():
    from config import COLORS
    required = [
        "bg_main", "bg_light", "bg_accent",
        "text_primary", "text_secondary", "text_hint",
        "button_primary", "button_accent", "border",
    ]
    for key in required:
        assert key in COLORS, f"Missing COLORS key: {key}"


def test_messages_have_required_keys():
    from config import MESSAGES
    required = [
        "main_title", "subtitle",
        "error_empty_hobby", "error_invalid_date",
        "result_hint",
    ]
    for key in required:
        assert key in MESSAGES, f"Missing MESSAGES key: {key}"


def test_import_logic():
    from logic.data_manager import DataManager, Hobby
    assert DataManager is not None
    assert Hobby is not None


def test_import_gui_modules():
    # Importing the module must not raise even without a running Tk instance.
    import gui
    from gui import HobbyTrackerApp
    assert HobbyTrackerApp is not None


def test_hobby_creation_defaults():
    from logic.data_manager import Hobby
    h = Hobby(name="Guitar", start_date="2024-01-15")
    assert h.name == "Guitar"
    assert h.start_date == "2024-01-15"
    assert h.end_date == ""
    assert h.added_date == ""
    assert h.comments == ""


def test_data_manager_no_file(tmp_path):
    from logic.data_manager import DataManager
    dm = DataManager.__new__(DataManager)
    dm.data_path = tmp_path / "hobbies.json"
    dm.hobbies = dm._load_hobbies()
    assert dm.hobbies == []


def test_data_file_path_is_resolvable():
    from logic.data_manager import DataManager
    dm = DataManager.__new__(DataManager)
    path = dm._resolve_data_path()
    # Must be a Path object pointing somewhere sensible.
    assert isinstance(path, Path)
    assert path.suffix == ".json"
