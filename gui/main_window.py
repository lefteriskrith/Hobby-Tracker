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
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(RESIZABLE, RESIZABLE)
        self.root.configure(bg=COLORS["bg_main"])
        
        self.data_manager = DataManager()
        self.date_field = None
        self.comments_field = None
        self._edit_old_name = None
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the user interface."""
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS["bg_main"], padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Header with Preview button
        header_frame = tk.Frame(main_frame, bg=COLORS["bg_main"])
        header_frame.pack(fill="x", pady=(0, 15))
        
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
        ).pack(anchor="w", pady=(4, 0))
        
        # Preview button - PROMINENT
        tk.Button(
            header_frame,
            text="📊 View All Hobbies",
            command=self._show_preview,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["accent_warm"],
            fg="white",
            activebackground=COLORS["button_accent_hover"],
            relief="flat",
            padx=16,
            pady=8,
        ).pack(side="right", anchor="e")
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=COLORS["bg_main"])
        content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
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
        self.hobby_field.pack(fill="x", pady=(0, 12))
        
        # Date input field (manual entry + picker)
        self.date_field = DateInputField(parent)
        self.date_field.pack(fill="x", pady=(0, 12))
        
        # End date field (optional - when hobby was stopped)
        self.end_date_field = DateInputField(parent, label_text="When did you stop? (optional)")
        self.end_date_field.pack(fill="x", pady=(0, 12))
        
        # Comments field
        self.comments_field = FormField(
            parent,
            "Comments (optional)",
            "Add any notes about this hobby",
            is_multiline=True,
        )
        self.comments_field.pack(fill="x", pady=(0, 12))
        
        # Buttons
        button_frame = tk.Frame(parent, bg=COLORS["bg_main"])
        button_frame.pack(fill="x", pady=(10, 12))
        
        tk.Button(
            button_frame,
            text="✅ Add new hobby",
            command=self.add_hobby,
            font=FONTS["label"],
            bg=COLORS["button_primary"],
            fg="white",
            activebackground=COLORS["button_primary_hover"],
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
        ).pack(side="left")
        
        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_all,
            font=FONTS["normal"],
            bg=COLORS["button_secondary"],
            fg=COLORS["text_primary"],
            activebackground=COLORS["button_secondary_hover"],
            activeforeground=COLORS["text_primary"],
            relief="flat",
            padx=15,
            pady=8,
        ).pack(side="left", padx=(8, 0))
        
        # Result display
        self.result_text = tk.Text(
            parent,
            font=FONTS["normal"],
            bg=COLORS["bg_light"],
            fg=COLORS["text_light"],
            relief="solid",
            bd=1,
            height=4,
            wrap="word",
        )
        self.result_text.pack(fill="both", expand=True, pady=(0, 10))
        self.result_text.insert("1.0", MESSAGES["result_hint"])
        self.result_text.config(state="disabled")
    
    def _build_footer(self, parent):
        """Build the footer section."""
        footer_frame = tk.Frame(parent, bg=COLORS["bg_main"])
        footer_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
        tk.Label(
            footer_frame,
            text=f"© {OWNER}",
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
            messagebox.showinfo("Success", f"Updated '{hobby_name}'!")
            self._edit_old_name = None
        else:
            self.data_manager.save_hobby(hobby)
            messagebox.showinfo("Success", f"Added '{hobby_name}'!")
        
        self.clear_all()
    
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
        # Store the old name for update
        self._edit_old_name = hobby.name
        messagebox.showinfo("Edit Mode", f"Editing '{hobby.name}'. Click 'Add new hobby' to save changes.")
    
    def _delete_hobby(self, hobby):
        """Delete a hobby."""
        if messagebox.askyesno("Confirm Delete", f"Delete '{hobby.name}' permanently?"):
            self.data_manager.delete_hobby(hobby.name)
            messagebox.showinfo("Deleted", f"'{hobby.name}' has been deleted.")
            # Refresh preview
            self._show_preview()
    
    def clear_all(self):
        """Clear all fields."""
        self.hobby_field.clear()
        self.date_field.clear()
        self.end_date_field.clear()
        self.comments_field.clear()
        
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", MESSAGES["result_hint"])
        self.result_text.config(state="disabled")
        self._edit_old_name = None
    
    def run(self):
        """Start the application."""
        self.root.mainloop()
