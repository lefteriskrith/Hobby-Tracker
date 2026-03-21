import tkinter as tk
from datetime import date, datetime
from tkinter import messagebox


class HobbyTrackerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Hobby Tracker")
        self.root.geometry("470x360")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5efe6")

        self.hobby_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.count_var = tk.StringVar()
        self.result_var = tk.StringVar(
            value="Vale to hobby sou, tin imerominia pou xekinises, kai posa fores to exeis kanei."
        )

        self._build_ui()

    def _build_ui(self) -> None:
        frame = tk.Frame(self.root, bg="#f5efe6", padx=22, pady=22)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Hobby Tracker",
            font=("Segoe UI", 16, "bold"),
            bg="#f5efe6",
            fg="#2f3b2f",
        ).pack(anchor="w")

        tk.Label(
            frame,
            text="Mathainei poso kairo kaneis ena hobby kai poses fores to exeis kanei.",
            font=("Segoe UI", 9),
            bg="#f5efe6",
            fg="#5f6b5f",
        ).pack(anchor="w", pady=(6, 18))

        self._field(frame, "Poio hobby exeis;", self.hobby_var, "p.x. gym, kithara, treksimo")
        self._field(frame, "Pote xekinises;", self.start_date_var, "μορφή: YYYY-MM-DD")
        self._field(frame, "Posa xompi exeis kanei mexri twra;", self.count_var, "p.x. 120")

        button_row = tk.Frame(frame, bg="#f5efe6")
        button_row.pack(fill="x", pady=(10, 14))

        tk.Button(
            button_row,
            text="Ypologismos",
            command=self.calculate,
            font=("Segoe UI", 10, "bold"),
            bg="#2f6f4f",
            fg="white",
            activebackground="#25573d",
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=9,
        ).pack(side="left")

        tk.Button(
            button_row,
            text="Katharisma",
            command=self.clear_all,
            font=("Segoe UI", 10),
            bg="#d8cbb8",
            fg="#2f3b2f",
            activebackground="#c7b7a2",
            activeforeground="#2f3b2f",
            relief="flat",
            padx=16,
            pady=9,
        ).pack(side="left", padx=(10, 0))

        result_box = tk.Label(
            frame,
            textvariable=self.result_var,
            justify="left",
            anchor="nw",
            wraplength=400,
            font=("Segoe UI", 10),
            bg="#fffaf2",
            fg="#283428",
            padx=14,
            pady=14,
            bd=1,
            relief="solid",
        )
        result_box.pack(fill="both", expand=True)

    def _field(self, parent: tk.Widget, label: str, variable: tk.StringVar, hint: str) -> None:
        wrapper = tk.Frame(parent, bg="#f5efe6")
        wrapper.pack(fill="x", pady=(0, 12))

        tk.Label(
            wrapper,
            text=label,
            font=("Segoe UI", 10, "bold"),
            bg="#f5efe6",
            fg="#2f3b2f",
        ).pack(anchor="w")

        tk.Entry(
            wrapper,
            textvariable=variable,
            font=("Segoe UI", 10),
            bg="white",
            fg="#1f2937",
            relief="solid",
            bd=1,
        ).pack(fill="x", pady=(6, 4))

        tk.Label(
            wrapper,
            text=hint,
            font=("Segoe UI", 8),
            bg="#f5efe6",
            fg="#7a847a",
        ).pack(anchor="w")

    def calculate(self) -> None:
        hobby_name = self.hobby_var.get().strip()
        start_date_text = self.start_date_var.get().strip()
        count_text = self.count_var.get().strip()

        if not hobby_name:
            messagebox.showerror("Lathos", "Grapse poio hobby exeis.")
            return

        try:
            start_date = datetime.strptime(start_date_text, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Lathos", "Vale tin imerominia se morfi YYYY-MM-DD.")
            return

        if start_date > date.today():
            messagebox.showerror("Lathos", "I imerominia den mporei na einai sto mellon.")
            return

        try:
            total_sessions = int(count_text)
        except ValueError:
            messagebox.showerror("Lathos", "Ta xompi prepei na einai arithmos.")
            return

        if total_sessions < 0:
            messagebox.showerror("Lathos", "Ta xompi den mporei na einai arnitika.")
            return

        today = date.today()
        total_days = (today - start_date).days
        years = total_days // 365
        remaining_days = total_days % 365
        months = remaining_days // 30
        days = remaining_days % 30

        if total_days == 0:
            average_text = "Xekinises simera, opote den yparxei akoma mesos oros ana mera."
        else:
            average_per_day = total_sessions / total_days
            average_per_week = total_sessions / max(total_days / 7, 1)
            average_text = (
                f"Mesos oros: {average_per_day:.2f} fores ana mera "
                f"kai {average_per_week:.2f} fores ana evdomada."
            )

        self.result_var.set(
            f"Exeis to hobby '{hobby_name}'.\n\n"
            f"To exeis kanei {total_sessions} fores.\n"
            f"To xekinises stis {start_date.isoformat()}.\n"
            f"To kaneis edo kai {years} xronia, {months} mines kai {days} meres.\n\n"
            f"{average_text}"
        )

    def clear_all(self) -> None:
        self.hobby_var.set("")
        self.start_date_var.set("")
        self.count_var.set("")
        self.result_var.set(
            value="Vale to hobby sou, tin imerominia pou xekinises, kai posa fores to exeis kanei."
        )

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    HobbyTrackerApp().run()
