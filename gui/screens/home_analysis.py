import tkinter as tk
from tkinter import ttk

def create_analysis_panels(self):
    right_frame = tk.Frame(self, bg="#121212")
    right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
    right_frame.columnconfigure((0, 1), weight=1)
    right_frame.rowconfigure((0, 1), weight=1)

    # Léxico
    lexical_frame = tk.LabelFrame(right_frame, text="Analizador Léxico", bg="#ccc")
    lexical_frame.configure(width=400, height=200)
    lexical_frame.grid_propagate(False)
    lexical_frame.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
    y_scroll = tk.Scrollbar(lexical_frame, orient="vertical")
    y_scroll.pack(side="right", fill="y")

    cols = ("LEXEMA", "TOKEN", "LINE", "COLUMN")
    self.lexical_table = ttk.Treeview(
        lexical_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set
    )
    y_scroll.config(command=self.lexical_table.yview)

    for col in cols:
        self.lexical_table.heading(col, text=col)
        self.lexical_table.column(col, anchor="center", stretch=True)

    self.lexical_table.pack(fill="both", expand=True)
    
    def adjust_columns(event):
        total_width = event.width
        widths = {
            "LEXEMA": int(total_width * 0.3),
            "TOKEN": int(total_width * 0.4),
            "LINE": int(total_width * 0.1),
            "COLUMN": int(total_width * 0.2),
        }
        for col in cols:
            self.lexical_table.column(col, width=widths[col])

    self.lexical_table.bind("<Configure>", adjust_columns)

    # Sintáctico
    syntax_frame = tk.LabelFrame(right_frame, text="Analizador Sintáctico", bg="#ccc")
    syntax_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)
    self.syntax_output = tk.Text(syntax_frame, bg="#1e1e1e", fg="white", state="disabled")
    self.syntax_output.pack(fill="both", expand=True)

    # Semántico
    semantic_frame = tk.LabelFrame(right_frame, text="Analizador Semántico", bg="#ccc")
    semantic_frame.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)
    self.semantic_output = tk.Text(semantic_frame, bg="#1e1e1e", fg="white", state="disabled")
    self.semantic_output.pack(fill="both", expand=True)
