import customtkinter as ctk

SIDEBAR  = "#1e2a38"
BG       = "#f4f6f9"
CARD     = "#ffffff"
ACCENT   = "#2980b9"
TEXT     = "#2c3e50"
MUTED    = "#95a5a6"
SEP      = "#2c3e50"


class MainApp:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("IMRATEL — Outil de Dimensionnement Télécoms")
        self.root.geometry("1150x700")
        self.root.minsize(950, 620)
        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        self._build_layout()

    def _build_layout(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # ── Sidebar ──────────────────────────────────────────────────────────
        sb = ctk.CTkFrame(self.root, width=220, corner_radius=0, fg_color=SIDEBAR)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_columnconfigure(0, weight=1)
        sb.grid_rowconfigure(9, weight=1)

        ctk.CTkLabel(sb, text="IMRATEL",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#ffffff").grid(row=0, column=0, padx=22, pady=(36, 2), sticky="w")

        ctk.CTkLabel(sb, text="Dimensionnement Télécoms",
                     font=ctk.CTkFont(size=10),
                     text_color=MUTED).grid(row=1, column=0, padx=22, pady=(0, 20), sticky="w")

        ctk.CTkFrame(sb, height=1, fg_color=SEP).grid(
            row=2, column=0, sticky="ew", padx=18, pady=(0, 18))

        modules = [
            ("  Décibels",                  self._show_decibels),
            ("  Shannon / Nyquist",         self._show_shannon),
            ("  Bilan Fibre Optique",       self._show_fibre),
            ("  Dim. Cellulaire",           self._show_cellulaire),
        ]
        for i, (label, cmd) in enumerate(modules):
            btn = ctk.CTkButton(
                sb, text=label,
                command=lambda c=cmd, l=label.strip(): self._nav(c, l),
                fg_color="transparent", text_color="#ffffff",
                hover_color=ACCENT, anchor="w",
                font=ctk.CTkFont(size=12), height=42, corner_radius=8,
            )
            btn.grid(row=3 + i, column=0, padx=12, pady=3, sticky="ew")
            self._nav_buttons[label.strip()] = btn

        ctk.CTkLabel(sb, text="v1.0  ·  MASTER GLSI",
                     font=ctk.CTkFont(size=9), text_color="#3d5166").grid(
            row=10, column=0, pady=18)

        # ── Zone contenu ─────────────────────────────────────────────────────
        self.content = ctk.CTkFrame(self.root, corner_radius=0, fg_color=BG)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self._show_welcome()

    # ── Navigation ────────────────────────────────────────────────────────────

    def _nav(self, cmd, label):
        for btn in self._nav_buttons.values():
            btn.configure(fg_color="transparent")
        self._nav_buttons[label].configure(fg_color=ACCENT)
        cmd()

    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _page(self, title: str, subtitle: str = "") -> ctk.CTkFrame:
        """Retourne la carte blanche d'un module."""
        self._clear()

        wrapper = ctk.CTkFrame(self.content, fg_color=BG, corner_radius=0)
        wrapper.grid(row=0, column=0, sticky="nsew", padx=32, pady=26)
        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(wrapper, text=title,
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=TEXT).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(wrapper, text=subtitle,
                     font=ctk.CTkFont(size=10), text_color=MUTED).grid(
            row=1, column=0, sticky="w", pady=(2, 14))

        card = ctk.CTkFrame(wrapper, fg_color=CARD, corner_radius=14)
        card.grid(row=2, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)
        return card

    # ── Écran d'accueil ───────────────────────────────────────────────────────

    def _show_welcome(self):
        self._clear()
        frame = ctk.CTkFrame(self.content, fg_color=BG, corner_radius=0)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="IMRATEL",
                     font=ctk.CTkFont(size=40, weight="bold"),
                     text_color=TEXT).pack()
        ctk.CTkLabel(frame, text="Outil de Dimensionnement des Réseaux Télécoms",
                     font=ctk.CTkFont(size=13), text_color=MUTED).pack(pady=(6, 28))

        for m in ["Décibels", "Shannon / Nyquist",
                  "Bilan Fibre Optique", "Dimensionnement Cellulaire"]:
            ctk.CTkLabel(frame, text=f"  ›   {m}",
                         font=ctk.CTkFont(size=12), text_color=TEXT).pack(anchor="w", pady=3)

        ctk.CTkLabel(frame, text="\nSélectionnez un module dans le menu à gauche.",
                     font=ctk.CTkFont(size=10), text_color=MUTED).pack()

    # ── Modules ───────────────────────────────────────────────────────────────

    def _show_decibels(self):
        from modules.decibels import DecibelFrame
        DecibelFrame(self._page("Décibels", "Conversion dB ↔ Linéaire  ·  dBm ↔ mW")).pack(
            fill="both", expand=True, padx=28, pady=22)

    def _show_shannon(self):
        from modules.shannon import ShannonFrame
        ShannonFrame(self._page("Shannon / Nyquist", "Calcul du débit maximal théorique")).pack(
            fill="both", expand=True, padx=28, pady=22)

    def _show_fibre(self):
        from modules.fibre import FibreFrame
        FibreFrame(self._page(
            "Bilan de Liaison Fibre Optique",
            "Laissez vide la variable à calculer : P_in, P_out ou L")).pack(
            fill="both", expand=True, padx=28, pady=22)

    def _show_cellulaire(self):
        from modules.cellulaire import CellulairFrame
        CellulairFrame(self._page(
            "Dimensionnement Cellulaire",
            "N = i² + i·j + j²   ·   motif hexagonal interactif")).pack(
            fill="both", expand=True, padx=28, pady=22)
