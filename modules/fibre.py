import customtkinter as ctk

CARD = "#ffffff"
OK   = "#27ae60"
ERR  = "#e74c3c"
HINT = "#95a5a6"
TEXT = "#2c3e50"


# ── Calculs ──────────────────────────────────────────────────────────────────
# P_out = P_in - α·L - n_c·A_c - n_e·A_e
# Marge = P_out - P_sensibilité

def _pertes_fixes(n_c, A_c, n_e, A_e):
    return n_c * A_c + n_e * A_e

def calc_pout(pin, alpha, L, n_c, A_c, n_e, A_e):
    return pin - alpha * L - _pertes_fixes(n_c, A_c, n_e, A_e)

def calc_pin(pout, alpha, L, n_c, A_c, n_e, A_e):
    return pout + alpha * L + _pertes_fixes(n_c, A_c, n_e, A_e)

def calc_length(pin, pout, alpha, n_c, A_c, n_e, A_e):
    if alpha == 0:
        raise ValueError("L'atténuation α ne peut pas être nulle.")
    return (pin - pout - _pertes_fixes(n_c, A_c, n_e, A_e)) / alpha

def calc_marge(pout, p_sens):
    return pout - p_sens


# ── Définition des champs ─────────────────────────────────────────────────────

FIELDS = [
    ("P_in (dBm)",          "pin",    "Puissance d'émission",              "ex: 0"),
    ("α  (dB/km)",          "alpha",  "Atténuation linéique de la fibre",  "ex: 0.2"),
    ("L  (km)",             "L",      "Longueur du lien",                  "ex: 50"),
    ("n_c",                 "n_c",    "Nombre de connecteurs",             "ex: 4"),
    ("A_c  (dB)",           "A_c",    "Atténuation par connecteur",        "ex: 0.5"),
    ("n_e",                 "n_e",    "Nombre d'épissures",                "ex: 10"),
    ("A_e  (dB)",           "A_e",    "Atténuation par épissure",          "ex: 0.1"),
    ("P_sensibilité (dBm)", "p_sens", "Sensibilité récepteur (optionnel)", "ex: -30"),
    ("P_out (dBm)",         "pout",   "Puissance de sortie",               "ex: -15"),
]

CALCULABLE = {"pin", "L", "pout"}


# ── Frame principale ──────────────────────────────────────────────────────────

class FibreFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=CARD, corner_radius=0)
        self._build()

    def _build(self):
        # Scrollable pour ne pas couper les champs
        scroll = ctk.CTkScrollableFrame(self, fg_color=CARD, corner_radius=0)
        scroll.pack(fill="both", expand=True)
        scroll.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(scroll,
                     text="Laissez vide exactement un champ parmi : P_in, L ou P_out.",
                     font=ctk.CTkFont(size=10), text_color=HINT).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 18))

        self.entries: dict[str, ctk.CTkEntry] = {}
        for i, (label, key, hint, ph) in enumerate(FIELDS):
            row = i + 1
            ctk.CTkLabel(scroll, text=label, text_color=TEXT,
                         font=ctk.CTkFont(size=12), width=170, anchor="w").grid(
                row=row, column=0, sticky="w", pady=7)

            entry = ctk.CTkEntry(scroll, width=190, placeholder_text=ph,
                                  font=ctk.CTkFont(size=12))
            entry.grid(row=row, column=1, padx=14, sticky="w")

            ctk.CTkLabel(scroll, text=hint, text_color=HINT,
                         font=ctk.CTkFont(size=9)).grid(row=row, column=2, sticky="w")

            self.entries[key] = entry

        ctk.CTkButton(scroll, text="Calculer →", command=self._calculate,
                      width=160, font=ctk.CTkFont(size=12, weight="bold"),
                      height=38, corner_radius=8).grid(
            row=len(FIELDS) + 1, column=0, columnspan=2, sticky="w", pady=22)

        self.result = ctk.CTkLabel(scroll, text="",
                                    font=ctk.CTkFont(size=13, weight="bold"),
                                    text_color=OK, justify="left")
        self.result.grid(row=len(FIELDS) + 2, column=0, columnspan=3, sticky="w")

    def _get(self, key):
        v = self.entries[key].get().strip()
        return float(v) if v else None

    def _calculate(self):
        try:
            pin   = self._get("pin")
            alpha = self._get("alpha")
            L     = self._get("L")
            n_c   = self._get("n_c")   or 0
            A_c   = self._get("A_c")   or 0
            n_e   = self._get("n_e")   or 0
            A_e   = self._get("A_e")   or 0
            p_sens = self._get("p_sens")
            pout  = self._get("pout")

            empty = [k for k in CALCULABLE
                     if {"pin": pin, "L": L, "pout": pout}[k] is None]

            if len(empty) != 1:
                self.result.configure(
                    text="Laissez exactement un champ vide parmi : P_in, L, P_out.",
                    text_color=ERR)
                return

            lines = []
            target = empty[0]

            if target == "pout":
                pout = calc_pout(pin, alpha, L, n_c, A_c, n_e, A_e)
                lines.append(f"P_out = {pout:.3f} dBm")
            elif target == "pin":
                pin = calc_pin(pout, alpha, L, n_c, A_c, n_e, A_e)
                lines.append(f"P_in = {pin:.3f} dBm")
            elif target == "L":
                L = calc_length(pin, pout, alpha, n_c, A_c, n_e, A_e)
                if L < 0:
                    self.result.configure(
                        text="Longueur négative : vérifiez vos valeurs.", text_color=ERR)
                    return
                lines.append(f"L = {L:.3f} km")

            if p_sens is not None and pout is not None:
                m = calc_marge(pout, p_sens)
                lines.append(f"Marge système = {m:.3f} dB  [{'OK ✓' if m >= 0 else 'INSUFFISANTE ✗'}]")

            self.result.configure(text="\n".join(lines), text_color=OK)

        except ValueError as e:
            self.result.configure(text=str(e) or "Entrée invalide.", text_color=ERR)
        except TypeError:
            self.result.configure(text="Certains champs requis sont manquants.", text_color=ERR)
