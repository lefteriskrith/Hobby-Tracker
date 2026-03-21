# Hobby Tracker

A modern, polished application to track your hobbies and keep them organized over time.

## Features

- 🗓️ **Interactive Calendar Picker** - Select start dates with an easy-to-use calendar widget
- 📊 **Clean Overview** - View all saved hobbies in a simple preview
- 🎨 **Modern UI** - Beautiful, polished interface with smooth interactions
- ⚡ **Fast & Responsive** - Lightweight application with instant calculations
- 📝 **Clean Codebase** - Well-organized, maintainable code structure

## Project Structure

```
hobby-tracker/
├── main.py              # Entry point - run this to start the app
├── config.py            # Configuration, messages, colors, and fonts
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── gui/                 # User interface components
│   ├── __init__.py
│   ├── main_window.py   # Main application window
│   └── widgets.py       # Custom widgets (DatePicker, FormField, Calendar)
└── logic/               # Data persistence
    ├── __init__.py
    └── data_manager.py  # Hobby loading and saving
```

## How to Use

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Enter hobby details:**
   - Enter the name of your hobby (e.g., "Guitar", "Gym", "Running")
   - Click "📅 Select Date" to pick your start date using the calendar
   - Optionally add an end date and comments

3. **Manage your list:**
   - Click "✅ Add new hobby" to save it
   - Open "📊 View All Hobbies" to see every saved hobby
   - Use the action buttons to edit or delete entries

4. **Clear fields:**
   - Click "Clear" to reset all fields and try again

## Features in Detail

### Calendar Date Picker
- No manual date typing needed - just click the button and select from a calendar
- Navigate months easily with arrow buttons
- Current day is highlighted
- Cannot select future dates

### Hobby Overview
- **Start Date**: When you began the hobby
- **End Date**: When you stopped it, if applicable
- **Duration**: Years, months, and days between start and end/today
- **Comments**: Optional notes for each hobby

### User Interface
- **Clean Design**: Minimalist interface with warm, pleasant colors
- **Responsive Layout**: Adapts to the window size
- **Owner Attribution**: "LefterisKr" credited at the bottom
- **Professional Polish**: Modern fonts and smooth interactions

## Technologies

- **Python 3.x**
- **tkinter** - Built-in Python GUI framework
- Standard library modules: `datetime`, `calendar`, `dataclasses`, `json`, `pathlib`

## Code Architecture

### Separation of Concerns
- **config.py**: All configuration in one place (messages, colors, fonts)
- **logic/data_manager.py**: Data model and JSON persistence
- **gui/main_window.py**: Main window and application flow
- **gui/widgets.py**: Reusable UI components

### Benefits
- ✅ Easy to maintain and update
- ✅ Simple to add new features
- ✅ Logic can be tested independently
- ✅ UI is separated from business logic
- ✅ Easy to reuse widgets in other projects

## Future Enhancements

- Save hobby data to a file or database
- View historical data with graphs
- Set goals and track progress toward them
- Export statistics as reports
- Dark mode theme option
- Multiple hobby tracking simultaneously

## License

Created for hobby tracking and personal use.

---

**Developed by**: LefterisKr
