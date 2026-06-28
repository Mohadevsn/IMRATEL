import math
import customtkinter as ctk

PRIMARY        = "#0056B3"
DEEP_NAVY      = "#002D62"
SURFACE_CARD   = "#F2F3FC"
OUTLINE        = "#D9D9E2"
ON_SURFACE     = "#212529"
ON_SURFACE_VAR = "#495057"
OK             = "#27ae60"
ERR            = "#e74c3c"
DISABLED_BG    = "#e9ecef"
RADIUS         = 4


# ── Calculs ───────────────────────────────────────────────────────────────────

def db_to_linear(db: float) -> float:
    return 10 ** (db / 10)

def linear_to_db(linear: float) -> float:
    if linear <= 0:
        raise ValueError("La valeur linéaire doit être strictement positive.")
    return 10 * math.log10(linear)

def dbm_to_mw(dbm: float) -> float:
    return 10 ** (dbm / 10)

def mw_to_dbm(mw: float) -> float:
    if mw <= 0:
        raise ValueError("La puissance doit être strictement positive.")
    return 10 * math.log10(mw)


# ── Helpers UI ────────────────────────────────────────────────────────────────

def _make_entry(parent, placeholder, textvariable):
    return ctk.CTkEntry(parent, width=210, placeholder_text=placeholder,
                        textvariable=textvariable,
                        font=ctk.CTkFont(size=12),
                        corner_radius=RADIUS, border_color=OUTLINE,
                        fg_color="white")

def _make_btn(parent, text, cmd):
    return ctk.CTkButton(parent, text=text, command=cmd, width=160,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         height=38, corner_radius=RADIUS,
                         fg_color=PRIMARY, hover_color=DEEP_NAVY)

def _make_label(parent, text):
    return ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=12),
                        text_color=ON_SURFACE)

def _disable(entry: ctk.CTkEntry):
    entry.configure(state="disabled", fg_color=DISABLED_BG)

def _enable(entry: ctk.CTkEntry):
    entry.configure(state="normal", fg_color="white")


# ── Frame principale ──────────────────────────────────────────────────────────

class DecibelFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=SURFACE_CARD, corner_radius=0)
        self._build()

    def _build(self):
        tabs = ctk.CTkTabview(self, fg_color=SURFACE_CARD,
                               segmented_button_fg_color=OUTLINE,
                               segmented_button_selected_color=PRIMARY,
                               segmented_button_selected_hover_color=DEEP_NAVY,
                               segmented_button_unselected_color=OUTLINE,
                               segmented_button_unselected_hover_color="#c8cdd5",
                               text_color=ON_SURFACE,
                               text_color_disabled=ON_SURFACE_VAR)
        tabs.pack(fill="both", expand=True)
        tabs.add("dB ↔ Linéaire")
        tabs.add("dBm ↔ mW")
        self._build_db_linear(tabs.tab("dB ↔ Linéaire"))
        self._build_dbm_mw(tabs.tab("dBm ↔ mW"))

    # ── Onglet 1 : dB ↔ Linéaire ─────────────────────────────────────────────

    def _build_db_linear(self, tab):
        f = ctk.CTkFrame(tab, fg_color=SURFACE_CARD)
        f.pack(padx=8, pady=16, anchor="w")

        ctk.CTkLabel(f, text="Remplissez un seul champ — l'autre se désactive automatiquement.",
                     font=ctk.CTkFont(size=10), text_color=ON_SURFACE_VAR).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))

        _make_label(f, "Valeur en dB :").grid(row=1, column=0, sticky="w", pady=10)
        self.var_db = ctk.StringVar()
        self.e_db = _make_entry(f, "ex: 3", self.var_db)
        self.e_db.grid(row=1, column=1, padx=16)

        _make_label(f, "Valeur linéaire :").grid(row=2, column=0, sticky="w", pady=10)
        self.var_lin = ctk.StringVar()
        self.e_lin = _make_entry(f, "ex: 2", self.var_lin)
        self.e_lin.grid(row=2, column=1, padx=16)

        _make_btn(f, "Calculer →", self._calc_db_linear).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=22)

        self.r_db = ctk.CTkLabel(f, text="", font=ctk.CTkFont(size=14, weight="bold"),
                                  text_color=OK)
        self.r_db.grid(row=4, column=0, columnspan=2, sticky="w")

        # Désactivation mutuelle
        self.var_db.trace_add("write", self._on_db_change)
        self.var_lin.trace_add("write", self._on_lin_change)

    def _on_db_change(self, *_):
        if self.var_db.get():
            _disable(self.e_lin)
        else:
            _enable(self.e_lin)

    def _on_lin_change(self, *_):
        if self.var_lin.get():
            _disable(self.e_db)
        else:
            _enable(self.e_db)

    def _calc_db_linear(self):
        db, lin = self.var_db.get().strip(), self.var_lin.get().strip()
        try:
            if db and not lin:
                self.r_db.configure(
                    text=f"Valeur linéaire = {db_to_linear(float(db)):.6g}",
                    text_color=OK)
            elif lin and not db:
                self.r_db.configure(
                    text=f"Valeur en dB = {linear_to_db(float(lin)):.4f} dB",
                    text_color=OK)
            else:
                self.r_db.configure(text="Remplissez exactement un seul champ.",
                                    text_color=ERR)
        except ValueError as e:
            self.r_db.configure(text=str(e), text_color=ERR)

    # ── Onglet 2 : dBm ↔ mW ─────────────────────────────────────────────────

    def _build_dbm_mw(self, tab):
        f = ctk.CTkFrame(tab, fg_color=SURFACE_CARD)
        f.pack(padx=8, pady=16, anchor="w")

        ctk.CTkLabel(f, text="Remplissez un seul champ — l'autre se désactive automatiquement.",
                     font=ctk.CTkFont(size=10), text_color=ON_SURFACE_VAR).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))

        _make_label(f, "Valeur en dBm :").grid(row=1, column=0, sticky="w", pady=10)
        self.var_dbm = ctk.StringVar()
        self.e_dbm = _make_entry(f, "ex: 0", self.var_dbm)
        self.e_dbm.grid(row=1, column=1, padx=16)

        _make_label(f, "Valeur en mW :").grid(row=2, column=0, sticky="w", pady=10)
        self.var_mw = ctk.StringVar()
        self.e_mw = _make_entry(f, "ex: 1", self.var_mw)
        self.e_mw.grid(row=2, column=1, padx=16)

        _make_btn(f, "Calculer →", self._calc_dbm_mw).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=22)

        self.r_dbm = ctk.CTkLabel(f, text="", font=ctk.CTkFont(size=14, weight="bold"),
                                   text_color=OK)
        self.r_dbm.grid(row=4, column=0, columnspan=2, sticky="w")

        self.var_dbm.trace_add("write", self._on_dbm_change)
        self.var_mw.trace_add("write", self._on_mw_change)

    def _on_dbm_change(self, *_):
        if self.var_dbm.get():
            _disable(self.e_mw)
        else:
            _enable(self.e_mw)

    def _on_mw_change(self, *_):
        if self.var_mw.get():
            _disable(self.e_dbm)
        else:
            _enable(self.e_dbm)

    def _calc_dbm_mw(self):
        dbm, mw = self.var_dbm.get().strip(), self.var_mw.get().strip()
        try:
            if dbm and not mw:
                self.r_dbm.configure(
                    text=f"Puissance = {dbm_to_mw(float(dbm)):.6g} mW",
                    text_color=OK)
            elif mw and not dbm:
                self.r_dbm.configure(
                    text=f"Puissance = {mw_to_dbm(float(mw)):.4f} dBm",
                    text_color=OK)
            else:
                self.r_dbm.configure(text="Remplissez exactement un seul champ.",
                                     text_color=ERR)
        except ValueError as e:
            self.r_dbm.configure(text=str(e), text_color=ERR)
