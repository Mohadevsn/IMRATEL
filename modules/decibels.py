import math
import customtkinter as ctk

PRIMARY        = "#0056B3"
DEEP_NAVY      = "#002D62"
ACCENT_AMBER   = "#F89406"
SURFACE_CARD   = "#F2F3FC"
OUTLINE        = "#D9D9E2"
ON_SURFACE     = "#212529"
ON_SURFACE_VAR = "#495057"
WHITE          = "#ffffff"
OK             = "#27ae60"
ERR            = "#e74c3c"
RADIUS         = 4


# ── Calculs ───────────────────────────────────────────────────────────────────

def db_to_linear(db: float, factor: int = 10) -> float:
    return 10 ** (db / factor)

def linear_to_db(linear: float, factor: int = 10) -> float:
    if linear <= 0:
        raise ValueError("La valeur doit être strictement positive.")
    return factor * math.log10(linear)

def dbm_to_mw(dbm: float) -> float:
    return 10 ** (dbm / 10)

def mw_to_dbm(mw: float) -> float:
    if mw <= 0:
        raise ValueError("La puissance doit être strictement positive.")
    return 10 * math.log10(mw)


# ── Frame principale ──────────────────────────────────────────────────────────

class DecibelFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # ── Carte gauche : paramètres ─────────────────────────────────────────
        left = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=RADIUS,
                             border_width=1, border_color=OUTLINE)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)

        # Header carte gauche
        h = ctk.CTkFrame(left, fg_color=WHITE, corner_radius=0)
        h.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 14))
        ctk.CTkLabel(h, text="⇄  PARAMÈTRES D'ENTRÉE",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=PRIMARY).pack(side="left")

        ctk.CTkFrame(left, height=1, fg_color=OUTLINE).grid(
            row=1, column=0, sticky="ew", padx=0)

        body = ctk.CTkFrame(left, fg_color=WHITE, corner_radius=0)
        body.grid(row=2, column=0, sticky="nsew", padx=20, pady=16)
        body.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(2, weight=1)

        # Champ de valeur
        ctk.CTkLabel(body, text="Valeur à convertir", text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=11)).grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.var_val = ctk.StringVar()
        self.entry_val = ctk.CTkEntry(body, textvariable=self.var_val,
                                       placeholder_text="Ex: 10",
                                       font=ctk.CTkFont(size=14), height=46,
                                       corner_radius=RADIUS, border_color=PRIMARY,
                                       border_width=2, fg_color=WHITE)
        self.entry_val.grid(row=1, column=0, sticky="ew", pady=(0, 18))

        # Toggle direction
        ctk.CTkLabel(body, text="Unité Source", text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=11)).grid(row=2, column=0, sticky="w", pady=(0, 4))
        self.seg = ctk.CTkSegmentedButton(
            body,
            values=["Décibel (dB)", "Réelle (Linéaire)"],
            fg_color=SURFACE_CARD,
            selected_color=PRIMARY,
            selected_hover_color=DEEP_NAVY,
            unselected_color=SURFACE_CARD,
            unselected_hover_color=OUTLINE,
            text_color=ON_SURFACE,
            font=ctk.CTkFont(size=11),
            corner_radius=RADIUS,
        )
        self.seg.grid(row=3, column=0, sticky="ew", pady=(0, 18))
        self.seg.set("Décibel (dB)")

        # Option type de grandeur
        ctk.CTkLabel(body, text="Type de Grandeur", text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=11)).grid(row=4, column=0, sticky="w", pady=(0, 4))
        self.opt = ctk.CTkOptionMenu(
            body,
            values=["Puissance  (P = 10 · log₁₀)", "Tension  (V = 20 · log₁₀)"],
            fg_color=SURFACE_CARD, button_color=PRIMARY,
            button_hover_color=DEEP_NAVY, text_color=ON_SURFACE,
            font=ctk.CTkFont(size=11), corner_radius=RADIUS,
        )
        self.opt.grid(row=5, column=0, sticky="ew", pady=(0, 24))
        self.opt.set("Puissance  (P = 10 · log₁₀)")

        # Bouton calculer
        ctk.CTkButton(body, text="▣  CALCULER", command=self._calculate,
                       font=ctk.CTkFont(size=13, weight="bold"),
                       height=46, corner_radius=RADIUS,
                       fg_color=PRIMARY, hover_color=DEEP_NAVY).grid(
            row=6, column=0, sticky="ew")

        # Rappels techniques
        rappels = ctk.CTkFrame(left, fg_color=SURFACE_CARD, corner_radius=RADIUS)
        rappels.grid(row=3, column=0, sticky="ew", padx=20, pady=(12, 20))
        rappels.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(rappels, text="ⓘ  RAPPELS TECHNIQUES",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=ON_SURFACE_VAR).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(10, 8))

        for i, (gauche, droite) in enumerate([
            ("0 dBm", "1 mW"),
            ("3 dB", "Puissance × 2"),
            ("10 dB", "Puissance × 10"),
            ("20 dB", "Tension × 10"),
        ]):
            ctk.CTkLabel(rappels, text=gauche, font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=ON_SURFACE).grid(row=i+1, column=0, sticky="w", padx=12, pady=3)
            ctk.CTkLabel(rappels, text=droite, font=ctk.CTkFont(size=11),
                         text_color=ON_SURFACE_VAR).grid(row=i+1, column=1, sticky="e", padx=12, pady=3)
        ctk.CTkFrame(rappels, height=8, fg_color=SURFACE_CARD).grid(row=6, column=0)

        # ── Carte droite : résultat ───────────────────────────────────────────
        right = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=RADIUS,
                              border_width=1, border_color=OUTLINE)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        rh = ctk.CTkFrame(right, fg_color=WHITE, corner_radius=0)
        rh.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 14))
        ctk.CTkLabel(rh, text="▣  RÉSULTAT D'ANALYSE",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=ACCENT_AMBER).pack(side="left")

        ctk.CTkFrame(right, height=1, fg_color=OUTLINE).grid(
            row=1, column=0, sticky="ew")

        result_body = ctk.CTkFrame(right, fg_color=WHITE, corner_radius=0)
        result_body.grid(row=2, column=0, sticky="nsew")
        result_body.grid_columnconfigure(0, weight=1)
        result_body.grid_rowconfigure(0, weight=1)

        # Zone résultat (centrée)
        self.result_zone = ctk.CTkFrame(result_body, fg_color=WHITE, corner_radius=0)
        self.result_zone.place(relx=0.5, rely=0.5, anchor="center")

        self.result_val = ctk.CTkLabel(self.result_zone, text="—",
                                        font=ctk.CTkFont(size=38, weight="bold"),
                                        text_color=DEEP_NAVY)
        self.result_val.pack()

        self.result_unit = ctk.CTkLabel(self.result_zone, text="",
                                         font=ctk.CTkFont(size=14),
                                         text_color=ON_SURFACE_VAR)
        self.result_unit.pack(pady=(4, 0))

        self.result_formula = ctk.CTkLabel(self.result_zone, text="",
                                            font=ctk.CTkFont(size=11, slant="italic"),
                                            text_color=ON_SURFACE_VAR)
        self.result_formula.pack(pady=(12, 0))

        self.result_err = ctk.CTkLabel(result_body, text="",
                                        font=ctk.CTkFont(size=12),
                                        text_color=ERR)
        self.result_err.grid(row=1, column=0, pady=(0, 16))

    def _calculate(self):
        val_str = self.var_val.get().strip()
        if not val_str:
            self.result_val.configure(text="—", text_color=DEEP_NAVY)
            self.result_unit.configure(text="Entrez une valeur")
            self.result_formula.configure(text="")
            self.result_err.configure(text="")
            return

        factor = 20 if "Tension" in self.opt.get() else 10
        direction = self.seg.get()

        try:
            val = float(val_str)
            if direction == "Décibel (dB)":
                result = db_to_linear(val, factor)
                self.result_val.configure(text=f"{result:.6g}", text_color=DEEP_NAVY)
                self.result_unit.configure(text="valeur linéaire")
                self.result_formula.configure(
                    text=f"10^({val}/{factor}) = {result:.6g}")
            else:
                result = linear_to_db(val, factor)
                self.result_val.configure(text=f"{result:.4f}", text_color=DEEP_NAVY)
                self.result_unit.configure(text="dB")
                self.result_formula.configure(
                    text=f"{factor} · log₁₀({val}) = {result:.4f} dB")
            self.result_err.configure(text="")
        except ValueError as e:
            self.result_val.configure(text="Erreur", text_color=ERR)
            self.result_unit.configure(text="")
            self.result_formula.configure(text="")
            self.result_err.configure(text=str(e))
