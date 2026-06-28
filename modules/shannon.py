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

def shannon_capacity(bandwidth_hz: float, snr_linear: float) -> float:
    return bandwidth_hz * math.log2(1 + snr_linear)

def nyquist_capacity(bandwidth_hz: float, M: int) -> float:
    if M < 2:
        raise ValueError("M doit être ≥ 2.")
    return 2 * bandwidth_hz * math.log2(M)

def nyquist_debit(Rm: float, V: int) -> float:
    """D = Rm · log₂(V)  [bit/s]"""
    if V < 2:
        raise ValueError("La valence V doit être ≥ 2.")
    return Rm * math.log2(V)

def snr_db_to_linear(snr_db: float) -> float:
    return 10 ** (snr_db / 10)

def format_bitrate(bps: float) -> tuple[str, str]:
    """Retourne (valeur, unité) séparés pour l'affichage."""
    if bps >= 1e9:
        return f"{bps / 1e9:.4f}", "Gbit/s"
    if bps >= 1e6:
        return f"{bps / 1e6:.4f}", "Mbit/s"
    if bps >= 1e3:
        return f"{bps / 1e3:.4f}", "kbit/s"
    return f"{bps:.4f}", "bit/s"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _card(parent, col, padx=(0, 0)):
    f = ctk.CTkFrame(parent, fg_color=WHITE, corner_radius=RADIUS,
                      border_width=1, border_color=OUTLINE)
    f.grid(row=0, column=col, sticky="nsew", padx=padx)
    f.grid_columnconfigure(0, weight=1)
    return f

def _card_header(card, text, color=PRIMARY):
    h = ctk.CTkFrame(card, fg_color=WHITE, corner_radius=0)
    h.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 14))
    ctk.CTkLabel(h, text=text, font=ctk.CTkFont(size=11, weight="bold"),
                 text_color=color).pack(side="left")
    ctk.CTkFrame(card, height=1, fg_color=OUTLINE).grid(row=1, column=0, sticky="ew")
    body = ctk.CTkFrame(card, fg_color=WHITE, corner_radius=0)
    body.grid(row=2, column=0, sticky="nsew", padx=20, pady=16)
    body.grid_columnconfigure(0, weight=1)
    card.grid_rowconfigure(2, weight=1)
    return body

def _field(parent, row, label, placeholder, unit=""):
    ctk.CTkLabel(parent, text=label, text_color=ON_SURFACE_VAR,
                 font=ctk.CTkFont(size=11)).grid(row=row*2, column=0, columnspan=2,
                                                   sticky="w", pady=(0, 4))
    e = ctk.CTkEntry(parent, placeholder_text=placeholder,
                     font=ctk.CTkFont(size=13), height=44,
                     corner_radius=RADIUS, border_color=OUTLINE, fg_color=WHITE)
    e.grid(row=row*2+1, column=0, sticky="ew", pady=(0, 16))
    if unit:
        ctk.CTkLabel(parent, text=unit, text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=11),
                     fg_color=SURFACE_CARD, corner_radius=RADIUS,
                     padx=8, pady=4).grid(row=row*2+1, column=1, padx=(4, 0), pady=(0, 16))
    return e


# ── Frame principale ──────────────────────────────────────────────────────────

class ShannonFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self._build()

    def _build(self):
        tabs = ctk.CTkTabview(self, fg_color="transparent",
                               segmented_button_fg_color=SURFACE_CARD,
                               segmented_button_selected_color=PRIMARY,
                               segmented_button_selected_hover_color=DEEP_NAVY,
                               segmented_button_unselected_color=SURFACE_CARD,
                               segmented_button_unselected_hover_color=OUTLINE,
                               text_color=ON_SURFACE)
        tabs.pack(fill="both", expand=True)
        tabs.add("Shannon")
        tabs.add("Nyquist")
        self._build_shannon(tabs.tab("Shannon"))
        self._build_nyquist(tabs.tab("Nyquist"))

    # ── Shannon ──────────────────────────────────────────────────────────────

    def _build_shannon(self, tab):
        tab.grid_columnconfigure(0, weight=5)
        tab.grid_columnconfigure(1, weight=4)
        tab.grid_rowconfigure(0, weight=1)

        # Carte gauche
        left = _card(tab, 0, (0, 8))
        body = _card_header(left, "⇄  Paramètres d'entrée")
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=0)

        self.e_s_bw  = _field(body, 0, "Bande passante (BP)", "Ex: 20", "Hz")
        self.e_s_snr = _field(body, 1, "Rapport Signal/Bruit (S/B)", "Ex: 30", "dB")

        ctk.CTkButton(body, text="▣  CALCULER", command=self._calc_shannon,
                       font=ctk.CTkFont(size=13, weight="bold"),
                       height=46, corner_radius=RADIUS,
                       fg_color=PRIMARY, hover_color=DEEP_NAVY).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(4, 0))

        # Formule
        formula_box = ctk.CTkFrame(left, fg_color=SURFACE_CARD, corner_radius=RADIUS)
        formula_box.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        formula_box.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(formula_box, text="ⓘ  FORMULE DE SHANNON-HARTLEY",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=ON_SURFACE_VAR).grid(row=0, column=0, sticky="w", padx=14, pady=(12, 6))

        formula_inner = ctk.CTkFrame(formula_box, fg_color=WHITE,
                                      corner_radius=RADIUS, border_width=1,
                                      border_color=OUTLINE)
        formula_inner.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 6))
        ctk.CTkLabel(formula_inner, text="C = BP × log₂(1 + S/N)",
                     font=ctk.CTkFont(size=13, slant="italic"),
                     text_color=ON_SURFACE).pack(padx=16, pady=10)

        for sym, desc in [("C",   "Capacité du canal (bps)"),
                           ("BP",  "Bande passante (Hz)"),
                           ("S/N", "Rapport Signal/Bruit (linéaire)")]:
            row_f = ctk.CTkFrame(formula_box, fg_color=SURFACE_CARD, corner_radius=0)
            row_f.grid(sticky="ew", padx=14)
            ctk.CTkLabel(row_f, text=f"• {sym} :", font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=PRIMARY, width=40).pack(side="left", padx=(8, 4), pady=2)
            ctk.CTkLabel(row_f, text=desc, font=ctk.CTkFont(size=11),
                         text_color=ON_SURFACE_VAR).pack(side="left")
        ctk.CTkFrame(formula_box, height=12, fg_color=SURFACE_CARD).grid()

        # Carte droite : résultats
        right = _card(tab, 1, (8, 0))
        rbody = _card_header(right, "▣  Résultats", ACCENT_AMBER)

        ctk.CTkLabel(rbody, text="DÉBIT MAXIMAL THÉORIQUE",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=ON_SURFACE_VAR).pack(pady=(8, 0))

        self.r_s_val = ctk.CTkLabel(rbody, text="—",
                                     font=ctk.CTkFont(size=42, weight="bold"),
                                     text_color=DEEP_NAVY)
        self.r_s_val.pack(pady=(4, 0))

        self.r_s_unit = ctk.CTkLabel(rbody, text="",
                                      font=ctk.CTkFont(size=16),
                                      text_color=ON_SURFACE_VAR)
        self.r_s_unit.pack(pady=(0, 20))

        ctk.CTkFrame(rbody, height=1, fg_color=OUTLINE).pack(fill="x", pady=(0, 16))

        details = ctk.CTkFrame(rbody, fg_color=WHITE, corner_radius=0)
        details.pack(fill="x")
        details.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(details, text="Efficacité spectrale :",
                     font=ctk.CTkFont(size=11), text_color=ON_SURFACE).grid(
            row=0, column=0, sticky="w", pady=5)
        self.r_s_eff = ctk.CTkLabel(details, text="—  bps/Hz",
                                     font=ctk.CTkFont(size=11), text_color=ON_SURFACE_VAR)
        self.r_s_eff.grid(row=0, column=1, sticky="e", pady=5)

        ctk.CTkLabel(details, text="S/N linéaire :",
                     font=ctk.CTkFont(size=11), text_color=ON_SURFACE).grid(
            row=1, column=0, sticky="w", pady=5)
        self.r_s_snr_lin = ctk.CTkLabel(details, text="—",
                                         font=ctk.CTkFont(size=11), text_color=ON_SURFACE_VAR)
        self.r_s_snr_lin.grid(row=1, column=1, sticky="e", pady=5)

        self.r_s_err = ctk.CTkLabel(rbody, text="", text_color=ERR,
                                     font=ctk.CTkFont(size=11))
        self.r_s_err.pack(pady=8)

    def _calc_shannon(self):
        try:
            B      = float(self.e_s_bw.get())
            snr_db = float(self.e_s_snr.get())
            snr    = snr_db_to_linear(snr_db)
            C      = shannon_capacity(B, snr)
            val, unit = format_bitrate(C)
            self.r_s_val.configure(text=val, text_color=DEEP_NAVY)
            self.r_s_unit.configure(text=unit)
            self.r_s_eff.configure(text=f"{C/B:.4f}  bps/Hz" if B else "—")
            self.r_s_snr_lin.configure(text=f"{snr:.4g}")
            self.r_s_err.configure(text="")
        except ValueError:
            self.r_s_val.configure(text="Erreur", text_color=ERR)
            self.r_s_unit.configure(text="")
            self.r_s_err.configure(text="Entrée invalide.")

    # ── Nyquist ──────────────────────────────────────────────────────────────

    def _build_nyquist(self, tab):
        tab.grid_columnconfigure(0, weight=5)
        tab.grid_columnconfigure(1, weight=4)
        tab.grid_rowconfigure(0, weight=1)

        left = _card(tab, 0, (0, 8))
        body = _card_header(left, "⇄  Paramètres d'entrée")
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=0)

        self.e_n_rm = _field(body, 0, "Rythme de modulation (Rm)", "Ex: 8000", "bauds")
        self.e_n_v  = _field(body, 1, "Valence (V)", "Ex: 8", "niv.")

        ctk.CTkButton(body, text="▣  CALCULER", command=self._calc_nyquist,
                       font=ctk.CTkFont(size=13, weight="bold"),
                       height=46, corner_radius=RADIUS,
                       fg_color=PRIMARY, hover_color=DEEP_NAVY).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(4, 0))

        # Boîte formule
        formula_box = ctk.CTkFrame(left, fg_color=SURFACE_CARD, corner_radius=RADIUS)
        formula_box.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        formula_box.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(formula_box, text="ⓘ  FORMULE DE NYQUIST",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=ON_SURFACE_VAR).grid(
            row=0, column=0, sticky="w", padx=14, pady=(12, 6))

        fi = ctk.CTkFrame(formula_box, fg_color=WHITE, corner_radius=RADIUS,
                           border_width=1, border_color=OUTLINE)
        fi.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 6))
        ctk.CTkLabel(fi, text="D = Rm · log₂(V)",
                     font=ctk.CTkFont(size=13, slant="italic"),
                     text_color=ON_SURFACE).pack(padx=16, pady=10)

        for sym, desc in [("D",  "Débit binaire (bit/s)"),
                           ("Rm", "Rythme de modulation (bauds)"),
                           ("V",  "Valence — nombre de niveaux")]:
            row_f = ctk.CTkFrame(formula_box, fg_color=SURFACE_CARD, corner_radius=0)
            row_f.grid(sticky="ew", padx=14)
            ctk.CTkLabel(row_f, text=f"• {sym} :", font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=PRIMARY, width=40).pack(side="left", padx=(8, 4), pady=2)
            ctk.CTkLabel(row_f, text=desc, font=ctk.CTkFont(size=11),
                         text_color=ON_SURFACE_VAR).pack(side="left")
        ctk.CTkFrame(formula_box, height=12, fg_color=SURFACE_CARD).grid()

        # Carte droite : résultats
        right = _card(tab, 1, (8, 0))
        rbody = _card_header(right, "▣  Résultats", ACCENT_AMBER)

        ctk.CTkLabel(rbody, text="DÉBIT BINAIRE",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=ON_SURFACE_VAR).pack(pady=(8, 0))

        self.r_n_val = ctk.CTkLabel(rbody, text="—",
                                     font=ctk.CTkFont(size=42, weight="bold"),
                                     text_color=DEEP_NAVY)
        self.r_n_val.pack(pady=(4, 0))

        self.r_n_unit = ctk.CTkLabel(rbody, text="",
                                      font=ctk.CTkFont(size=16),
                                      text_color=ON_SURFACE_VAR)
        self.r_n_unit.pack(pady=(0, 20))

        ctk.CTkFrame(rbody, height=1, fg_color=OUTLINE).pack(fill="x", pady=(0, 16))

        details = ctk.CTkFrame(rbody, fg_color=WHITE, corner_radius=0)
        details.pack(fill="x")
        details.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(details, text="Efficacité de codage :",
                     font=ctk.CTkFont(size=11), text_color=ON_SURFACE).grid(
            row=0, column=0, sticky="w", pady=4)
        self.r_n_eff = ctk.CTkLabel(details, text="—  bits/symbole",
                                     font=ctk.CTkFont(size=11), text_color=ON_SURFACE_VAR)
        self.r_n_eff.grid(row=0, column=1, sticky="e", pady=4)

        ctk.CTkLabel(details, text="Rm (bauds) :",
                     font=ctk.CTkFont(size=11), text_color=ON_SURFACE).grid(
            row=1, column=0, sticky="w", pady=4)
        self.r_n_rm = ctk.CTkLabel(details, text="—",
                                    font=ctk.CTkFont(size=11), text_color=ON_SURFACE_VAR)
        self.r_n_rm.grid(row=1, column=1, sticky="e", pady=4)

        self.r_n_err = ctk.CTkLabel(rbody, text="", text_color=ERR,
                                     font=ctk.CTkFont(size=11))
        self.r_n_err.pack(pady=8)

    def _calc_nyquist(self):
        try:
            Rm = float(self.e_n_rm.get())
            V  = int(self.e_n_v.get())
            D  = nyquist_debit(Rm, V)
            val, unit = format_bitrate(D)
            self.r_n_val.configure(text=val, text_color=DEEP_NAVY)
            self.r_n_unit.configure(text=unit)
            self.r_n_eff.configure(text=f"{math.log2(V):.4f}  bits/symbole")
            self.r_n_rm.configure(text=f"{Rm:,.0f} bauds")
            self.r_n_err.configure(text="")
        except ValueError as e:
            self.r_n_val.configure(text="Erreur", text_color=ERR)
            self.r_n_unit.configure(text="")
            self.r_n_err.configure(text=str(e) or "Entrée invalide.")
