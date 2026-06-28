import math
import customtkinter as ctk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

PRIMARY        = "#0056B3"
DEEP_NAVY      = "#002D62"
ACCENT_AMBER   = "#F89406"
SURFACE_CARD   = "#F2F3FC"
OUTLINE        = "#D9D9E2"
ON_SURFACE     = "#212529"
ON_SURFACE_VAR = "#495057"
WHITE          = "#ffffff"
OK             = "#27ae60"
ERR            = "#e74c3c"
RADIUS         = 4


# ── Calculs ───────────────────────────────────────────────────────────────────

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
                is_center = (q == 0 and r == 0)
                cid = (q * 3 + r * 7) % max(N, 1)
                centers.append((dx * (q + r / 2), dy * r, cid, is_center))
    return centers


# ── Frame principale ──────────────────────────────────────────────────────────

class CellulairFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)

        # ── Carte gauche : paramètres ─────────────────────────────────────────
        left = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=RADIUS,
                             border_width=1, border_color=OUTLINE)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)

        h = ctk.CTkFrame(left, fg_color=WHITE, corner_radius=0)
        h.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 14))
        ctk.CTkLabel(h, text="⇄  Paramètres du Réseau",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=ON_SURFACE).pack(side="left")
        ctk.CTkFrame(left, height=1, fg_color=OUTLINE).grid(
            row=1, column=0, sticky="ew")

        body = ctk.CTkFrame(left, fg_color=WHITE, corner_radius=0)
        body.grid(row=2, column=0, sticky="nsew", padx=20, pady=16)
        body.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(body, text="PARAMÈTRE I  (DÉCALAGE HORIZONTAL)",
                     text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=9, weight="bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 4))
        self.e_i = ctk.CTkEntry(body, placeholder_text="2",
                                 font=ctk.CTkFont(size=13), height=44,
                                 corner_radius=RADIUS, border_color=OUTLINE, fg_color=WHITE)
        self.e_i.grid(row=1, column=0, sticky="ew", pady=(0, 16))

        ctk.CTkLabel(body, text="PARAMÈTRE J  (DÉCALAGE ANGULAIRE)",
                     text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=9, weight="bold")).grid(
            row=2, column=0, sticky="w", pady=(0, 4))
        self.e_j = ctk.CTkEntry(body, placeholder_text="1",
                                 font=ctk.CTkFont(size=13), height=44,
                                 corner_radius=RADIUS, border_color=OUTLINE, fg_color=WHITE)
        self.e_j.grid(row=3, column=0, sticky="ew", pady=(0, 20))

        ctk.CTkButton(body, text="▣  CALCULER", command=self._calculate,
                       font=ctk.CTkFont(size=12, weight="bold"),
                       height=44, corner_radius=RADIUS,
                       fg_color=ACCENT_AMBER, hover_color="#d4830a",
                       text_color=WHITE).grid(row=4, column=0, sticky="ew")

        # Résultat N
        self.n_result_frame = ctk.CTkFrame(left, fg_color=DEEP_NAVY, corner_radius=RADIUS)
        self.n_result_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(12, 0))
        self.n_result_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.n_result_frame, text="TAILLE DU MOTIF CALCULÉE",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color="#8ab4d4").grid(row=0, column=0, sticky="w", padx=14, pady=(10, 2))
        self.r_N = ctk.CTkLabel(self.n_result_frame, text="N = —",
                                 font=ctk.CTkFont(size=28, weight="bold"),
                                 text_color=WHITE)
        self.r_N.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 12))

        # Rappel formule
        formula_box = ctk.CTkFrame(left, fg_color=SURFACE_CARD, corner_radius=RADIUS)
        formula_box.grid(row=4, column=0, sticky="ew", padx=20, pady=(12, 20))
        formula_box.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(formula_box,
                     text="Rappel : La taille du motif est\ndonnée par la formule",
                     font=ctk.CTkFont(size=10), text_color=ON_SURFACE_VAR,
                     justify="left").grid(row=0, column=0, sticky="w", padx=12, pady=(10, 4))
        ctk.CTkLabel(formula_box, text="N = i² + ij + j²",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=PRIMARY).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 10))

        self.r_err = ctk.CTkLabel(left, text="", font=ctk.CTkFont(size=11),
                                   text_color=ERR, wraplength=180)
        self.r_err.grid(row=5, column=0, padx=20, pady=(0, 8))

        # ── Carte droite : schéma hexagonal ──────────────────────────────────
        right = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=RADIUS,
                              border_width=1, border_color=OUTLINE)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        rh = ctk.CTkFrame(right, fg_color=WHITE, corner_radius=0)
        rh.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 14))
        ctk.CTkLabel(rh,
                     text="SCHÉMATIQUE DE RÉUTILISATION  (TOPOLOGIE HEXAGONALE)",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=ON_SURFACE_VAR).pack(side="left")
        ctk.CTkFrame(right, height=1, fg_color=OUTLINE).grid(
            row=1, column=0, sticky="ew")

        self.plot_frame = ctk.CTkFrame(right, fg_color=WHITE, corner_radius=0)
        self.plot_frame.grid(row=2, column=0, sticky="nsew")

        # Légende
        leg = ctk.CTkFrame(right, fg_color=WHITE, corner_radius=0)
        leg.grid(row=3, column=0, sticky="ew", padx=20, pady=(8, 16))
        for color, label in [(PRIMARY, "Cellule Centrale"),
                              (ACCENT_AMBER, "Co-Canal"),
                              (SURFACE_CARD, "Frontière Cluster")]:
            dot = ctk.CTkFrame(leg, width=14, height=14, fg_color=color,
                                corner_radius=2)
            dot.pack(side="left", padx=(0, 4))
            ctk.CTkLabel(leg, text=label, font=ctk.CTkFont(size=10),
                         text_color=ON_SURFACE).pack(side="left", padx=(0, 20))

    def _calculate(self):
        try:
            i, j = int(self.e_i.get()), int(self.e_j.get())
            if i < 0 or j < 0:
                raise ValueError("i et j doivent être ≥ 0.")
            if i == 0 and j == 0:
                raise ValueError("i et j ne peuvent pas être tous les deux nuls.")
            N = calc_N(i, j)
            self.r_N.configure(text=f"N = {N}")
            self.r_err.configure(text="")
            self._render(N)
        except ValueError as e:
            self.r_err.configure(text=str(e) or "Entrée invalide.")

    def _render(self, N):
        for w in self.plot_frame.winfo_children():
            w.destroy()

        ref_cid = 0  # cid de la cellule centrale (q=0, r=0) est toujours 0

        fig, ax = plt.subplots(figsize=(6, 5), facecolor=WHITE)
        ax.set_facecolor(WHITE)

        for cx, cy, cid, is_center in _hex_grid(N, rings=3):
            if is_center:
                face  = PRIMARY
                edge  = WHITE
                tc    = WHITE
                lw    = 2.0
            elif cid == ref_cid:
                face  = ACCENT_AMBER
                edge  = WHITE
                tc    = WHITE
                lw    = 1.5
            else:
                face  = SURFACE_CARD
                edge  = OUTLINE
                tc    = ON_SURFACE
                lw    = 1.0

            patch = mpatches.Polygon(_hex_vertices(cx, cy, 0.92), closed=True,
                                     facecolor=face, edgecolor=edge, linewidth=lw)
            ax.add_patch(patch)
            ax.text(cx, cy, str(cid + 1), ha="center", va="center",
                    fontsize=8, fontweight="bold", color=tc)

        ax.set_aspect("equal")
        ax.autoscale_view()
        ax.axis("off")
        fig.tight_layout(pad=0.5)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)
