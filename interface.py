import tkinter as tk
from tkinter import ttk


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IMRATEL — Outil de Dimensionnement Télécoms")
        self.root.geometry("1000x650")
        self.root.resizable(True, True)

        self._build_layout()

    def _build_layout(self):
        # Zone gauche : menu de navigation
        self.sidebar = tk.Frame(self.root, width=200, bg="#1e2a38")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="IMRATEL",
            bg="#1e2a38",
            fg="#ffffff",
            font=("Helvetica", 16, "bold"),
        ).pack(pady=(30, 5))

        tk.Label(
            self.sidebar,
            text="Dimensionnement Télécoms",
            bg="#1e2a38",
            fg="#8a9bb0",
            font=("Helvetica", 8),
            wraplength=180,
        ).pack(pady=(0, 30))

        modules = [
            ("Décibels", self._show_decibels),
            ("Shannon / Nyquist", self._show_shannon),
            ("Bilan Fibre Optique", self._show_fibre),
            ("Dimensionnement Cellulaire", self._show_cellulaire),
        ]

        for label, command in modules:
            btn = tk.Button(
                self.sidebar,
                text=label,
                command=command,
                bg="#2c3e50",
                fg="#ffffff",
                font=("Helvetica", 10),
                relief=tk.FLAT,
                cursor="hand2",
                pady=12,
                padx=10,
                anchor="w",
            )
            btn.pack(fill=tk.X, padx=10, pady=4)

        # Zone droite : contenu
        self.content = tk.Frame(self.root, bg="#f0f2f5")
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._show_welcome()

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def _show_welcome(self):
        self._clear_content()
        tk.Label(
            self.content,
            text="Bienvenue sur IMRATEL",
            bg="#f0f2f5",
            font=("Helvetica", 20, "bold"),
            fg="#1e2a38",
        ).pack(expand=True)
        tk.Label(
            self.content,
            text="Sélectionnez un module dans le menu pour commencer.",
            bg="#f0f2f5",
            font=("Helvetica", 11),
            fg="#555",
        ).pack()

    def _show_decibels(self):
        from modules.decibels import DecibelFrame
        self._clear_content()
        DecibelFrame(self.content).pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    def _show_shannon(self):
        from modules.shannon import ShannonFrame
        self._clear_content()
        ShannonFrame(self.content).pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    def _show_fibre(self):
        from modules.fibre import FibreFrame
        self._clear_content()
        FibreFrame(self.content).pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    def _show_cellulaire(self):
        from modules.cellulaire import CellulairFrame
        self._clear_content()
        CellulairFrame(self.content).pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
