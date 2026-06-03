import tkinter as tk


class AnimatedCalculator:
    """A dark-themed animated calculator built with Tkinter."""

    OPERATORS = {"÷", "×", "−", "+"}

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.geometry("340x580")
        self.window.configure(bg="#1a1a2e")
        self.window.resizable(False, False)

        self.expression = ""
        self.just_evaluated = False
        self.display_var = tk.StringVar(value="0")
        self.expr_var = tk.StringVar(value="")

        self._setup_ui()

    # ──────────────────────────────── UI SETUP ────────────────────────────────

    def _setup_ui(self):
        # ── Display ────────────────────────────────────────────────────────────
        disp_frame = tk.Frame(self.window, bg="#1a1a2e")
        disp_frame.pack(fill=tk.X, padx=24, pady=(28, 6))

        # Small expression label (e.g. "12 + 5 =")
        tk.Label(
            disp_frame, textvariable=self.expr_var,
            font=("Helvetica", 13), bg="#1a1a2e", fg="#6868a0",
            anchor="e", justify="right"
        ).pack(fill=tk.X)

        # Large result / input label
        self.main_lbl = tk.Label(
            disp_frame, textvariable=self.display_var,
            font=("Helvetica", 50, "bold"),
            bg="#1a1a2e", fg="#ffffff",
            anchor="e", justify="right"
        )
        self.main_lbl.pack(fill=tk.X)

        # Separator line
        tk.Frame(self.window, bg="#2e2e55", height=1).pack(
            fill=tk.X, padx=20, pady=8
        )

        # ── Button grid ────────────────────────────────────────────────────────
        grid = tk.Frame(self.window, bg="#1a1a2e")
        grid.pack(fill=tk.BOTH, expand=True, padx=14, pady=(4, 14))

        # (label, normal_bg, pressed_bg)
        layout = [
            [("C",  "#e74c3c","#c0392b"), ("±", "#3d3d5c","#555580"),
             ("%",  "#3d3d5c","#555580"), ("÷", "#e8820c","#c66a00")],
            [("7",  "#252542","#3a3a60"), ("8", "#252542","#3a3a60"),
             ("9",  "#252542","#3a3a60"), ("×", "#e8820c","#c66a00")],
            [("4",  "#252542","#3a3a60"), ("5", "#252542","#3a3a60"),
             ("6",  "#252542","#3a3a60"), ("−", "#e8820c","#c66a00")],
            [("1",  "#252542","#3a3a60"), ("2", "#252542","#3a3a60"),
             ("3",  "#252542","#3a3a60"), ("+", "#e8820c","#c66a00")],
            [("0",  "#252542","#3a3a60"), (".", "#252542","#3a3a60"),
             ("⌫", "#3d3d5c","#555580"), ("=", "#2ecc71","#27ae60")],
        ]

        for r, row in enumerate(layout):
            grid.rowconfigure(r, weight=1, minsize=72)
            for c, (lbl, norm, press) in enumerate(row):
                grid.columnconfigure(c, weight=1)
                btn = tk.Button(
                    grid, text=lbl,
                    font=("Helvetica", 22, "bold"),
                    bg=norm, fg="#ffffff",
                    activebackground=press,
                    activeforeground="#ffffff",
                    bd=0, relief=tk.FLAT, cursor="hand2",
                    command=lambda l=lbl: self._on_click(l)
                )
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                self._bind_animation(btn, norm, press)

    # ──────────────────────────── BUTTON ANIMATIONS ───────────────────────────

    @staticmethod
    def _lighten(hex_col, factor=0.18):
        """Return a slightly lighter shade of a hex colour."""
        h = hex_col.lstrip("#")
        r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
        return "#{:02x}{:02x}{:02x}".format(
            min(255, int(r + (255 - r) * factor)),
            min(255, int(g + (255 - g) * factor)),
            min(255, int(b + (255 - b) * factor)),
        )

    def _bind_animation(self, btn, norm, press):
        hover = self._lighten(norm)
        btn.bind("<Enter>",           lambda e: btn.configure(bg=hover))
        btn.bind("<Leave>",           lambda e: btn.configure(bg=norm))
        btn.bind("<ButtonPress-1>",   lambda e: btn.configure(bg=press, relief=tk.SUNKEN))
        btn.bind("<ButtonRelease-1>", lambda e: btn.configure(bg=norm,  relief=tk.FLAT))

    def _flash_result(self):
        """Brief green flash on the display to confirm evaluation."""
        self.main_lbl.configure(fg="#2ecc71")
        self.window.after(220, lambda: self.main_lbl.configure(fg="#ffffff"))

    # ────────────────────────────── BUTTON LOGIC ──────────────────────────────

    def _on_click(self, lbl):
        expr = self.expression

        # ── Clear ─────────────────────────────────────────────────────────────
        if lbl == "C":
            self.expression = ""
            self.display_var.set("0")
            self.expr_var.set("")
            self.just_evaluated = False

        # ── Backspace ─────────────────────────────────────────────────────────
        elif lbl == "⌫":
            if self.just_evaluated:
                self.expression = ""
                self.display_var.set("0")
                self.just_evaluated = False
            else:
                self.expression = expr[:-1]
                self.display_var.set(self.expression or "0")

        # ── Evaluate ──────────────────────────────────────────────────────────
        elif lbl == "=":
            if not expr:
                return
            try:
                # Replace display symbols with Python operators before eval
                py_expr = (
                    expr.replace("÷", "/")
                        .replace("×", "*")
                        .replace("−", "-")
                )
                result = eval(py_expr)          # safe: only button input possible
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.expr_var.set(expr + "  =")
                self.expression = str(result)
                self.display_var.set(self.expression)
                self.just_evaluated = True
                self._flash_result()
            except Exception:
                self.display_var.set("Error")
                self.expression = ""
                self.just_evaluated = False

        # ── Toggle sign ───────────────────────────────────────────────────────
        elif lbl == "±":
            if not expr or expr == "0":
                return
            if expr.startswith("−"):
                self.expression = expr[1:]
            else:
                self.expression = "−" + expr
            self.display_var.set(self.expression)

        # ── Percentage ────────────────────────────────────────────────────────
        elif lbl == "%":
            if not expr:
                return
            try:
                val = eval(expr.replace("÷","/").replace("×","*").replace("−","-"))
                result = val / 100
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.expression = str(result)
                self.display_var.set(self.expression)
            except Exception:
                pass

        # ── Digit / operator ──────────────────────────────────────────────────
        else:
            if self.just_evaluated:
                if lbl in self.OPERATORS:
                    # Chain: continue arithmetic with previous result
                    self.expr_var.set("")
                    self.expression += lbl
                    self.display_var.set(self.expression)
                else:
                    # Fresh number entry
                    self.expression = lbl
                    self.display_var.set(lbl)
                    self.expr_var.set("")
                self.just_evaluated = False
            else:
                self.expression += lbl
                self.display_var.set(self.expression)

    # ──────────────────────────────────────────────────────────────────────────

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = AnimatedCalculator()
    app.run()