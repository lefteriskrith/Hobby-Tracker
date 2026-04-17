# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
python main.py
```

No dependencies to install — the app uses only Python's standard library (tkinter, json, datetime, pathlib).

To build a standalone executable:
```bash
pyinstaller HobbyTracker.spec
```

## Architecture

The app follows a modular MVC-like structure:

- **`config.py`** — Single source of truth for all colors, fonts, sizes, and UI strings. Always update here, never inline.
- **`logic/data_manager.py`** — `DataManager` handles JSON persistence; `Hobby` is a dataclass with `to_dict`/`from_dict` for serialization. The data file path resolves differently for source vs. PyInstaller frozen builds.
- **`gui/main_window.py`** — `HobbyTrackerApp` owns the main window, form state, and edit mode (`_edit_old_name` tracks whether a save is an add or update).
- **`gui/widgets.py`** — Reusable components: `FormField`, `DateInputField` (manual entry + calendar picker), `CalendarWidget` (built from scratch, no external date library), `PreviewWindow` (sortable, scrollable table with expandable rows).

## Key Patterns

- **Edit mode**: `_edit_old_name` on `HobbyTrackerApp` distinguishes add vs. update. Set when editing, cleared after save/clear.
- **Scrollable canvas pattern**: `PreviewWindow` uses `tk.Canvas` + `tk.Scrollbar` + inner `tk.Frame`, with a `<Configure>` binding to sync width.
- **Sorting**: `PreviewWindow` tracks `sort_column` and `sort_descending`; `_sort_by()` toggles direction on re-click.
- **Data reload**: `data_manager.reload_hobbies()` is called before opening `PreviewWindow` to ensure fresh data.
- **Forward-compatible deserialization**: `Hobby.from_dict` filters unknown keys so older JSON files load without error.

## Design System

All visual constants live in `config.py` under `COLORS` and `FONTS`. The theme is dark (`#0b0d12` base) with a warm orange primary (`#ff7a2f`), blue accent (`#4d7ef0`), and Segoe UI typography. Use `relief="flat"` for all buttons.
