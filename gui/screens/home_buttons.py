import tkinter as tk
from gui import style

def create_buttons_panel(self, r, c):
    actions_frame = tk.Frame(self, bg=style.BACKGROUND)
    actions_frame.grid(row=r, column=c, sticky="nsew")
    actions_frame.rowconfigure(1, weight=1)
    actions_frame.columnconfigure(2, weight=1) 

    tk.Button(actions_frame, text="⬆️", bg=style.BUTTONS_T2_BG, width=3, command=self.open_file).grid(row=0, column=0)
    tk.Button(actions_frame, text="Limpiar", bg=style.BUTTONS_T2_BG, command=self.clean_panels).grid(row=0, column=1, padx=4)
    self.boton_toggle_live = tk.Button(actions_frame, text="Live: OFF", bg=style.BUTTON_OFF_BG, command=self.toggle_live)
    self.boton_toggle_live.grid(row=0, column=3, padx=4)
    tk.Button(actions_frame, text="Ejecutar todo", bg=style.BUTTONS_T1_BG, command=self.analizar_todo).grid(row=0, column=4)

    buttons_frame = tk.Frame(actions_frame, bg=style.BACKGROUND)
    buttons_frame.grid(row=2, column=0, columnspan=5, sticky="w", padx=0)

    tk.Button(buttons_frame, text="Ejecutar análisis léxico", bg=style.BUTTONS_T1_BG, width=30, command=self.analisis_lexico).pack(anchor="w")
    tk.Button(buttons_frame, text="Ejecutar análisis sintáctico", bg=style.BUTTONS_T1_BG, width=30, command=self.analisis_sintactico).pack(anchor="w", pady=4)
    self.semantic_button = tk.Button(buttons_frame, text="Ejecutar análisis semántico", bg=style.BUTTON_DISABLED, width=30, command=self.analisis_semantico)
    self.semantic_button.config(state="disabled")
    self.semantic_button.pack(anchor="w")

