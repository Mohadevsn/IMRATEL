import customtkinter as ctk

PRIMARY        = "#0056B3"
DEEP_NAVY      = "#002D62"
ACCENT_AMBER   = "#F89406"
SURFACE        = "#F9F9FF"
SURFACE_CARD   = "#F2F3FC"
OUTLINE        = "#D9D9E2"
ON_SURFACE     = "#212529"
ON_SURFACE_VAR = "#495057"
WHITE          = "#ffffff"
RADIUS         = 4


class MainApp:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("IMRATEL — Outil de Dimensionnement Télécoms")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)
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
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=WHITE).grid(row=0, column=0, padx=24, pady=(32, 2), sticky="w")
        ctk.CTkLabel(sb, text="TELECOMMUNICATIONS TOOL",
                     font=ctk.CTkFont(size=9),
                     text_color="#4a6278").grid(row=1, column=0, padx=24, pady=(0, 28), sticky="w")

        ctk.CTkFrame(sb, height=1, fg_color="#1a3a5c").grid(
            row=2, column=0, sticky="ew", padx=20, pady=(0, 16))

        modules = [
            ("Module Décibels",           "ll",  self._show_decibels),
            ("Module Shannon / Nyquist",  "~",   self._show_shannon),
            ("Bilan Fibre Optique",       "###", self._show_fibre),
            ("Dimensionnement Cellulaire","(())", self._show_cellulaire),
        ]
        for i, (label, _, cmd) in enumerate(modules):
            btn = ctk.CTkButton(
                sb, text=f"  {label}",
                command=lambda c=cmd, l=label: self._nav(c, l),
                fg_color="transparent", text_color="#b0bec5",
                hover_color="#0d3a6e", anchor="w",
                font=ctk.CTkFont(size=12), height=44,
                corner_radius=RADIUS,
            )
            btn.grid(row=3 + i, column=0, padx=12, pady=2, sticky="ew")
            self._nav_buttons[label] = btn

        # Bas de sidebar
        ctk.CTkFrame(sb, height=1, fg_color="#1a3a5c").grid(
            row=9, column=0, sticky="ew", padx=20, pady=(0, 8))
        ctk.CTkLabel(sb, text="v1.0  ·  MASTER GLSI",
                     font=ctk.CTkFont(size=9),
                     text_color="#3d5166").grid(row=10, column=0, pady=(4, 16))

        # ── Zone contenu ──────────────────────────────────────────────────────
        self.content = ctk.CTkFrame(self.root, corner_radius=0, fg_color=SURFACE)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        self._topbar = ctk.CTkFrame(self.content, height=48, corner_radius=0,
                                     fg_color=WHITE,
                                     border_width=1, border_color=OUTLINE)
        self._topbar.grid(row=0, column=0, sticky="ew")
        self._topbar.grid_propagate(False)
        self._topbar.grid_columnconfigure(1, weight=1)

        self._bc_label = ctk.CTkLabel(self._topbar, text="Espace de Calcul",
                                       font=ctk.CTkFont(size=11),
                                       text_color=PRIMARY)
        self._bc_label.grid(row=0, column=0, padx=24, pady=14, sticky="w")

        ctk.CTkLabel(self._topbar, text="?   Administrateur",
                     font=ctk.CTkFont(size=11),
                     text_color=ON_SURFACE_VAR).grid(row=0, column=2, padx=24)

        self._main = ctk.CTkFrame(self.content, corner_radius=0, fg_color=SURFACE)
        self._main.grid(row=1, column=0, sticky="nsew")
        self._main.grid_columnconfigure(0, weight=1)
        self._main.grid_rowconfigure(0, weight=1)

        self._show_welcome()

    # ── Navigation ────────────────────────────────────────────────────────────

    def _nav(self, cmd, label):
        for btn in self._nav_buttons.values():
            btn.configure(fg_color="transparent", text_color="#b0bec5")
        self._nav_buttons[label].configure(fg_color="#0d3a6e", text_color=WHITE)
        cmd()

    def _clear(self):
        for w in self._main.winfo_children():
            w.destroy()

    def _page(self, title: str, subtitle: str, breadcrumb: str) -> ctk.CTkFrame:
        """Retourne la zone de contenu après le header."""
        self._clear()
        self._bc_label.configure(text=breadcrumb)

        wrap = ctk.CTkFrame(self._main, fg_color=SURFACE, corner_radius=0)
        wrap.grid(row=0, column=0, sticky="nsew", padx=32, pady=(24, 16))
        wrap.grid_columnconfigure(0, weight=1)
        wrap.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(wrap, text=title,
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=DEEP_NAVY).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(wrap, text=subtitle,
                     font=ctk.CTkFont(size=11),
                     text_color=ON_SURFACE_VAR).grid(row=1, column=0, sticky="w", pady=(4, 16))

        zone = ctk.CTkFrame(wrap, fg_color=SURFACE, corner_radius=0)
        zone.grid(row=2, column=0, sticky="nsew")
        zone.grid_columnconfigure(0, weight=1)
        zone.grid_rowconfigure(0, weight=1)
        return zone

    # ── Accueil ───────────────────────────────────────────────────────────────

    def _show_welcome(self):
        self._clear()
        self._bc_label.configure(text="Espace de Calcul")
        frame = ctk.CTkFrame(self._main, fg_color=SURFACE, corner_radius=0)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="IMRATEL",
                     font=ctk.CTkFont(size=44, weight="bold"),
                     text_color=DEEP_NAVY).pack()
        ctk.CTkLabel(frame, text="Outil de Dimensionnement des Réseaux Télécoms",
                     font=ctk.CTkFont(size=13), text_color=ON_SURFACE_VAR).pack(pady=(6, 32))
        for m in ["Module Décibels", "Module Shannon / Nyquist",
                  "Bilan Fibre Optique", "Dimensionnement Cellulaire"]:
            ctk.CTkLabel(frame, text=f"  ›   {m}",
                         font=ctk.CTkFont(size=12), text_color=ON_SURFACE).pack(anchor="w", pady=3)
        ctk.CTkLabel(frame, text="\nSélectionnez un module dans le menu à gauche.",
                     font=ctk.CTkFont(size=10), text_color=ON_SURFACE_VAR).pack()

    # ── Modules ───────────────────────────────────────────────────────────────

    def _show_decibels(self):
        from modules.decibels import DecibelFrame
        DecibelFrame(self._page(
            "Module Décibels",
            "Outil de conversion universel pour les calculs de puissance et de tension.",
            "Espace de Calcul")).pack(fill="both", expand=True)

    def _show_shannon(self):
        from modules.shannon import ShannonFrame
        ShannonFrame(self._page(
            "Module Shannon / Nyquist",
            "Calcul théorique de la capacité de canal pour les transmissions numériques.",
            "Espace de travail  ›  Module Shannon / Nyquist")).pack(fill="both", expand=True)

    def _show_fibre(self):
        from modules.fibre import FibreFrame
        FibreFrame(self._page(
            "Bilan de Liaison Fibre",
            "Outil de calcul de bilan de puissance pour les liaisons point à point.",
            "WORKSPACE  ›  Bilan Fibre Optique")).pack(fill="both", expand=True)

    def _show_cellulaire(self):
        from modules.cellulaire import CellulairFrame
        CellulairFrame(self._page(
            "Module Dimensionnement Cellulaire",
            "Calculez la taille du motif de réutilisation des fréquences (N).",
            "Dimensionnement Réseau")).pack(fill="both", expand=True)
