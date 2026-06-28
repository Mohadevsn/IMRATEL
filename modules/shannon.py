import math
import customtkinter as ctk

CARD = "#ffffff"
OK   = "#27ae60"
ERR  = "#e74c3c"
HINT = "#95a5a6"
TEXT = "#2c3e50"


# ── Calculs ──────────────────────────────────────────────────────────────────

def shannon_capacity(bandwidth_hz: float, snr_linear: float) -> float:
    return bandwidth_hz * math.log2(1 + snr_linear)

def nyquist_capacity(bandwidth_hz: float, M: int) -> float:
    if M < 2:
        raise ValueError("M doit être ≥ 2.")
    return 2 * bandwidth_hz * math.log2(M)

def snr_db_to_linear(snr_db: float) -> float:
    return 10 ** (snr_db / 10)

def format_bitrate(bps: float) -> str:
    if bps >= 1e9:
        return f"{bps / 1e9:.4f} Gbit/s"
    if bps >= 1e6:
        return f"{bps / 1e6:.4f} Mbit/s"
    if bps >= 1e3:
        return f"{bps / 1e3:.4f} kbit/s"
    return f"{bps:.4f} bit/s"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _entry(parent, placeholder=""):
    return ctk.CTkEntry(parent, width=200, placeholder_text=placeholder,
                        font=ctk.CTkFont(size=12))

def _btn(parent, text, cmd):
    return ctk.CTkButton(parent, text=text, command=cmd, width=160,
                         font=ctk.CTkFont(size=12, weight="bold"), height=38, corner_radius=8)


# ── Frame principale ──────────────────────────────────────────────────────────

class ShannonFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=CARD, corner_radius=0)
        self._build()

    def _build(self):
        tabs = ctk.CTkTabview(self, fg_color=CARD)
        tabs.pack(fill="both", expand=True)
        tabs.add("Shannon")
        tabs.add("Nyquist")
        self._build_shannon(tabs.tab("Shannon"))
        self._build_nyquist(tabs.tab("Nyquist"))

    # ── Shannon ──────────────────────────────────────────────────────────────

    def _build_shannon(self, tab):
        f = ctk.CTkFrame(tab, fg_color=CARD)
        f.pack(padx=8, pady=16, anchor="w")

        ctk.CTkLabel(f, text="C = B · log₂(1 + S/B)",
                     font=ctk.CTkFont(size=13, slant="italic"),
                     text_color=HINT).grid(row=0, column=0, columnspan=2,
                                           sticky="w", pady=(0, 20))

        ctk.CTkLabel(f, text="Bande passante B (Hz) :", text_color=TEXT,
                     font=ctk.CTkFont(size=12)).grid(row=1, column=0, sticky="w", pady=10)
        self.e_s_bw = _entry(f, "ex: 4000")
        self.e_s_bw.grid(row=1, column=1, padx=16)

        ctk.CTkLabel(f, text="Rapport S/B (dB) :", text_color=TEXT,
                     font=ctk.CTkFont(size=12)).grid(row=2, column=0, sticky="w", pady=10)
        self.e_s_snr = _entry(f, "ex: 30")
        self.e_s_snr.grid(row=2, column=1, padx=16)

        _btn(f, "Calculer →", self._calc_shannon).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=22)

        self.r_shannon = ctk.CTkLabel(f, text="",
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       text_color=OK)
        self.r_shannon.grid(row=4, column=0, columnspan=2, sticky="w")

    def _calc_shannon(self):
        try:
            B = float(self.e_s_bw.get())
            C = shannon_capacity(B, snr_db_to_linear(float(self.e_s_snr.get())))
            self.r_shannon.configure(
                text=f"Débit max (Shannon) = {format_bitrate(C)}", text_color=OK)
        except ValueError:
            self.r_shannon.configure(text="Entrée invalide.", text_color=ERR)

    # ── Nyquist ──────────────────────────────────────────────────────────────

    def _build_nyquist(self, tab):
        f = ctk.CTkFrame(tab, fg_color=CARD)
        f.pack(padx=8, pady=16, anchor="w")

        ctk.CTkLabel(f, text="C = 2B · log₂(M)",
                     font=ctk.CTkFont(size=13, slant="italic"),
                     text_color=HINT).grid(row=0, column=0, columnspan=2,
                                           sticky="w", pady=(0, 20))

        ctk.CTkLabel(f, text="Bande passante B (Hz) :", text_color=TEXT,
                     font=ctk.CTkFont(size=12)).grid(row=1, column=0, sticky="w", pady=10)
        self.e_n_bw = _entry(f, "ex: 4000")
        self.e_n_bw.grid(row=1, column=1, padx=16)

        ctk.CTkLabel(f, text="Nombre de niveaux M :", text_color=TEXT,
                     font=ctk.CTkFont(size=12)).grid(row=2, column=0, sticky="w", pady=10)
        self.e_n_m = _entry(f, "ex: 8")
        self.e_n_m.grid(row=2, column=1, padx=16)

        _btn(f, "Calculer →", self._calc_nyquist).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=22)

        self.r_nyquist = ctk.CTkLabel(f, text="",
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       text_color=OK)
        self.r_nyquist.grid(row=4, column=0, columnspan=2, sticky="w")

    def _calc_nyquist(self):
        try:
            B = float(self.e_n_bw.get())
            M = int(self.e_n_m.get())
            self.r_nyquist.configure(
                text=f"Débit max (Nyquist) = {format_bitrate(nyquist_capacity(B, M))}",
                text_color=OK)
        except ValueError as e:
            self.r_nyquist.configure(text=str(e) or "Entrée invalide.", text_color=ERR)
