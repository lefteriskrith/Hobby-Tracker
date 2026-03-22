"""Custom GUI widgets for Hobby Tracker."""

import tkinter as tk
from datetime import datetime, date
from config import COLORS, FONTS


class DateInputField(tk.Frame):
    """A date field with both manual entry and calendar picker."""
    
    def __init__(self, parent, label_text="When did you start?", **kwargs):
        super().__init__(parent, bg=COLORS["bg_main"], **kwargs)
        
        tk.Label(
            self,
            text=label_text,
            font=FONTS["label"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w")
        
        # Container for entry and button
        input_frame = tk.Frame(self, bg=COLORS["bg_main"])
        input_frame.pack(fill="x", pady=(6, 4))
        
        # Entry field for manual date input
        self.entry = tk.Entry(
            input_frame,
            font=FONTS["normal"],
            bg=COLORS["bg_light"],
            fg=COLORS["text_primary"],
            relief="solid",
            bd=1,
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.entry.insert(0, "YYYY-MM-DD")
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        
        # Calendar picker button
        self.date_picker = DatePickerButton(
            input_frame,
            on_date_selected=self._on_date_selected,
            width=12
        )
        self.date_picker.pack(side="right")
        
        self.selected_date = None
    
    def _on_focus_in(self, event):
        """Clear placeholder on focus."""
        if self.entry.get() == "YYYY-MM-DD":
            self.entry.delete(0, tk.END)
            self.entry.config(fg=COLORS["text_primary"])
    
    def _on_focus_out(self, event):
        """Show placeholder if empty."""
        if not self.entry.get():
            self.entry.insert(0, "YYYY-MM-DD")
            self.entry.config(fg=COLORS["text_hint"])
    
    def _on_date_selected(self, selected_date):
        """Handle date selection from picker."""
        self.selected_date = selected_date
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected_date.strftime("%Y-%m-%d"))
        self.entry.config(fg=COLORS["text_primary"])
    
    def get_date(self):
        """Get the selected date."""
        from datetime import datetime
        text = self.entry.get().strip()
        
        # If date was selected from picker
        if self.selected_date:
            return self.selected_date
        
        # Try to parse manual entry
        if text and text != "YYYY-MM-DD":
            try:
                return datetime.strptime(text, "%Y-%m-%d").date()
            except ValueError:
                return None
        
        return None
    
    def clear(self):
        """Clear the field."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "YYYY-MM-DD")
        self.entry.config(fg=COLORS["text_hint"])
        self.selected_date = None


class DatePickerButton(tk.Button):
    """A button that opens a date picker calendar."""
    
    def __init__(self, parent, on_date_selected=None, **kwargs):
        self.selected_date = None
        self.on_date_selected = on_date_selected
        
        super().__init__(
            parent,
            text="📅 Select Date",
            font=FONTS["normal"],
            bg=COLORS["button_secondary"],
            fg=COLORS["text_primary"],
            activebackground=COLORS["button_secondary_hover"],
            activeforeground=COLORS["text_primary"],
            relief="flat",
            pady=6,
            command=self._open_calendar,
            **kwargs
        )
    
    def _open_calendar(self):
        """Open a calendar window for date selection."""
        calendar_window = tk.Toplevel(self.master)
        calendar_window.title("Select Date")
        calendar_window.resizable(True, True)
        calendar_window.grab_set()
        
        # Give the calendar enough room for all 6 possible week rows.
        calendar_window.minsize(420, 360)
        calendar_window.geometry("460x420+360+220")
        
        CalendarWidget(calendar_window, on_date_selected=self._on_date_selected)
    
    def _on_date_selected(self, selected_date):
        """Called when a date is selected from the calendar."""
        self.selected_date = selected_date
        self.config(text=f"📅 {selected_date.strftime('%B %d, %Y')}")
        if self.on_date_selected:
            self.on_date_selected(selected_date)
    
    def get_date(self):
        """Return the selected date."""
        return self.selected_date


class CalendarWidget(tk.Frame):
    """A simple calendar widget for date selection."""
    
    MONTHS = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    def __init__(self, parent, on_date_selected=None, **kwargs):
        super().__init__(parent, bg=COLORS["bg_main"], **kwargs)
        self.on_date_selected = on_date_selected
        self.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.current_date = date.today()
        self.display_month = self.current_date.month
        self.display_year = self.current_date.year
        
        self._build_calendar()
    
    def _build_calendar(self):
        """Build the calendar interface."""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header with month/year selector
        header = tk.Frame(self, bg=COLORS["bg_main"])
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        tk.Button(
            header,
            text="◀",
            command=self._prev_month,
            font=FONTS["label"],
            bg=COLORS["button_secondary"],
            fg=COLORS["text_primary"],
            relief="flat",
            width=3,
        ).pack(side="left")
        
        # Month selector
        month_frame = tk.Frame(header, bg=COLORS["bg_main"])
        month_frame.pack(side="left", expand=True, fill="x", padx=10)
        
        self.month_combo = tk.StringVar(value=self.MONTHS[self.display_month - 1])
        month_dropdown = tk.OptionMenu(
            month_frame,
            self.month_combo,
            *self.MONTHS,
            command=self._on_month_change
        )
        month_dropdown.config(
            font=FONTS["normal"],
            bg=COLORS["bg_light"],
            fg=COLORS["text_primary"],
            relief="flat",
            pady=2,
        )
        month_dropdown.pack(side="left", padx=(0, 10))
        
        # Year selector
        years = list(range(1950, self.display_year + 11))
        self.year_combo = tk.StringVar(value=str(self.display_year))
        year_dropdown = tk.OptionMenu(
            month_frame,
            self.year_combo,
            *years,
            command=self._on_year_change
        )
        year_dropdown.config(
            font=FONTS["normal"],
            bg=COLORS["bg_light"],
            fg=COLORS["text_primary"],
            relief="flat",
            pady=2,
        )
        year_dropdown.pack(side="left")
        
        tk.Button(
            header,
            text="▶",
            command=self._next_month,
            font=FONTS["label"],
            bg=COLORS["button_secondary"],
            fg=COLORS["text_primary"],
            relief="flat",
            width=3,
        ).pack(side="right")
        
        # Calendar grid
        self.calendar_frame = tk.Frame(self, bg=COLORS["bg_main"])
        self.calendar_frame.grid(row=1, column=0, sticky="nsew")
        
        self._render_calendar()
    
    def _render_calendar(self):
        """Render the calendar for the current month."""
        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        for col in range(7):
            self.calendar_frame.grid_columnconfigure(col, weight=1, uniform="calendar_col")
        for row in range(7):
            self.calendar_frame.grid_rowconfigure(row, weight=1, uniform="calendar_row")
        
        # Day headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for day in days:
            tk.Label(
                self.calendar_frame,
                text=day,
                font=FONTS["hint"],
                bg=COLORS["bg_light"],
                fg=COLORS["text_secondary"],
                padx=5,
                pady=6,
            ).grid(row=0, column=days.index(day), sticky="ew", padx=2, pady=2)
        
        # Get first day of month and number of days
        import calendar
        first_day, num_days = calendar.monthrange(self.display_year, self.display_month)
        
        row = 1
        col = first_day
        
        for day in range(1, num_days + 1):
            btn = tk.Button(
                self.calendar_frame,
                text=str(day),
                font=FONTS["normal"],
                bg=COLORS["bg_light"] if day != self.current_date.day or 
                    self.display_month != self.current_date.month or
                    self.display_year != self.current_date.year else COLORS["button_accent"],
                fg=COLORS["text_primary"],
                activebackground=COLORS["bg_hover"] if day != self.current_date.day or
                    self.display_month != self.current_date.month or
                    self.display_year != self.current_date.year else COLORS["button_accent_hover"],
                activeforeground=COLORS["text_primary"],
                relief="flat",
                padx=5,
                pady=8,
                command=lambda d=day: self._select_date(d),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            
            col += 1
            if col > 6:
                col = 0
                row += 1
    
    def _select_date(self, day):
        """Handle date selection."""
        selected = date(self.display_year, self.display_month, day)
        if self.on_date_selected:
            self.on_date_selected(selected)
        self.winfo_toplevel().destroy()
    
    def _prev_month(self):
        """Go to previous month."""
        if self.display_month == 1:
            self.display_month = 12
            self.display_year -= 1
        else:
            self.display_month -= 1
        self._update_calendar_display()
    
    def _next_month(self):
        """Go to next month."""
        if self.display_month == 12:
            self.display_month = 1
            self.display_year += 1
        else:
            self.display_month += 1
        self._update_calendar_display()
    
    def _on_month_change(self, month_name):
        """Handle month dropdown change."""
        self.display_month = self.MONTHS.index(month_name) + 1
        self._update_calendar_display()
    
    def _on_year_change(self, year_str):
        """Handle year dropdown change."""
        self.display_year = int(year_str)
        self._update_calendar_display()
    
    def _update_calendar_display(self):
        """Update calendar display after month/year change."""
        self.month_combo.set(self.MONTHS[self.display_month - 1])
        self.year_combo.set(str(self.display_year))
        self._render_calendar()


class FormField(tk.Frame):
    """A form field with label, input, and hint."""
    
    def __init__(self, parent, label_text, hint_text="", is_multiline=False, **kwargs):
        super().__init__(parent, bg=COLORS["bg_main"], **kwargs)
        
        tk.Label(
            self,
            text=label_text,
            font=FONTS["label"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w")
        
        if is_multiline:
            self.entry = tk.Text(
                self,
                font=FONTS["normal"],
                bg=COLORS["bg_light"],
                fg=COLORS["text_primary"],
                relief="solid",
                bd=1,
                insertbackground=COLORS["text_primary"],
                height=2,
            )
        else:
            self.entry = tk.Entry(
                self,
                font=FONTS["normal"],
                bg=COLORS["bg_light"],
                fg=COLORS["text_primary"],
                relief="solid",
                bd=1,
                insertbackground=COLORS["text_primary"],
            )
        
        self.entry.pack(fill="x", pady=(6, 4))
        
        if hint_text:
            tk.Label(
                self,
                text=hint_text,
                font=FONTS["hint"],
                bg=COLORS["bg_main"],
                fg=COLORS["text_hint"],
            ).pack(anchor="w")
    
    def get(self):
        """Get the field value."""
        return self.entry.get()
    
    def set(self, value):
        """Set the field value."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def clear(self):
        """Clear the field."""
        if isinstance(self.entry, tk.Text):
            self.entry.delete("1.0", tk.END)
        else:
            self.entry.delete(0, tk.END)


class PreviewWindow:
    """A window to preview all saved hobbies as a table-like grid."""
    
    COLUMN_WIDTHS = (5, 28, 18, 16, 18)
    
    def __init__(self, hobbies, on_edit_callback=None, on_delete_callback=None):
        self.hobbies = hobbies
        self.on_edit_callback = on_edit_callback
        self.on_delete_callback = on_delete_callback
        self.sort_column = None
        self.sort_descending = False
        self.sortable_headers = {}
        self.rows_frame = None
        self.window = tk.Toplevel()
        self.window.title("All Hobbies Preview")
        self.window.geometry("900x600")
        self.window.configure(bg=COLORS["bg_main"])
        
        self._build_preview()
    
    def _build_preview(self):
        """Build the preview window with table-like layout."""
        # Header
        header = tk.Frame(self.window, bg=COLORS["button_primary"])
        header.pack(fill="x", padx=0, pady=0)
        
        tk.Label(
            header,
            text="📊 All Your Hobbies",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS["button_primary"],
            fg="white",
        ).pack(anchor="w", padx=20, pady=15)
        
        # Table header
        table_header = tk.Frame(self.window, bg=COLORS["bg_accent"])
        table_header.pack(fill="x", padx=(9, 15), pady=(15, 5))
        
        headers = ["", "Hobby Name", "Started", "Duration", "Actions"]
        
        for col_index, (header_text, width) in enumerate(zip(headers, self.COLUMN_WIDTHS)):
            table_header.grid_columnconfigure(col_index, weight=0)
            header_padx = 4
            if col_index == 0:
                header_padx = (8, 2)
            elif col_index == 1:
                header_padx = (0, 8)
            sort_key = None
            if header_text == "Hobby Name":
                sort_key = "name"
            elif header_text == "Started":
                sort_key = "started"
            elif header_text == "Duration":
                sort_key = "duration"

            if sort_key:
                btn = tk.Button(
                    table_header,
                    text=header_text,
                    command=lambda key=sort_key: self._sort_by(key),
                    font=("Segoe UI", 10, "bold"),
                    bg=COLORS["bg_accent"],
                    fg=COLORS["text_primary"],
                    activebackground=COLORS["bg_hover"],
                    activeforeground=COLORS["text_primary"],
                    relief="flat",
                    bd=0,
                    width=width,
                    cursor="hand2",
                    anchor="w" if col_index in {1, 2, 3} else "center",
                )
                btn.grid(row=0, column=col_index, padx=header_padx, pady=8, ipady=5, sticky="nsew")
                self.sortable_headers[sort_key] = btn
            else:
                tk.Label(
                    table_header,
                    text=header_text,
                    font=("Segoe UI", 10, "bold"),
                    bg=COLORS["bg_accent"],
                    fg=COLORS["text_primary"],
                    width=width,
                    anchor="w" if col_index in {1, 2, 3} else "center",
                ).grid(row=0, column=col_index, padx=header_padx, pady=8, ipady=5, sticky="nsew")
        
        # Scrollable frame for hobbies
        canvas_frame = tk.Frame(self.window, bg=COLORS["bg_main"])
        canvas_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        canvas = tk.Canvas(
            canvas_frame,
            bg=COLORS["bg_main"],
            highlightthickness=0,
        )
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg_main"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _sync_scrollable_width(event):
            canvas.itemconfigure(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", _sync_scrollable_width)
        
        self.rows_frame = scrollable_frame
        self._render_hobby_rows()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _render_hobby_rows(self):
        """Render hobby rows using the current sort order."""
        for widget in self.rows_frame.winfo_children():
            widget.destroy()

        sorted_hobbies = self._get_sorted_hobbies()

        if sorted_hobbies:
            for i, hobby in enumerate(sorted_hobbies):
                self._create_hobby_row(self.rows_frame, hobby, i % 2 == 0)
            return

        tk.Label(
            self.rows_frame,
            text="No hobbies yet. Add one to get started!",
            font=("Segoe UI", 12),
            bg=COLORS["bg_main"],
            fg=COLORS["text_secondary"],
        ).pack(pady=30)

    def _get_sorted_hobbies(self):
        """Return hobbies ordered by the active sort column."""
        hobbies = list(self.hobbies)

        if self.sort_column == "name":
            return sorted(
                hobbies,
                key=lambda hobby: hobby.name.lower(),
                reverse=self.sort_descending,
            )

        if self.sort_column == "started":
            return sorted(
                hobbies,
                key=self._get_started_sort_value,
                reverse=self.sort_descending,
            )

        if self.sort_column == "duration":
            return sorted(
                hobbies,
                key=self._get_duration_days,
                reverse=self.sort_descending,
            )

        return hobbies

    def _sort_by(self, column):
        """Toggle sorting for a specific column and refresh the table."""
        if self.sort_column == column:
            self.sort_descending = not self.sort_descending
        else:
            self.sort_column = column
            self.sort_descending = column in {"started", "duration"}

        self._update_header_labels()
        self._render_hobby_rows()

    def _update_header_labels(self):
        """Refresh sort arrows in clickable headers."""
        for column, button in self.sortable_headers.items():
            label_map = {
                "name": "Hobby Name",
                "started": "Started",
                "duration": "Duration",
            }
            label = label_map[column]
            if column == self.sort_column:
                arrow = "▼" if self.sort_descending else "▲"
                label = f"{label} {arrow}"
            button.config(text=label)

    def _get_started_sort_value(self, hobby):
        """Return the hobby start date for sorting."""
        try:
            return datetime.strptime(hobby.start_date, "%Y-%m-%d").date()
        except Exception:
            return date.min

    def _get_duration_days(self, hobby):
        """Calculate total duration in days for sorting."""
        try:
            start_date_obj = datetime.strptime(hobby.start_date, "%Y-%m-%d").date()
            end_date_raw = getattr(hobby, "end_date", "")
            end_date_obj = (
                datetime.strptime(end_date_raw, "%Y-%m-%d").date()
                if end_date_raw else date.today()
            )
            return max((end_date_obj - start_date_obj).days, 0)
        except Exception:
            return -1
    
    def _create_hobby_row(self, parent, hobby, alternate_bg):
        """Create an expandable row for a single hobby in table format."""
        bg_color = COLORS["bg_light"] if alternate_bg else COLORS["bg_secondary"]
        
        # Container for row + expandable details
        container = tk.Frame(parent, bg=bg_color)
        container.pack(fill="x", pady=2, padx=0)
        
        # Parse dates
        start_date_obj = datetime.strptime(hobby.start_date, "%Y-%m-%d").date()
        
        # Calculate duration only
        try:
            total_days = self._get_duration_days(hobby)
            years = total_days // 365
            remaining_days = total_days % 365
            months = remaining_days // 30
            days = remaining_days % 30
            duration = f"{years}y {months}mo {days}d"
        except Exception:
            duration = "N/A"
        
        # Main row (no expand toggle, plain aligned table)
        row = tk.Frame(container, bg=bg_color, relief="solid", bd=1)
        row.pack(fill="x", padx=0, pady=0)
        
        for col_index in range(5):
            row.grid_columnconfigure(col_index, weight=0, minsize=self.COLUMN_WIDTHS[col_index] * 8)

        details_frame = tk.Frame(container, bg=COLORS["bg_accent"], relief="solid", bd=1)

        toggle_text = tk.StringVar(value="▶")

        def _toggle_details():
            if details_frame.winfo_ismapped():
                details_frame.pack_forget()
                toggle_text.set("▶")
            else:
                details_frame.pack(fill="x", padx=18, pady=(0, 4))
                toggle_text.set("▼")

        toggle_btn = tk.Button(
            row,
            textvariable=toggle_text,
            command=_toggle_details,
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["button_secondary"],
            fg=COLORS["text_primary"],
            activebackground=COLORS["button_secondary_hover"],
            activeforeground=COLORS["text_primary"],
            relief="flat",
            bd=0,
            width=2,
            padx=0,
            pady=2,
            cursor="hand2",
        )
        toggle_btn.grid(row=0, column=0, padx=(8, 2), pady=8, sticky="w")

        name_label = tk.Label(
            row,
            text=hobby.name,
            font=("Segoe UI", 10, "bold"),
            bg=bg_color,
            fg=COLORS["text_primary"],
            anchor="w",
            width=self.COLUMN_WIDTHS[1],
        )
        name_label.grid(row=0, column=1, padx=(0, 12), pady=8, ipady=3, sticky="w")
        
        # Started date
        started_text = start_date_obj.strftime("%b %d, %Y")
        started_label = tk.Label(
            row,
            text=started_text,
            font=("Segoe UI", 9),
            bg=bg_color,
            fg=COLORS["text_secondary"],
            width=self.COLUMN_WIDTHS[2],
            anchor="w",
        )
        started_label.grid(row=0, column=2, padx=(4, 14), pady=8, ipady=3, sticky="w")
        
        # Duration
        duration_label = tk.Label(
            row,
            text=duration,
            font=("Segoe UI", 9),
            bg=bg_color,
            fg=COLORS["text_secondary"],
            width=self.COLUMN_WIDTHS[3],
            anchor="w",
        )
        duration_label.grid(row=0, column=3, padx=(4, 10), pady=8, ipady=3, sticky="w")
        
        # Action buttons centered inside a fixed-width cell
        action_cell = tk.Frame(row, bg=bg_color, width=self.COLUMN_WIDTHS[4] * 8)
        action_cell.grid(row=0, column=4, padx=(4, 8), pady=8, sticky="nsew")
        action_cell.grid_propagate(False)

        action_frame = tk.Frame(action_cell, bg=bg_color)
        action_frame.place(relx=0.5, rely=0.5, anchor="center")

        if self.on_edit_callback:
            edit_btn = tk.Button(
                action_frame,
                text="Edit",
                command=lambda h=hobby: self.on_edit_callback(h),
                font=("Segoe UI", 8, "bold"),
                bg=COLORS["button_accent"],
                fg="white",
                activebackground=COLORS["button_accent_hover"],
                relief="raised",
                bd=1,
                width=7,
                height=1,
                padx=2,
                pady=2,
                cursor="hand2",
            )
            edit_btn.pack(side="left", padx=(0, 6))

        if self.on_delete_callback:
            delete_btn = tk.Button(
                action_frame,
                text="Delete",
                command=lambda h=hobby: self.on_delete_callback(h),
                font=("Segoe UI", 8, "bold"),
                bg="#e85d75",
                fg="white",
                activebackground="#d94a63",
                relief="raised",
                bd=1,
                width=7,
                height=1,
                padx=2,
                pady=2,
                cursor="hand2",
            )
            delete_btn.pack(side="left")

        self._build_hobby_details(details_frame, hobby, start_date_obj, duration)

    def _build_hobby_details(self, parent, hobby, start_date_obj, duration):
        """Build the expandable details section for a hobby."""
        started_value = start_date_obj.strftime("%b %d, %Y")
        ended_value = "Still active"

        if getattr(hobby, "end_date", ""):
            try:
                ended_value = datetime.strptime(hobby.end_date, "%Y-%m-%d").strftime("%b %d, %Y")
            except ValueError:
                ended_value = hobby.end_date

        comments_value = getattr(hobby, "comments", "").strip() or "No comments"

        details_text = (
            f"Started: {started_value}\n"
            f"Ended: {ended_value}\n"
            f"Duration: {duration}\n"
            f"Comments: {comments_value}"
        )

        tk.Label(
            parent,
            text=details_text,
            font=("Segoe UI", 9),
            bg=COLORS["bg_accent"],
            fg=COLORS["text_primary"],
            justify="left",
            anchor="w",
            padx=12,
            pady=10,
        ).pack(fill="x")

    

        

