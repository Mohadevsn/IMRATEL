import customtkinter as ctk

# ── Design System: Technical Precision ───────────────────────────────────────
PRIMARY         = "#0056B3"   # actions, boutons, état actif
DEEP_NAVY       = "#002D62"   # sidebar, headers
ACCENT_AMBER    = "#F89406"   # résultats critiques
SURFACE         = "#F9F9FF"   # fond principal
SURFACE_CARD    = "#F2F3FC"   # cartes
OUTLINE         = "#D9D9E2"   # bordures
ON_SURFACE      = "#212529"   # texte principal
ON_SURFACE_VAR  = "#495057"   # texte secondaire
WHITE           = "#ffffff"
RADIUS          = 4


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

        # ── Sidebar 260px ─────────────────────────────────────────────────────
        sb = ctk.CTkFrame(self.root, width=260, corner_radius=0, fg_color=DEEP_NAVY)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_columnconfigure(0, weight=1)
        sb.grid_rowconfigure(9, weight=1)

        ctk.CTkLabel(sb, text="IMRATEL",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     text_color=WHITE).grid(row=0, column=0, padx=24, pady=(36, 2), sticky="w")

        ctk.CTkLabel(sb, text="Dimensionnement Télécoms",
                     font=ctk.CTkFont(size=10),
                     text_color=ON_SURFACE_VAR).grid(row=1, column=0, padx=24, pady=(0, 24), sticky="w")

        ctk.CTkFrame(sb, height=1, fg_color="#1a3a5c").grid(
            row=2, column=0, sticky="ew", padx=20, pady=(0, 20))

        modules = [
            ("Décibels",                   self._show_decibels),
            ("Shannon / Nyquist",          self._show_shannon),
            ("Bilan Fibre Optique",        self._show_fibre),
            ("Dimensionnement Cellulaire", self._show_cellulaire),
        ]
        for i, (label, cmd) in enumerate(modules):
            btn = ctk.CTkButton(
                sb, text=f"  {label}",
                command=lambda c=cmd, l=label: self._nav(c, l),
                fg_color="transparent", text_color=WHITE,
                hover_color=PRIMARY, anchor="w",
                font=ctk.CTkFont(size=12), height=44,
                corner_radius=RADIUS,
            )
            btn.grid(row=3 + i, column=0, padx=14, pady=3, sticky="ew")
            self._nav_buttons[label] = btn

        ctk.CTkLabel(sb, text="v1.0  ·  MASTER GLSI",
                     font=ctk.CTkFont(size=9),
                     text_color="#3d5166").grid(row=10, column=0, pady=20)

        # ── Zone contenu ──────────────────────────────────────────────────────
        self.content = ctk.CTkFrame(self.root, corner_radius=0, fg_color=SURFACE)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self._show_welcome()

    def _nav(self, cmd, label):
        for btn in self._nav_buttons.values():
            btn.configure(fg_color="transparent")
        self._nav_buttons[label].configure(fg_color=PRIMARY)
        cmd()

    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _page(self, title: str, subtitle: str = "") -> ctk.CTkFrame:
        self._clear()
        wrapper = ctk.CTkFrame(self.content, fg_color=SURFACE, corner_radius=0)
        wrapper.grid(row=0, column=0, sticky="nsew", padx=32, pady=28)
        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(wrapper, text=title,
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=DEEP_NAVY).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(wrapper, text=subtitle,
                     font=ctk.CTkFont(size=11),
                     text_color=ON_SURFACE_VAR).grid(row=1, column=0, sticky="w", pady=(3, 16))

        card = ctk.CTkFrame(wrapper, fg_color=SURFACE_CARD,
                             corner_radius=RADIUS,
                             border_width=1, border_color=OUTLINE)
        card.grid(row=2, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)
        return card

    def _show_welcome(self):
        self._clear()
        frame = ctk.CTkFrame(self.content, fg_color=SURFACE, corner_radius=0)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="IMRATEL",
                     font=ctk.CTkFont(size=42, weight="bold"),
                     text_color=DEEP_NAVY).pack()
        ctk.CTkLabel(frame, text="Outil de Dimensionnement des Réseaux Télécoms",
                     font=ctk.CTkFont(size=13),
                     text_color=ON_SURFACE_VAR).pack(pady=(6, 32))

        for m in ["Décibels", "Shannon / Nyquist",
                  "Bilan Fibre Optique", "Dimensionnement Cellulaire"]:
            ctk.CTkLabel(frame, text=f"  ›   {m}",
                         font=ctk.CTkFont(size=12),
                         text_color=ON_SURFACE).pack(anchor="w", pady=4)

        ctk.CTkLabel(frame, text="\nSélectionnez un module dans le menu à gauche.",
                     font=ctk.CTkFont(size=10),
                     text_color=ON_SURFACE_VAR).pack()

    def _show_decibels(self):
        from modules.decibels import DecibelFrame
        DecibelFrame(self._page("Décibels",
                                "Conversion dB ↔ Linéaire  ·  dBm ↔ mW")).pack(
            fill="both", expand=True, padx=28, pady=22)

    def _show_shannon(self):
        from modules.shannon import ShannonFrame
        ShannonFrame(self._page("Shannon / Nyquist",
                                "Calcul du débit maximal théorique")).pack(
            fill="both", expand=True, padx=28, pady=22)

    def _show_fibre(self):
        from modules.fibre import FibreFrame
        FibreFrame(self._page("Bilan de Liaison Fibre Optique",
                              "Laissez vide la variable à calculer : P_in, P_out ou L")).pack(
            fill="both", expand=True, padx=28, pady=22)

    def _show_cellulaire(self):
        from modules.cellulaire import CellulairFrame
        CellulairFrame(self._page("Dimensionnement Cellulaire",
                                   "N = i² + i·j + j²   ·   motif hexagonal interactif")).pack(
            fill="both", expand=True, padx=28, pady=22)
