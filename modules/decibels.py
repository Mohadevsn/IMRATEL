import math
import customtkinter as ctk

CARD  = "#ffffff"
OK    = "#27ae60"
ERR   = "#e74c3c"
HINT  = "#95a5a6"
TEXT  = "#2c3e50"


# ── Calculs ──────────────────────────────────────────────────────────────────

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


# ── Helpers ───────────────────────────────────────────────────────────────────

def _entry(parent, placeholder=""):
    return ctk.CTkEntry(parent, width=200, placeholder_text=placeholder,
                        font=ctk.CTkFont(size=12))

def _btn(parent, text, cmd):
    return ctk.CTkButton(parent, text=text, command=cmd, width=160,
                         font=ctk.CTkFont(size=12, weight="bold"), height=38, corner_radius=8)

def _hint(parent, text):
    return ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=10),
                        text_color=HINT)

def _result_label(parent):
    return ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=OK)


# ── Frame principale ──────────────────────────────────────────────────────────

class DecibelFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=CARD, corner_radius=0)
        self._build()

    def _build(self):
        tabs = ctk.CTkTabview(self, fg_color=CARD)
        tabs.pack(fill="both", expand=True)

        tabs.add("dB ↔ Linéaire")
        tabs.add("dBm ↔ mW")

        self._build_db_linear(tabs.tab("dB ↔ Linéaire"))
        self._build_dbm_mw(tabs.tab("dBm ↔ mW"))

    # ── Onglet 1 ─────────────────────────────────────────────────────────────

    def _build_db_linear(self, tab):
        f = ctk.CTkFrame(tab, fg_color=CARD)
        f.pack(padx=8, pady=16, anchor="w")

        _hint(f, "Remplissez un seul champ — laissez l'autre vide.").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))

        ctk.CTkLabel(f, text="Valeur en dB :", text_color=TEXT,
                     font=ctk.CTkFont(size=12)).grid(row=1, column=0, sticky="w", pady=10)
        self.e_db = _entry(f, "ex: 3")
        self.e_db.grid(row=1, column=1, padx=16)

        ctk.CTkLabel(f, text="Valeur linéaire :", text_color=TEXT,
                     font=ctk.CTkFont(size=12)).grid(row=2, column=0, sticky="w", pady=10)
        self.e_lin = _entry(f, "ex: 2")
        self.e_lin.grid(row=2, column=1, padx=16)

        _btn(f, "Calculer →", self._calc_db_linear).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=22)

        self.r_db = _result_label(f)
        self.r_db.grid(row=4, column=0, columnspan=2, sticky="w")

    def _calc_db_linear(self):
        db, lin = self.e_db.get().strip(), self.e_lin.get().strip()
        try:
            if db and not lin:
                self.r_db.configure(text=f"Valeur linéaire = {db_to_linear(float(db)):.6g}",
                                    text_color=OK)
            elif lin and not db:
                self.r_db.configure(text=f"Valeur en dB = {linear_to_db(float(lin)):.4f} dB",
                                    text_color=OK)
            else:
                self.r_db.configure(text="Remplissez exactement un seul champ.", text_color=ERR)
        except ValueError as e:
            self.r_db.configure(text=str(e), text_color=ERR)

    # ── Onglet 2 ─────────────────────────────────────────────────────────────

    def _build_dbm_mw(self, tab):
        f = ctk.CTkFrame(tab, fg_color=CARD)
        f.pack(padx=8, pady=16, anchor="w")

        _hint(f, "Remplissez un seul champ — laissez l'autre vide.").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))

        ctk.CTkLabel(f, text="Valeur en dBm :", text_color=TEXT,
                     font=ctk.CTkFont(size=12)).grid(row=1, column=0, sticky="w", pady=10)
        self.e_dbm = _entry(f, "ex: 0")
        self.e_dbm.grid(row=1, column=1, padx=16)

        ctk.CTkLabel(f, text="Valeur en mW :", text_color=TEXT,
                     font=ctk.CTkFont(size=12)).grid(row=2, column=0, sticky="w", pady=10)
        self.e_mw = _entry(f, "ex: 1")
        self.e_mw.grid(row=2, column=1, padx=16)

        _btn(f, "Calculer →", self._calc_dbm_mw).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=22)

        self.r_dbm = _result_label(f)
        self.r_dbm.grid(row=4, column=0, columnspan=2, sticky="w")

    def _calc_dbm_mw(self):
        dbm, mw = self.e_dbm.get().strip(), self.e_mw.get().strip()
        try:
            if dbm and not mw:
                self.r_dbm.configure(text=f"Puissance = {dbm_to_mw(float(dbm)):.6g} mW",
                                     text_color=OK)
            elif mw and not dbm:
                self.r_dbm.configure(text=f"Puissance = {mw_to_dbm(float(mw)):.4f} dBm",
                                     text_color=OK)
            else:
                self.r_dbm.configure(text="Remplissez exactement un seul champ.", text_color=ERR)
        except ValueError as e:
            self.r_dbm.configure(text=str(e), text_color=ERR)
