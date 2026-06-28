import math
import customtkinter as ctk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

CARD = "#ffffff"
OK   = "#27ae60"
ERR  = "#e74c3c"
TEXT = "#2c3e50"


# ── Calculs ──────────────────────────────────────────────────────────────────

def calc_N(i: int, j: int) -> int:
    return i * i + i * j + j * j

def _hex_vertices(cx, cy, size):
    return [(cx + size * math.cos(math.radians(60 * k - 30)),
             cy + size * math.sin(math.radians(60 * k - 30))) for k in range(6)]

def _hex_grid(N, rings=3):
    dx, dy = math.sqrt(3), 1.5
    centers = []
    for q in range(-rings, rings + 1):
        for r in range(-rings, rings + 1):
            if abs(-q - r) <= rings:
                centers.append((dx * (q + r / 2), dy * r,
                                 (q * 3 + r * 7) % max(N, 1)))
    return centers


# ── Frame principale ──────────────────────────────────────────────────────────

class CellulairFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=CARD, corner_radius=0)
        self._build()

    def _build(self):
        # Barre de saisie en haut
        top = ctk.CTkFrame(self, fg_color=CARD)
        top.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(top, text="i :", text_color=TEXT,
                     font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 4))
        self.e_i = ctk.CTkEntry(top, width=70, placeholder_text="ex: 2",
                                 font=ctk.CTkFont(size=12))
        self.e_i.pack(side="left", padx=(0, 18))

        ctk.CTkLabel(top, text="j :", text_color=TEXT,
                     font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 4))
        self.e_j = ctk.CTkEntry(top, width=70, placeholder_text="ex: 1",
                                 font=ctk.CTkFont(size=12))
        self.e_j.pack(side="left", padx=(0, 24))

        ctk.CTkButton(top, text="Calculer et Afficher →", command=self._calculate,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      height=36, corner_radius=8, width=200).pack(side="left")

        self.result = ctk.CTkLabel(self, text="",
                                    font=ctk.CTkFont(size=13, weight="bold"),
                                    text_color=OK, justify="left")
        self.result.pack(anchor="w", pady=(0, 6))

        # Zone graphique
        self.plot_frame = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        self.plot_frame.pack(fill="both", expand=True)

    def _calculate(self):
        try:
            i, j = int(self.e_i.get()), int(self.e_j.get())
            if i < 0 or j < 0:
                raise ValueError("i et j doivent être ≥ 0.")
            if i == 0 and j == 0:
                raise ValueError("i et j ne peuvent pas être tous les deux nuls.")
            N = calc_N(i, j)
            self.result.configure(
                text=f"N = {i}² + {i}×{j} + {j}² = {N}   →   {N} cellules par cluster",
                text_color=OK)
            self._render(N)
        except ValueError as e:
            self.result.configure(text=str(e) or "Entrée invalide.", text_color=ERR)

    def _render(self, N):
        for w in self.plot_frame.winfo_children():
            w.destroy()

        cmap   = plt.get_cmap("tab20", max(N, 1))
        colors = [mcolors.to_hex(cmap(k % N)) for k in range(N)]

        fig, ax = plt.subplots(figsize=(6, 4.2), facecolor=CARD)
        ax.set_facecolor(CARD)

        for cx, cy, cid in _hex_grid(N, rings=3):
            patch = mpatches.Polygon(_hex_vertices(cx, cy, 0.92), closed=True,
                                     facecolor=colors[cid % N],
                                     edgecolor="white", linewidth=1.5)
            ax.add_patch(patch)
            ax.text(cx, cy, str(cid + 1), ha="center", va="center",
                    fontsize=8, fontweight="bold", color="white")

        ax.set_aspect("equal")
        ax.autoscale_view()
        ax.axis("off")
        ax.set_title(f"Motif de réutilisation — N = {N}",
                     fontsize=11, color=TEXT, pad=10)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()

        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)
