"""
Hobby Tracker Application

A simple tool to track hobbies and keep your entries organized over time.

Entry point: main.py
"""

from gui import HobbyTrackerApp


def main():
    """Launch the Hobby Tracker application."""
    app = HobbyTrackerApp()
    app.run()


if __name__ == "__main__":
    main()
