import tkinter as tk
from tkinter import ttk


# --- Fonctions de calcul ---
# Bilan de liaison fibre : P_out = P_in - alpha*L - n_c*A_c - n_e*A_e
# Marge = P_out - P_sensibilite

def _pertes_fixes(n_c: float, A_c: float, n_e: float, A_e: float) -> float:
    return n_c * A_c + n_e * A_e


def calc_pout(pin, alpha, L, n_c, A_c, n_e, A_e):
    return pin - alpha * L - _pertes_fixes(n_c, A_c, n_e, A_e)


def calc_pin(pout, alpha, L, n_c, A_c, n_e, A_e):
    return pout + alpha * L + _pertes_fixes(n_c, A_c, n_e, A_e)


def calc_length(pin, pout, alpha, n_c, A_c, n_e, A_e):
    pertes = _pertes_fixes(n_c, A_c, n_e, A_e)
    denom = alpha
    if denom == 0:
        raise ValueError("L'atténuation α ne peut pas être nulle.")
    return (pin - pout - pertes) / denom


def calc_marge(pout, p_sensibilite):
    return pout - p_sensibilite


# --- Interface graphique ---

FIELDS = [
    ("P_in (dBm)", "pin", "Puissance d'émission"),
    ("α (dB/km)", "alpha", "Atténuation linéique de la fibre"),
    ("L (km)", "L", "Longueur du lien"),
    ("n_c", "n_c", "Nombre de connecteurs"),
    ("A_c (dB)", "A_c", "Atténuation par connecteur"),
    ("n_e", "n_e", "Nombre d'épissures"),
    ("A_e (dB)", "A_e", "Atténuation par épissure"),
    ("P_sensibilité (dBm)", "p_sens", "Sensibilité du récepteur"),
    ("P_out (dBm)", "pout", "Puissance en sortie (à calculer)"),
]

CALCULABLE = {"pin", "L", "pout"}


class FibreFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f2f5")
        self._build()

    def _build(self):
        tk.Label(self, text="Bilan de Liaison Fibre Optique",
                 font=("Helvetica", 16, "bold"), bg="#f0f2f5", fg="#1e2a38").pack(
            anchor="w", pady=(0, 5))

        tk.Label(self,
                 text="Laissez vide la variable à calculer (P_out, P_in ou L).",
                 bg="#f0f2f5", font=("Helvetica", 10, "italic"), fg="#555").pack(anchor="w", pady=(0, 15))

        form = tk.Frame(self, bg="#f0f2f5")
        form.pack(anchor="w")

        self.entries = {}
        for i, (label, key, tooltip) in enumerate(FIELDS):
            tk.Label(form, text=label, bg="#f0f2f5", width=22, anchor="w").grid(
                row=i, column=0, sticky="w", pady=4)
            entry = tk.Entry(form, width=18)
            entry.grid(row=i, column=1, padx=10)
            tk.Label(form, text=tooltip, bg="#f0f2f5", fg="#888",
                     font=("Helvetica", 8)).grid(row=i, column=2, sticky="w")
            self.entries[key] = entry

        tk.Button(self, text="Calculer →", command=self._calculate,
                  bg="#2c3e50", fg="white", relief=tk.FLAT, padx=15, pady=6,
                  cursor="hand2").pack(anchor="w", pady=15)

        self.result_label = tk.Label(self, text="", bg="#f0f2f5",
                                      font=("Helvetica", 12, "bold"), fg="#27ae60",
                                      justify=tk.LEFT)
        self.result_label.pack(anchor="w")

    def _get(self, key):
        val = self.entries[key].get().strip()
        return float(val) if val else None

    def _calculate(self):
        try:
            pin = self._get("pin")
            alpha = self._get("alpha")
            L = self._get("L")
            n_c = self._get("n_c")
            A_c = self._get("A_c")
            n_e = self._get("n_e")
            A_e = self._get("A_e")
            p_sens = self._get("p_sens")
            pout = self._get("pout")

            # Valeurs par défaut si pertes fixes non renseignées
            n_c = n_c or 0
            A_c = A_c or 0
            n_e = n_e or 0
            A_e = A_e or 0

            empty = [k for k in CALCULABLE
                     if {"pin": pin, "L": L, "pout": pout}[k] is None]

            if len(empty) != 1:
                self.result_label.config(
                    text="Laissez exactement un champ vide parmi : P_in, L, P_out.",
                    fg="#e74c3c")
                return

            target = empty[0]
            lines = []

            if target == "pout":
                pout = calc_pout(pin, alpha, L, n_c, A_c, n_e, A_e)
                lines.append(f"P_out = {pout:.3f} dBm")
            elif target == "pin":
                pin = calc_pin(pout, alpha, L, n_c, A_c, n_e, A_e)
                lines.append(f"P_in = {pin:.3f} dBm")
            elif target == "L":
                L = calc_length(pin, pout, alpha, n_c, A_c, n_e, A_e)
                if L < 0:
                    self.result_label.config(
                        text="Longueur négative : vérifiez vos valeurs.", fg="#e74c3c")
                    return
                lines.append(f"L = {L:.3f} km")

            if p_sens is not None and pout is not None:
                marge = calc_marge(pout, p_sens)
                etat = "OK" if marge >= 0 else "INSUFFISANTE"
                lines.append(f"Marge système = {marge:.3f} dB  [{etat}]")

            self.result_label.config(text="\n".join(lines), fg="#27ae60")

        except ValueError as e:
            self.result_label.config(text=str(e) or "Entrée invalide.", fg="#e74c3c")
        except TypeError:
            self.result_label.config(
                text="Certains champs requis sont manquants.", fg="#e74c3c")
