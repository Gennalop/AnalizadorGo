import tkinter as tk
from gui import style
from tkinter import ttk

def create_analysis_panels(self, r, c):
    right_frame = tk.Frame(self, bg=style.BACKGROUND)
    right_frame.grid(row=r, column=c, rowspan=3, sticky="nsew")
    right_frame.columnconfigure((0, 2), weight=1)
    right_frame.columnconfigure(0, minsize=250)
    right_frame.columnconfigure(1, minsize=style.PANELS_SPACE)
    right_frame.rowconfigure((0, 2), weight=1)
    right_frame.rowconfigure(1, minsize=style.PANELS_SPACE)

    # Léxico
    lexical_frame = tk.LabelFrame(right_frame, text="Analizador Léxico", bg=style.PANEL_HEADER_BG)
    lexical_frame.configure(width=400, height=200)
    lexical_frame.grid_propagate(False)
    lexical_frame.grid(row=0, column=0, sticky="nsew")
    y_scroll = tk.Scrollbar(lexical_frame, orient="vertical")
    y_scroll.pack(side="right", fill="y")

    style_lexical = ttk.Style()
    style_lexical.theme_use("default") 

    style_lexical.configure("Lexical.Treeview",
                            background=style.PANEL_BG,        # fondo de las celdas
                            fieldbackground=style.PANEL_BG,   # fondo general del widget
                            foreground="white",          # texto
                            rowheight=22)
    
    style_lexical.configure("Lexical.Treeview.Heading",
                            background=style.PANEL_BG,         # encabezado
                            foreground="white",
                            font=("Segoe UI", 8)
    )
    style_lexical.map("Lexical.Treeview", background=[("selected", style.PANEL_BG_T2)])

    cols = ("LEXEMA", "TOKEN", "LINE", "COL")
    self.lexical_table = ttk.Treeview(
        lexical_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        style="Lexical.Treeview"
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
            "TOKEN": int(total_width * 0.3),
            "LINE": int(total_width * 0.2),
            "COL": int(total_width * 0.2),
        }
        for c in cols:
            self.lexical_table.column(c, width=widths[c])

    self.lexical_table.bind("<Configure>", adjust_columns)

    # Sintáctico
    syntax_frame = tk.LabelFrame(right_frame, text="Analizador Sintáctico", bg=style.PANEL_HEADER_BG)
    syntax_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")
    scrollbar_parser_y = tk.Scrollbar(syntax_frame)
    scrollbar_parser_y.pack(side="right", fill="y")
    self.syntax_output = tk.Text(syntax_frame, bg=style.PANEL_BG, fg="white", state="disabled", yscrollcommand=scrollbar_parser_y.set)
    self.syntax_output.pack(fill="both", expand=True)
    scrollbar_parser_y.config(command=self.syntax_output.yview)

    # Semántico
    semantic_frame = tk.LabelFrame(right_frame, text="Analizador Semántico", bg=style.PANEL_HEADER_BG)
    semantic_frame.grid(row=0, column=2, sticky="nsew")
    scrollbar_semantic_y = tk.Scrollbar(semantic_frame)
    scrollbar_semantic_y.pack(side="right", fill="y")
    self.semantic_output = tk.Text(semantic_frame, bg=style.PANEL_BG, fg="white", state="disabled", yscrollcommand=scrollbar_semantic_y.set)
    self.semantic_output.pack(fill="both", expand=True)
    scrollbar_semantic_y.config(command=self.semantic_output.yview)

