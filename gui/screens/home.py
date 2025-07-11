import tkinter as tk
from tkinter import filedialog
from gui import style
from analizer.lexer import lexer, lexer_analyze
from analizer.parser import parser_analyze, semantic_analyse
from .home_editor import create_editor_panel
from .home_buttons import create_buttons_panel
from .home_analysis import create_analysis_panels

class Home(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padx=20, pady=20, background=style.BACKGROUND)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, minsize=style.PANELS_SPACE)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, minsize=style.PANELS_SPACE)
        self.rowconfigure(2, weight=1)
        self._analisis_programado = None
        self.semantic_available = False
        self.live_enabled = False
        create_editor_panel(self, 0, 0)
        create_buttons_panel(self, 2, 0)
        create_analysis_panels(self, 0, 2)
        self.update_line_numbers()

    #Editor logic ===============================================================
    def _on_scrollbar(self, *args):
        self.editor.yview(*args)
        self.line_numbers.yview(*args)

    def _on_mousewheel(self, event):
        self.editor.yview("scroll", int(-1*(event.delta/120)), "units")
        self.line_numbers.yview("scroll", int(-1*(event.delta/120)), "units")
        return "break"

    def update_line_numbers(self, event=None):
        if self.semantic_available:
            self.semantic_disabled()
            self.semantic_available = False
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        codigo = self.editor.get("1.0", "end-1c")
        num_lines = codigo.count('\n') + 1 if codigo else 1
        line_nums = "\n".join(str(i) for i in range(1, num_lines + 1))
        self.line_numbers.insert("1.0", line_nums)
        self.line_numbers.configure(state="disabled")
        if event and event.type == tk.EventType.VirtualEvent:
            self.editor.edit_modified(False)

    #Live logic =================================================================
    def debounce_analisis(self, event=None):
        if not self.live_enabled:
            return
        if self._analisis_programado:
            self.after_cancel(self._analisis_programado)
        self._analisis_programado = self.after(1000, self.analizar_todo(False))

    def analizar_todo(self, clean=True):
        if clean:
            self.clean_lexico()
            self.clean_sintactico()
        code = self.editor.get("1.0", "end-1c")
        self.analisis_lexico(code)
        self.analisis_sintactico(code)
        self.analisis_semantico(code)

    #Buttons logic ==============================================================
    def clean_panels(self):
        self.editor.delete("1.0", "end")
        if self.semantic_available:
            self.semantic_disabled()
            self.semantic_available = False
        self.clean_lexico()
        self.clean_sintactico()
        self.clean_semantico()
        
    def analisis_lexico(self, code=None):
        if code is None:
            self.clean_lexico()
            code = self.editor.get("1.0", "end-1c")
        if not code.strip():
            self.clean_lexico()
            return
        tokens, errors_lex = lexer_analyze(code)
        tokens_totales = tokens + errors_lex
        tokens_totales.sort(key=lambda tok: (tok.linea, tok.columna))
        self.insertar_tokens(tokens_totales)

    def clean_lexico(self):
        for row in self.lexical_table.get_children():
            self.lexical_table.delete(row)

    def analisis_sintactico(self, code=None):
        if code is None:
            code = self.editor.get("1.0", "end-1c")
        if not code.strip():
            self.clean_sintactico()
            return
        if not self.semantic_available:
            self.semantic_disabled(False)
            self.semantic_available = True
        parser_result = parser_analyze(code)
        self.syntax_output.configure(state="normal")
        self.syntax_output.delete("1.0", "end")
        self.syntax_output.insert("1.0", parser_result)
        self.syntax_output.configure(state="disabled")
    
    def clean_sintactico(self):
        self.syntax_output.configure(state="normal")
        self.syntax_output.delete("1.0", "end")
        self.syntax_output.configure(state="disabled")

    def analisis_semantico(self, code=None):
        if code is None:
            code = self.editor.get("1.0", "end-1c")
        if not code.strip():
            self.clean_semantico()
            return
        semantic_result = semantic_analyse()
        self.semantic_output.configure(state="normal")
        self.semantic_output.delete("1.0", "end")
        self.semantic_output.insert("1.0", semantic_result)
        self.semantic_output.configure(state="disabled")

    def clean_semantico(self):
        self.semantic_output.configure(state="normal")
        self.semantic_output.delete("1.0", "end")
        self.semantic_output.configure(state="disabled")

    def open_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Go Files", "*.go"), ("Text Files", "*.txt")]
        )
        if not filepath:
            return
        if self.semantic_available:
            self.semantic_disabled()
            self.semantic_available = False
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", content)

    def toggle_live(self):
        self.live_enabled = not self.live_enabled
        boton = self.boton_toggle_live
        if self.live_enabled:
            boton.config(text="Live: ON", bg=style.BUTTON_ON_BG)
        else:
            boton.config(text="Live: OFF", bg=style.BUTTON_OFF_BG)

    def semantic_disabled(self, turnOff=True):
        boton = self.semantic_button
        if turnOff:
            #self.clean_semantico()
            boton.config(state="disabled")
            boton.config(bg=style.BUTTON_DISABLED)
        else:
            boton.config(state="normal")
            boton.config(bg=style.BUTTONS_T1_BG)
    
    def insertar_tokens(self, tokens):
        self.clean_lexico()
        for t in tokens:
            if t.category == "error":
                self.lexical_table.insert("", "end", values=(t.lexema, t.tipo, t.linea, t.columna), tags=("error",))
            else:
                self.lexical_table.insert("", "end", values=(t.lexema, t.tipo, t.linea, t.columna))
        self.lexical_table.tag_configure("error", background=style.BUTTON_OFF_BG, foreground="white")
