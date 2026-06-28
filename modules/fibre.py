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


# ── Champs du formulaire ──────────────────────────────────────────────────────

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

# Les 3 champs mutuellement exclusifs : exactement 1 doit rester vide
CALCULABLE = ["pin", "L", "pout"]


# ── Frame principale ──────────────────────────────────────────────────────────

class FibreFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=SURFACE_CARD, corner_radius=0)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color=SURFACE_CARD, corner_radius=0)
        scroll.pack(fill="both", expand=True)
        scroll.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(scroll,
                     text="Parmi P_in, L et P_out : remplissez-en deux — le troisième se désactive.",
                     font=ctk.CTkFont(size=10), text_color=ON_SURFACE_VAR).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 18))

        self.vars: dict[str, ctk.StringVar] = {}
        self.entries: dict[str, ctk.CTkEntry] = {}

        for i, (label, key, hint, ph) in enumerate(FIELDS):
            row = i + 1
            ctk.CTkLabel(scroll, text=label, text_color=ON_SURFACE,
                         font=ctk.CTkFont(size=12), width=180, anchor="w").grid(
                row=row, column=0, sticky="w", pady=7)

            var = ctk.StringVar()
            entry = ctk.CTkEntry(scroll, width=200, placeholder_text=ph,
                                  textvariable=var, font=ctk.CTkFont(size=12),
                                  corner_radius=RADIUS, border_color=OUTLINE,
                                  fg_color="white")
            entry.grid(row=row, column=1, padx=14, sticky="w")

            ctk.CTkLabel(scroll, text=hint, text_color=ON_SURFACE_VAR,
                         font=ctk.CTkFont(size=9)).grid(row=row, column=2, sticky="w")

            self.vars[key] = var
            self.entries[key] = entry

            # Trace uniquement sur les 3 champs calculables
            if key in CALCULABLE:
                var.trace_add("write", self._on_calculable_change)

        ctk.CTkButton(scroll, text="Calculer →", command=self._calculate,
                      width=160, font=ctk.CTkFont(size=12, weight="bold"),
                      height=38, corner_radius=RADIUS,
                      fg_color=PRIMARY, hover_color=DEEP_NAVY).grid(
            row=len(FIELDS) + 1, column=0, columnspan=2, sticky="w", pady=22)

        self.result = ctk.CTkLabel(scroll, text="",
                                    font=ctk.CTkFont(size=13, weight="bold"),
                                    text_color=OK, justify="left")
        self.result.grid(row=len(FIELDS) + 2, column=0, columnspan=3, sticky="w")

    def _on_calculable_change(self, *_):
        """Quand 2 des 3 champs calculables sont remplis, désactive le 3ème."""
        filled = [k for k in CALCULABLE if self.vars[k].get().strip()]

        if len(filled) == 2:
            empty_key = next(k for k in CALCULABLE if k not in filled)
            for k in CALCULABLE:
                if k == empty_key:
                    self.entries[k].configure(state="disabled", fg_color=DISABLED_BG)
                else:
                    self.entries[k].configure(state="normal", fg_color="white")
        else:
            # Moins de 2 remplis : tout réactiver
            for k in CALCULABLE:
                self.entries[k].configure(state="normal", fg_color="white")

    def _get(self, key):
        v = self.vars[key].get().strip()
        return float(v) if v else None

    def _calculate(self):
        try:
            pin    = self._get("pin")
            alpha  = self._get("alpha")
            L      = self._get("L")
            n_c    = self._get("n_c")    or 0
            A_c    = self._get("A_c")    or 0
            n_e    = self._get("n_e")    or 0
            A_e    = self._get("A_e")    or 0
            p_sens = self._get("p_sens")
            pout   = self._get("pout")

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
                lines.append(
                    f"Marge système = {m:.3f} dB  [{'OK ✓' if m >= 0 else 'INSUFFISANTE ✗'}]")

            self.result.configure(text="\n".join(lines), text_color=OK)

        except ValueError as e:
            self.result.configure(text=str(e) or "Entrée invalide.", text_color=ERR)
        except TypeError:
            self.result.configure(text="Certains champs requis sont manquants.", text_color=ERR)
