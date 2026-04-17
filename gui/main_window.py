"""Main application window for Hobby Tracker."""

import tkinter as tk
from tkinter import messagebox
from datetime import date

from config import (
    APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, RESIZABLE, COLORS, FONTS,
    MESSAGES, OWNER
)
from logic import DataManager, Hobby
from gui.widgets import FormField, DateInputField, PreviewWindow


class HobbyTrackerApp:
    """Main application class for Hobby Tracker."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.resizable(RESIZABLE, RESIZABLE)
        self.root.configure(bg=COLORS["bg_main"])
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - WINDOW_WIDTH) // 2
        y = (sh - WINDOW_HEIGHT) // 2
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        self.data_manager = DataManager()
        self.date_field = None
        self.comments_field = None
        self._edit_old_name = None
        self.save_btn = None
        self._status_after_id = None

        self._build_ui()
        self._make_icon()
        self.root.bind("<Return>", lambda e: self.add_hobby())
        self.root.bind("<Escape>", lambda e: self.clear_all())
    
    def _build_ui(self):
        """Build the user interface."""
        # Top accent bar
        tk.Frame(self.root, bg=COLORS["button_primary"], height=3).pack(fill="x", side="top")

        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS["bg_main"], padx=24, pady=16)
        main_frame.pack(fill="both", expand=True)

        # Header with Preview button
        header_frame = tk.Frame(main_frame, bg=COLORS["bg_main"])
        header_frame.pack(fill="x", pady=(0, 0))

        left_frame = tk.Frame(header_frame, bg=COLORS["bg_main"])
        left_frame.pack(side="left", fill="both", expand=True)

        tk.Label(
            left_frame,
            text=MESSAGES["main_title"],
            font=FONTS["title"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w")

        tk.Label(
            left_frame,
            text=MESSAGES["subtitle"],
            font=FONTS["subtitle"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(3, 0))

        view_btn = tk.Button(
            header_frame,
            text="View All",
            command=self._show_preview,
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["button_accent"],
            fg="white",
            activebackground=COLORS["button_accent_hover"],
            activeforeground="white",
            relief="flat",
            padx=14,
            pady=7,
            cursor="hand2",
        )
        view_btn.pack(side="right", anchor="e")
        view_btn.bind("<Enter>", lambda e: view_btn.config(bg=COLORS["button_accent_hover"]))
        view_btn.bind("<Leave>", lambda e: view_btn.config(bg=COLORS["button_accent"]))

        # Thin divider under header
        tk.Frame(main_frame, bg=COLORS["border"], height=1).pack(fill="x", pady=(12, 0))

        # Content area
        content_frame = tk.Frame(main_frame, bg=COLORS["bg_main"])
        content_frame.pack(fill="both", expand=True, pady=(12, 0))
        
        self._build_form(content_frame)
        
        # Footer
        self._build_footer(main_frame)
    
    def _build_form(self, parent):
        """Build the form section."""
        # Hobby name field
        self.hobby_field = FormField(
            parent,
            MESSAGES["hobby_label"],
            MESSAGES["hobby_hint"],
        )
        self.hobby_field.pack(fill="x", pady=(0, 10))

        # Date input field (manual entry + picker)
        self.date_field = DateInputField(parent)
        self.date_field.pack(fill="x", pady=(0, 10))

        # End date field (optional - when hobby was stopped)
        self.end_date_field = DateInputField(parent, label_text="When did you stop? (optional)")
        self.end_date_field.pack(fill="x", pady=(0, 10))

        # Comments field
        self.comments_field = FormField(
            parent,
            "Comments (optional)",
            "Add any notes about this hobby",
            is_multiline=True,
        )
        self.comments_field.pack(fill="x", pady=(0, 10))

        # Thin divider before buttons
        tk.Frame(parent, bg=COLORS["border"], height=1).pack(fill="x", pady=(4, 0))

        # Buttons
        button_frame = tk.Frame(parent, bg=COLORS["bg_main"])
        button_frame.pack(fill="x", pady=(12, 8))
        
        self.save_btn = tk.Button(
            button_frame,
            text="Add Hobby",
            command=self.add_hobby,
            font=FONTS["label"],
            bg=COLORS["button_primary"],
            fg="white",
            activebackground=COLORS["button_primary_hover"],
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
        )
        self.save_btn.pack(side="left")
        self.save_btn.bind("<Enter>", lambda e: self.save_btn.config(bg=COLORS["button_primary_hover"]))
        self.save_btn.bind("<Leave>", lambda e: self.save_btn.config(bg=COLORS["button_primary"]))

        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_all,
            font=FONTS["normal"],
            bg=COLORS["button_secondary"],
            fg=COLORS["text_secondary"],
            activebackground=COLORS["button_secondary_hover"],
            activeforeground=COLORS["text_primary"],
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
        )
        clear_btn.pack(side="left", padx=(8, 0))
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg=COLORS["button_secondary_hover"]))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg=COLORS["button_secondary"]))
        
        # Status label
        self.status_label = tk.Label(
            parent,
            text=MESSAGES["result_hint"],
            font=FONTS["hint"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_hint"],
            anchor="w",
        )
        self.status_label.pack(fill="x", pady=(4, 0))
    
    def _build_footer(self, parent):
        """Build the footer section."""
        footer_frame = tk.Frame(parent, bg=COLORS["bg_main"])
        footer_frame.pack(fill="x", side="bottom", pady=(6, 0))

        tk.Label(
            footer_frame,
            text=f"© {OWNER}  ·  Press Enter to save  ·  Esc to clear",
            font=FONTS["small"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_hint"],
        ).pack(anchor="e")
    
    def add_hobby(self):
        """Add or update the hobby and clear."""
        hobby_name = self.hobby_field.get().strip()
        start_date = self.date_field.get_date()
        
        # Validation
        if not hobby_name:
            messagebox.showerror(MESSAGES["error_title"], MESSAGES["error_empty_hobby"])
            return
        
        if not start_date:
            messagebox.showerror(MESSAGES["error_title"], MESSAGES["error_invalid_date"])
            return
        
        # Get comments if provided
        comments = self.comments_field.entry.get("1.0", tk.END).strip()
        
        # Get end date if provided
        end_date = self.end_date_field.get_date()
        
        # Check if editing existing hobby
        old_name = getattr(self, '_edit_old_name', None)
        
        # Add hobby to data
        hobby = Hobby(
            name=hobby_name,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat() if end_date else "",
            added_date=date.today().isoformat(),
            comments=comments,
        )
        
        if old_name:
            self.data_manager.update_hobby(old_name, hobby)
            self._edit_old_name = None
            self._set_status(f"✓ Updated '{hobby_name}'", success=True)
        else:
            self.data_manager.save_hobby(hobby)
            self._set_status(f"✓ Added '{hobby_name}'", success=True)
        
        self.clear_all(skip_confirm=True)
    
    def _show_preview(self):
        """Show preview of all hobbies."""
        # Reload from disk each time, so preview always matches file (cwd-independent)
        self.data_manager.reload_hobbies()
        PreviewWindow(
            self.data_manager.get_all_hobbies(),
            on_edit_callback=self._edit_hobby,
            on_delete_callback=self._delete_hobby,
        )
    
    def _edit_hobby(self, hobby):
        """Edit an existing hobby."""
        self.hobby_field.set(hobby.name)
        # Parse the date and set it
        from datetime import datetime
        start_date = datetime.strptime(hobby.start_date, "%Y-%m-%d").date()
        self.date_field.selected_date = start_date
        self.date_field.entry.delete(0, tk.END)
        self.date_field.entry.insert(0, start_date.strftime("%Y-%m-%d"))
        
        # Set end date if available
        if hasattr(hobby, 'end_date') and hobby.end_date:
            end_date = datetime.strptime(hobby.end_date, "%Y-%m-%d").date()
            self.end_date_field.selected_date = end_date
            self.end_date_field.entry.delete(0, tk.END)
            self.end_date_field.entry.insert(0, end_date.strftime("%Y-%m-%d"))
        
        # Set comments
        if hasattr(hobby, 'comments'):
            self.comments_field.entry.delete("1.0", tk.END)
            self.comments_field.entry.insert("1.0", hobby.comments)
        self._edit_old_name = hobby.name
        self.save_btn.config(text="Save Changes")
        self._set_status(f"Editing '{hobby.name}' — press Enter or click Save Changes.")
    
    def _delete_hobby(self, hobby):
        """Delete a hobby."""
        if messagebox.askyesno("Confirm Delete", f"Delete '{hobby.name}' permanently?"):
            self.data_manager.delete_hobby(hobby.name)
            self._set_status(f"✓ Deleted '{hobby.name}'", success=True)
            self._show_preview()
    
    def clear_all(self, skip_confirm=False):
        """Clear all fields."""
        if not skip_confirm and self._is_form_dirty():
            if not messagebox.askyesno("Clear form", "Discard unsaved changes?"):
                return
        self.hobby_field.clear()
        self.date_field.clear()
        self.end_date_field.clear()
        self.comments_field.clear()
        self._set_status(MESSAGES["result_hint"])
        self._edit_old_name = None
        if self.save_btn:
            self.save_btn.config(text="Add Hobby")
    
    def _make_icon(self):
        img = tk.PhotoImage(width=16, height=16)
        orange = COLORS["button_primary"]
        for y in range(16):
            img.put("{" + " ".join([orange] * 16) + "}", to=(0, y))
        self.root.iconphoto(True, img)
        self._app_icon = img

    def _set_status(self, text, success=False):
        if self._status_after_id:
            self.root.after_cancel(self._status_after_id)
            self._status_after_id = None
        color = COLORS["accent_soft"] if success else COLORS["text_hint"]
        self.status_label.config(text=text, fg=color)
        if success:
            self._status_after_id = self.root.after(3500, self._fade_status)

    def _fade_status(self):
        self._status_after_id = None
        self.status_label.config(text=MESSAGES["result_hint"], fg=COLORS["text_hint"])

    def _is_form_dirty(self):
        has_name = bool(self.hobby_field.get().strip())
        has_date = self.date_field.get_date() is not None
        has_comments = bool(self.comments_field.entry.get("1.0", tk.END).strip())
        return has_name or has_date or has_comments

    def run(self):
        """Start the application."""
        self.root.mainloop()
