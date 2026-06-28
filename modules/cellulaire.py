import math
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.colors as mcolors


# --- Fonctions de calcul ---

def calc_N(i: int, j: int) -> int:
    """Facteur de réutilisation N = i² + i·j + j²"""
    return i * i + i * j + j * j


def hexagon_vertices(cx: float, cy: float, size: float):
    """Retourne les 6 sommets d'un hexagone pointy-top centré en (cx, cy)."""
    angles = [math.radians(60 * k - 30) for k in range(6)]
    return [(cx + size * math.cos(a), cy + size * math.sin(a)) for a in angles]


def generate_hex_grid(N: int, rings: int = 3):
    """
    Génère les centres d'une grille hexagonale sur `rings` couronnes.
    Retourne une liste de (cx, cy, cluster_id).
    """
    size = 1.0
    dx = math.sqrt(3) * size
    dy = 1.5 * size

    centers = []
    for q in range(-rings, rings + 1):
        for r in range(-rings, rings + 1):
            s = -q - r
            if abs(s) <= rings:
                cx = dx * (q + r / 2)
                cy = dy * r
                cluster_id = _cluster_id(q, r, N)
                centers.append((cx, cy, cluster_id))
    return centers


def _cluster_id(q: int, r: int, N: int) -> int:
    """Assigne un identifiant de cluster (couleur) à chaque cellule."""
    if N == 0:
        return 0
    return (q * 3 + r * 7) % N


# --- Interface graphique ---

class CellulairFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f2f5")
        self._build()
        self._canvas_widget = None
        self._toolbar = None

    def _build(self):
        tk.Label(self, text="Dimensionnement Cellulaire",
                 font=("Helvetica", 16, "bold"), bg="#f0f2f5", fg="#1e2a38").pack(
            anchor="w", pady=(0, 15))

        form = tk.Frame(self, bg="#f0f2f5")
        form.pack(anchor="w")

        tk.Label(form, text="i :", bg="#f0f2f5", width=6, anchor="w").grid(
            row=0, column=0, sticky="w", pady=5)
        self.entry_i = tk.Entry(form, width=10)
        self.entry_i.grid(row=0, column=1, padx=10)

        tk.Label(form, text="j :", bg="#f0f2f5", width=6, anchor="w").grid(
            row=1, column=0, sticky="w", pady=5)
        self.entry_j = tk.Entry(form, width=10)
        self.entry_j.grid(row=1, column=1, padx=10)

        tk.Button(self, text="Calculer et Afficher →", command=self._calculate,
                  bg="#2c3e50", fg="white", relief=tk.FLAT, padx=15, pady=6,
                  cursor="hand2").pack(anchor="w", pady=12)

        self.result_label = tk.Label(self, text="", bg="#f0f2f5",
                                      font=("Helvetica", 13, "bold"), fg="#27ae60")
        self.result_label.pack(anchor="w", pady=(0, 10))

        self.plot_frame = tk.Frame(self, bg="#f0f2f5")
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    def _calculate(self):
        try:
            i = int(self.entry_i.get())
            j = int(self.entry_j.get())
            if i < 0 or j < 0:
                raise ValueError("i et j doivent être ≥ 0.")
            if i == 0 and j == 0:
                raise ValueError("i et j ne peuvent pas être tous les deux nuls.")

            N = calc_N(i, j)
            self.result_label.config(
                text=f"Facteur de réutilisation N = i² + i·j + j² = {i}² + {i}·{j} + {j}² = {N}",
                fg="#27ae60")
            self._draw_hexagonal_pattern(N)

        except ValueError as e:
            self.result_label.config(text=str(e) or "Entrée invalide.", fg="#e74c3c")

    def _draw_hexagonal_pattern(self, N: int):
        # Nettoyer l'affichage précédent
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        centers = generate_hex_grid(N, rings=3)
        size = 0.9

        cmap = plt.get_cmap("tab20", max(N, 1))
        colors = [mcolors.to_hex(cmap(k % N)) for k in range(N)]

        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor("#f0f2f5")
        ax.set_facecolor("#f0f2f5")

        for cx, cy, cid in centers:
            verts = hexagon_vertices(cx, cy, size)
            patch = mpatches.Polygon(verts, closed=True,
                                     facecolor=colors[cid % N] if N > 0 else "#3498db",
                                     edgecolor="white", linewidth=1.2)
            ax.add_patch(patch)
            ax.text(cx, cy, str(cid + 1), ha="center", va="center",
                    fontsize=7, fontweight="bold", color="white")

        ax.set_aspect("equal")
        ax.autoscale_view()
        ax.axis("off")
        ax.set_title(f"Motif hexagonal — N = {N}", fontsize=12, color="#1e2a38")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        plt.close(fig)
