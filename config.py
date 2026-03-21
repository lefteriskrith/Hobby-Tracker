# Configuration and Constants for Hobby Tracker

APP_TITLE = "Hobby Tracker"
APP_VERSION = "1.0.0"
OWNER = "LefterisKr"

# Window Configuration
WINDOW_WIDTH = 520
WINDOW_HEIGHT = 550
RESIZABLE = False

# Date Format
DATE_FORMAT = "%Y-%m-%d"
DATE_DISPLAY_FORMAT = "%B %d, %Y"

# UI Messages
MESSAGES = {
    "main_title": "Hobby Tracker",
    "subtitle": "Track your hobbies and keep them organized over time.",
    "hobby_label": "What hobby do you practice?",
    "hobby_hint": "e.g., gym, guitar, running",
    "start_date_label": "When did you start?",
    "start_date_button": "Select Date",
    "count_label": "Comments (optional)",
    "count_hint": "Add notes or details about this hobby",
    "calculate_button": "Calculate",
    "clear_button": "Clear",
    
    # Errors
    "error_title": "Error",
    "error_empty_hobby": "Please enter a hobby name.",
    "error_invalid_date": "Please select a valid date.",
    "error_future_date": "The date cannot be in the future.",
    
    # Results
    "result_hint": "Enter hobby details above and save your hobby.",
}

# Color Scheme - Dark, lively, and higher-contrast
COLORS = {
    "bg_main": "#0b0d12",
    "bg_light": "#131821",
    "bg_accent": "#1a2130",
    "bg_hover": "#212a3b",
    "bg_secondary": "#0f141c",
    
    "text_primary": "#f5f7fb",
    "text_secondary": "#c7d0dd",
    "text_hint": "#8e9aae",
    "text_light": "#eef2f8",
    
    "button_primary": "#ff7a2f",
    "button_primary_hover": "#eb6720",
    "button_primary_light": "#ff9a60",
    
    "button_secondary": "#252d3b",
    "button_secondary_hover": "#313b4d",
    
    "button_accent": "#4d7ef0",
    "button_accent_hover": "#3f6fe0",
    
    "accent_warm": "#f0a500",
    "accent_gold": "#ffc857",
    "accent_soft": "#69cfe6",
    
    "border": "#232b38",
    "border_light": "#313c4e",
    "shadow": "rgba(0,0,0,0.35)",
}

# Font Sizes
FONTS = {
    "title": ("Segoe UI", 16, "bold"),
    "subtitle": ("Segoe UI", 9),
    "label": ("Segoe UI", 10, "bold"),
    "normal": ("Segoe UI", 10),
    "hint": ("Segoe UI", 8),
    "small": ("Segoe UI", 8),
}
