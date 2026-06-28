import math
import tkinter as tk
from tkinter import ttk


# --- Fonctions de calcul ---

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


# --- Interface graphique ---

class DecibelFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f2f5")
        self._build()

    def _build(self):
        tk.Label(self, text="Conversion Décibels", font=("Helvetica", 16, "bold"),
                 bg="#f0f2f5", fg="#1e2a38").pack(anchor="w", pady=(0, 20))

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Onglet dB <-> linéaire
        tab_db = tk.Frame(notebook, bg="#f0f2f5")
        notebook.add(tab_db, text="dB ↔ Linéaire")
        self._build_db_linear(tab_db)

        # Onglet dBm <-> mW
        tab_dbm = tk.Frame(notebook, bg="#f0f2f5")
        notebook.add(tab_dbm, text="dBm ↔ mW")
        self._build_dbm_mw(tab_dbm)

    def _build_db_linear(self, parent):
        frame = tk.Frame(parent, bg="#f0f2f5")
        frame.pack(padx=20, pady=20, anchor="w")

        tk.Label(frame, text="Valeur en dB :", bg="#f0f2f5").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_db = tk.Entry(frame, width=20)
        self.entry_db.grid(row=0, column=1, padx=10)

        tk.Label(frame, text="Valeur linéaire :", bg="#f0f2f5").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_linear = tk.Entry(frame, width=20)
        self.entry_linear.grid(row=1, column=1, padx=10)

        tk.Button(frame, text="Calculer →", command=self._calc_db_linear,
                  bg="#2c3e50", fg="white", relief=tk.FLAT, padx=15, pady=6,
                  cursor="hand2").grid(row=2, column=0, columnspan=2, pady=15)

        self.result_db = tk.Label(frame, text="", bg="#f0f2f5", fg="#27ae60",
                                   font=("Helvetica", 12, "bold"))
        self.result_db.grid(row=3, column=0, columnspan=2)

    def _calc_db_linear(self):
        db_val = self.entry_db.get().strip()
        lin_val = self.entry_linear.get().strip()
        try:
            if db_val and not lin_val:
                result = db_to_linear(float(db_val))
                self.result_db.config(text=f"Valeur linéaire = {result:.6g}", fg="#27ae60")
            elif lin_val and not db_val:
                result = linear_to_db(float(lin_val))
                self.result_db.config(text=f"Valeur en dB = {result:.4f} dB", fg="#27ae60")
            else:
                self.result_db.config(text="Remplissez exactement un seul champ.", fg="#e74c3c")
        except ValueError as e:
            self.result_db.config(text=str(e), fg="#e74c3c")

    def _build_dbm_mw(self, parent):
        frame = tk.Frame(parent, bg="#f0f2f5")
        frame.pack(padx=20, pady=20, anchor="w")

        tk.Label(frame, text="Valeur en dBm :", bg="#f0f2f5").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_dbm = tk.Entry(frame, width=20)
        self.entry_dbm.grid(row=0, column=1, padx=10)

        tk.Label(frame, text="Valeur en mW :", bg="#f0f2f5").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_mw = tk.Entry(frame, width=20)
        self.entry_mw.grid(row=1, column=1, padx=10)

        tk.Button(frame, text="Calculer →", command=self._calc_dbm_mw,
                  bg="#2c3e50", fg="white", relief=tk.FLAT, padx=15, pady=6,
                  cursor="hand2").grid(row=2, column=0, columnspan=2, pady=15)

        self.result_dbm = tk.Label(frame, text="", bg="#f0f2f5", fg="#27ae60",
                                    font=("Helvetica", 12, "bold"))
        self.result_dbm.grid(row=3, column=0, columnspan=2)

    def _calc_dbm_mw(self):
        dbm_val = self.entry_dbm.get().strip()
        mw_val = self.entry_mw.get().strip()
        try:
            if dbm_val and not mw_val:
                result = dbm_to_mw(float(dbm_val))
                self.result_dbm.config(text=f"Puissance = {result:.6g} mW", fg="#27ae60")
            elif mw_val and not dbm_val:
                result = mw_to_dbm(float(mw_val))
                self.result_dbm.config(text=f"Puissance = {result:.4f} dBm", fg="#27ae60")
            else:
                self.result_dbm.config(text="Remplissez exactement un seul champ.", fg="#e74c3c")
        except ValueError as e:
            self.result_dbm.config(text=str(e), fg="#e74c3c")
