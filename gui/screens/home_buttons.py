import tkinter as tk

def create_buttons_panel(self, r, c):
    actions_frame = tk.Frame(self, bg="#121212")
    actions_frame.grid(row=r, column=c, sticky="nsew")

    tk.Button(actions_frame, text="⬆️", width=3, command=self.open_file).grid(row=0, column=0, padx=4) #Subir archivo
    tk.Button(actions_frame, text="Limpiar", bg="#C0C0C0", command=self.clean_panels).grid(row=0, column=1, padx=4)
    self.boton_toggle_live = tk.Button(actions_frame, text="Live: OFF", bg="#FF9999", command=self.toggle_live)
    self.boton_toggle_live.grid(row=0, column=2, padx=4)
    tk.Button(actions_frame, text="Ejecutar todo", bg="#99CCFF", command=self.analizar_todo).grid(row=0, column=3, padx=4)

    buttons_frame = tk.Frame(actions_frame, bg="#121212")
    buttons_frame.grid(row=1, column=0, columnspan=3, pady=10)

    tk.Button(buttons_frame, text="Ejecutar análisis léxico", bg="#00C2B2", command=self.analisis_lexico).pack(fill="x", pady=2)
    tk.Button(buttons_frame, text="Ejecutar análisis sintáctico", bg="#00C2B2", command=self.analisis_sintactico).pack(fill="x", pady=2)
    tk.Button(buttons_frame, text="Ejecutar análisis semántico", bg="#A0E0DA").pack(fill="x", pady=2)



