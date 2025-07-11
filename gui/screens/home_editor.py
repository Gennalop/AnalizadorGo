import tkinter as tk

def create_editor_panel(self, r, c):
    editorFrame = tk.Frame(self)
    editorFrame.grid(row=r, column=c, sticky="nsew")

    scrollbar_y = tk.Scrollbar(editorFrame)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_y.config(command=self._on_scrollbar)

    scrollbar_x = tk.Scrollbar(editorFrame, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    self.line_numbers = tk.Text(editorFrame, width=4, bg="#1e1e1e", fg="white", state="disabled", yscrollcommand=scrollbar_y.set)
    self.line_numbers.pack(side="left", fill="y")

    self.editor = tk.Text(editorFrame, bg="#1e1e1e", fg="white", insertbackground="white", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set, wrap="none")
    self.editor.pack(side="left", fill="both", expand=True) 

    scrollbar_x.config(command=self.editor.xview)

    self.editor.bind("<KeyRelease>", self.debounce_analisis)
    self.editor.bind("<Return>", self.update_line_numbers)
    self.editor.bind("<BackSpace>", self.update_line_numbers)
    self.editor.bind("<Delete>", self.update_line_numbers)
    self.editor.bind("<<Modified>>", self.update_line_numbers)
    self.editor.bind("<MouseWheel>", self._on_mousewheel)
    self.line_numbers.bind("<MouseWheel>", self._on_mousewheel)

    