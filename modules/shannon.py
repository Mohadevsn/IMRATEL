import math
import tkinter as tk
from tkinter import ttk


# --- Fonctions de calcul ---

def shannon_capacity(bandwidth_hz: float, snr_linear: float) -> float:
    """C = B · log2(1 + S/B)  [bit/s]"""
    return bandwidth_hz * math.log2(1 + snr_linear)


def nyquist_capacity(bandwidth_hz: float, M: int) -> float:
    """C = 2B · log2(M)  [bit/s]"""
    if M < 2:
        raise ValueError("M doit être ≥ 2.")
    return 2 * bandwidth_hz * math.log2(M)


def snr_db_to_linear(snr_db: float) -> float:
    return 10 ** (snr_db / 10)


def format_bitrate(bps: float) -> str:
    if bps >= 1e9:
        return f"{bps / 1e9:.4f} Gbit/s"
    elif bps >= 1e6:
        return f"{bps / 1e6:.4f} Mbit/s"
    elif bps >= 1e3:
        return f"{bps / 1e3:.4f} kbit/s"
    return f"{bps:.4f} bit/s"


# --- Interface graphique ---

class ShannonFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f2f5")
        self._build()

    def _build(self):
        tk.Label(self, text="Shannon / Nyquist", font=("Helvetica", 16, "bold"),
                 bg="#f0f2f5", fg="#1e2a38").pack(anchor="w", pady=(0, 20))

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        tab_shannon = tk.Frame(notebook, bg="#f0f2f5")
        notebook.add(tab_shannon, text="Shannon")
        self._build_shannon(tab_shannon)

        tab_nyquist = tk.Frame(notebook, bg="#f0f2f5")
        notebook.add(tab_nyquist, text="Nyquist")
        self._build_nyquist(tab_nyquist)

    def _build_shannon(self, parent):
        frame = tk.Frame(parent, bg="#f0f2f5")
        frame.pack(padx=20, pady=20, anchor="w")

        tk.Label(frame, text="Formule : C = B · log₂(1 + S/B)",
                 bg="#f0f2f5", font=("Helvetica", 10, "italic"), fg="#555").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))

        fields = [
            ("Bande passante B (Hz) :", "shannon_bw"),
            ("Rapport S/B en dB :", "shannon_snr_db"),
        ]
        self.shannon_entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label, bg="#f0f2f5").grid(row=i+1, column=0, sticky="w", pady=5)
            entry = tk.Entry(frame, width=20)
            entry.grid(row=i+1, column=1, padx=10)
            self.shannon_entries[key] = entry

        tk.Button(frame, text="Calculer →", command=self._calc_shannon,
                  bg="#2c3e50", fg="white", relief=tk.FLAT, padx=15, pady=6,
                  cursor="hand2").grid(row=3, column=0, columnspan=2, pady=15)

        self.result_shannon = tk.Label(frame, text="", bg="#f0f2f5", fg="#27ae60",
                                        font=("Helvetica", 12, "bold"))
        self.result_shannon.grid(row=4, column=0, columnspan=2)

    def _calc_shannon(self):
        try:
            B = float(self.shannon_entries["shannon_bw"].get())
            snr_db = float(self.shannon_entries["shannon_snr_db"].get())
            snr = snr_db_to_linear(snr_db)
            C = shannon_capacity(B, snr)
            self.result_shannon.config(
                text=f"Débit max (Shannon) = {format_bitrate(C)}", fg="#27ae60")
        except ValueError:
            self.result_shannon.config(text="Entrée invalide.", fg="#e74c3c")

    def _build_nyquist(self, parent):
        frame = tk.Frame(parent, bg="#f0f2f5")
        frame.pack(padx=20, pady=20, anchor="w")

        tk.Label(frame, text="Formule : C = 2B · log₂(M)",
                 bg="#f0f2f5", font=("Helvetica", 10, "italic"), fg="#555").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))

        fields = [
            ("Bande passante B (Hz) :", "nyquist_bw"),
            ("Nombre de niveaux M :", "nyquist_m"),
        ]
        self.nyquist_entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label, bg="#f0f2f5").grid(row=i+1, column=0, sticky="w", pady=5)
            entry = tk.Entry(frame, width=20)
            entry.grid(row=i+1, column=1, padx=10)
            self.nyquist_entries[key] = entry

        tk.Button(frame, text="Calculer →", command=self._calc_nyquist,
                  bg="#2c3e50", fg="white", relief=tk.FLAT, padx=15, pady=6,
                  cursor="hand2").grid(row=3, column=0, columnspan=2, pady=15)

        self.result_nyquist = tk.Label(frame, text="", bg="#f0f2f5", fg="#27ae60",
                                        font=("Helvetica", 12, "bold"))
        self.result_nyquist.grid(row=4, column=0, columnspan=2)

    def _calc_nyquist(self):
        try:
            B = float(self.nyquist_entries["nyquist_bw"].get())
            M = int(self.nyquist_entries["nyquist_m"].get())
            C = nyquist_capacity(B, M)
            self.result_nyquist.config(
                text=f"Débit max (Nyquist) = {format_bitrate(C)}", fg="#27ae60")
        except ValueError as e:
            self.result_nyquist.config(text=str(e) or "Entrée invalide.", fg="#e74c3c")
