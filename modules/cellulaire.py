import math
import customtkinter as ctk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

PRIMARY        = "#0056B3"
DEEP_NAVY      = "#002D62"
ACCENT_AMBER   = "#F89406"
SURFACE_CARD   = "#F2F3FC"
OUTLINE        = "#D9D9E2"
ON_SURFACE     = "#212529"
ON_SURFACE_VAR = "#495057"
WHITE          = "#ffffff"
MUTED          = "#9aa5b1"
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

        # ── Carte gauche ──────────────────────────────────────────────────────
        left = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=RADIUS,
                             border_width=1, border_color=OUTLINE)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(2, weight=1)

        h = ctk.CTkFrame(left, fg_color=WHITE, corner_radius=0)
        h.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 14))
        ctk.CTkLabel(h, text="⇄  Paramètres du Réseau",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=ON_SURFACE).pack(side="left")
        ctk.CTkFrame(left, height=1, fg_color=OUTLINE).grid(row=1, column=0, sticky="ew")

        # Scrollable body to fit all fields
        scroll = ctk.CTkScrollableFrame(left, fg_color=WHITE, corner_radius=0,
                                         scrollbar_button_color=OUTLINE,
                                         scrollbar_button_hover_color=PRIMARY)
        scroll.grid(row=2, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        # ── Entrées obligatoires ──────────────────────────────────────────────
        ctk.CTkLabel(scroll, text="PARAMÈTRE I  (DÉCALAGE HORIZONTAL)",
                     text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=9, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=20, pady=(16, 4))
        self.e_i = ctk.CTkEntry(scroll, placeholder_text="ex : 2",
                                 font=ctk.CTkFont(size=13), height=38,
                                 corner_radius=RADIUS, border_color=OUTLINE, fg_color=WHITE)
        self.e_i.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

        ctk.CTkLabel(scroll, text="PARAMÈTRE J  (DÉCALAGE ANGULAIRE)",
                     text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=9, weight="bold")).grid(
            row=2, column=0, sticky="w", padx=20, pady=(0, 4))
        self.e_j = ctk.CTkEntry(scroll, placeholder_text="ex : 1",
                                 font=ctk.CTkFont(size=13), height=38,
                                 corner_radius=RADIUS, border_color=OUTLINE, fg_color=WHITE)
        self.e_j.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 16))

        # ── Entrées optionnelles ──────────────────────────────────────────────
        opt_header = ctk.CTkFrame(scroll, fg_color=SURFACE_CARD, corner_radius=RADIUS)
        opt_header.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 12))
        ctk.CTkLabel(opt_header, text="PARAMÈTRES OPTIONNELS",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=ON_SURFACE_VAR).grid(row=0, column=0, sticky="w", padx=12, pady=7)

        ctk.CTkLabel(scroll, text="RAYON DE CELLULE  R  (km)",
                     text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=9, weight="bold")).grid(
            row=5, column=0, sticky="w", padx=20, pady=(0, 4))
        self.e_R = ctk.CTkEntry(scroll, placeholder_text="ex : 2.5",
                                 font=ctk.CTkFont(size=13), height=38,
                                 corner_radius=RADIUS, border_color=OUTLINE, fg_color=WHITE)
        self.e_R.grid(row=6, column=0, sticky="ew", padx=20, pady=(0, 12))

        ctk.CTkLabel(scroll, text="FRÉQUENCES DISPONIBLES  F  (canaux)",
                     text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=9, weight="bold")).grid(
            row=7, column=0, sticky="w", padx=20, pady=(0, 4))
        self.e_F = ctk.CTkEntry(scroll, placeholder_text="ex : 200",
                                 font=ctk.CTkFont(size=13), height=38,
                                 corner_radius=RADIUS, border_color=OUTLINE, fg_color=WHITE)
        self.e_F.grid(row=8, column=0, sticky="ew", padx=20, pady=(0, 16))

        ctk.CTkButton(scroll, text="▣  CALCULER", command=self._calculate,
                       font=ctk.CTkFont(size=12, weight="bold"),
                       height=44, corner_radius=RADIUS,
                       fg_color=ACCENT_AMBER, hover_color="#d4830a",
                       text_color=WHITE).grid(row=9, column=0, sticky="ew", padx=20, pady=(0, 16))

        # ── Résultat N ───────────────────────────────────────────────────────
        n_frame = ctk.CTkFrame(scroll, fg_color=DEEP_NAVY, corner_radius=RADIUS)
        n_frame.grid(row=10, column=0, sticky="ew", padx=20, pady=(0, 14))
        n_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(n_frame, text="TAILLE DU MOTIF CALCULÉE",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color="#8ab4d4").grid(row=0, column=0, sticky="w", padx=14, pady=(10, 2))
        self.r_N = ctk.CTkLabel(n_frame, text="N = —",
                                 font=ctk.CTkFont(size=28, weight="bold"),
                                 text_color=WHITE)
        self.r_N.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 12))

        # ── Métriques dérivées ────────────────────────────────────────────────
        ctk.CTkLabel(scroll, text="MÉTRIQUES DÉRIVÉES",
                     text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=9, weight="bold")).grid(
            row=11, column=0, sticky="w", padx=20, pady=(0, 6))

        metrics_frame = ctk.CTkFrame(scroll, fg_color=WHITE, corner_radius=0)
        metrics_frame.grid(row=12, column=0, sticky="ew", padx=20, pady=(0, 12))
        metrics_frame.grid_columnconfigure(0, weight=1)

        self._metric_labels = {}
        metrics_def = [
            ("DR",           "Rapport D/R  =  √(3N)"),
            ("D",            "Distance de réutilisation  D  (km)"),
            ("surf_cell",    "Surface d'une cellule  (km²)"),
            ("surf_cluster", "Surface du cluster  (km²)"),
            ("canaux",       "Canaux par cellule"),
        ]
        defaults = {
            "DR":           "—",
            "D":            "— km",
            "surf_cell":    "— km²",
            "surf_cluster": "— km²",
            "canaux":       "—",
        }
        for idx, (key, label_text) in enumerate(metrics_def):
            card = ctk.CTkFrame(metrics_frame, fg_color=SURFACE_CARD, corner_radius=RADIUS)
            card.grid(row=idx, column=0, sticky="ew", pady=(0, 5))
            card.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(card, text=label_text,
                         font=ctk.CTkFont(size=9), text_color=ON_SURFACE_VAR).grid(
                row=0, column=0, sticky="w", padx=10, pady=(6, 0))
            val = ctk.CTkLabel(card, text=defaults[key],
                                font=ctk.CTkFont(size=14, weight="bold"),
                                text_color=MUTED)
            val.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 6))
            self._metric_labels[key] = val

        # ── Formules rappel ───────────────────────────────────────────────────
        formula_box = ctk.CTkFrame(scroll, fg_color=SURFACE_CARD, corner_radius=RADIUS)
        formula_box.grid(row=13, column=0, sticky="ew", padx=20, pady=(0, 8))
        ctk.CTkLabel(formula_box,
                     text="N = i²+ij+j²   ·   D = R·√(3N)   ·   A = 2.6·R²",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=PRIMARY).grid(row=0, column=0, sticky="w", padx=12, pady=8)

        self.r_err = ctk.CTkLabel(scroll, text="", font=ctk.CTkFont(size=11),
                                   text_color=ERR, wraplength=200)
        self.r_err.grid(row=14, column=0, padx=20, pady=(0, 16))

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
        ctk.CTkFrame(right, height=1, fg_color=OUTLINE).grid(row=1, column=0, sticky="ew")

        self.plot_frame = ctk.CTkFrame(right, fg_color=WHITE, corner_radius=0)
        self.plot_frame.grid(row=2, column=0, sticky="nsew")

        leg = ctk.CTkFrame(right, fg_color=WHITE, corner_radius=0)
        leg.grid(row=3, column=0, sticky="ew", padx=20, pady=(8, 16))
        for color, label in [(PRIMARY, "Cellule Centrale"),
                              (ACCENT_AMBER, "Co-Canal"),
                              (SURFACE_CARD, "Frontière Cluster")]:
            dot = ctk.CTkFrame(leg, width=14, height=14, fg_color=color, corner_radius=2)
            dot.pack(side="left", padx=(0, 4))
            ctk.CTkLabel(leg, text=label, font=ctk.CTkFont(size=10),
                         text_color=ON_SURFACE).pack(side="left", padx=(0, 20))

    # ── Logique de calcul ─────────────────────────────────────────────────────

    def _calculate(self):
        try:
            i_str = self.e_i.get().strip()
            j_str = self.e_j.get().strip()
            if not i_str or not j_str:
                raise ValueError("i et j sont obligatoires.")
            i, j = int(i_str), int(j_str)
            if i < 0 or j < 0:
                raise ValueError("i et j doivent être ≥ 0.")
            if i == 0 and j == 0:
                raise ValueError("i et j ne peuvent pas être tous les deux nuls.")

            R = None
            r_str = self.e_R.get().strip()
            if r_str:
                R = float(r_str)
                if R <= 0:
                    raise ValueError("Le rayon R doit être > 0.")

            F = None
            f_str = self.e_F.get().strip()
            if f_str:
                F = int(f_str)
                if F <= 0:
                    raise ValueError("Le nombre de fréquences F doit être > 0.")

            N = calc_N(i, j)
            self.r_N.configure(text=f"N = {N}")
            self.r_err.configure(text="")
            self._update_metrics(N, R, F)
            self._render(N)

        except ValueError as e:
            self.r_err.configure(text=str(e) or "Entrée invalide.")

    def _update_metrics(self, N: int, R: float | None, F: int | None):
        DR = math.sqrt(3 * N)
        self._metric_labels["DR"].configure(text=f"{DR:.3f}", text_color=PRIMARY)

        if R is not None:
            D          = R * DR
            surf_cell  = 2.6 * R ** 2
            surf_clust = N * surf_cell
            self._metric_labels["D"].configure(
                text=f"{D:.2f} km", text_color=PRIMARY)
            self._metric_labels["surf_cell"].configure(
                text=f"{surf_cell:.2f} km²", text_color=PRIMARY)
            self._metric_labels["surf_cluster"].configure(
                text=f"{surf_clust:.2f} km²", text_color=PRIMARY)
        else:
            for key in ("D", "surf_cell", "surf_cluster"):
                defaults = {"D": "— km", "surf_cell": "— km²", "surf_cluster": "— km²"}
                self._metric_labels[key].configure(
                    text=f"{defaults[key]}  (R non fourni)", text_color=MUTED)

        if F is not None:
            canaux = F / N
            self._metric_labels["canaux"].configure(
                text=f"{canaux:.1f}  ≈  {int(canaux)} canaux / cellule",
                text_color=PRIMARY)
        else:
            self._metric_labels["canaux"].configure(
                text="—  (F non fourni)", text_color=MUTED)

    # ── Rendu hexagonal ───────────────────────────────────────────────────────

    def _render(self, N):
        for w in self.plot_frame.winfo_children():
            w.destroy()

        ref_cid = 0

        fig, ax = plt.subplots(figsize=(6, 5), facecolor=WHITE)
        ax.set_facecolor(WHITE)

        for cx, cy, cid, is_center in _hex_grid(N, rings=3):
            if is_center:
                face, edge, tc, lw = PRIMARY, WHITE, WHITE, 2.0
            elif cid == ref_cid:
                face, edge, tc, lw = ACCENT_AMBER, WHITE, WHITE, 1.5
            else:
                face, edge, tc, lw = SURFACE_CARD, OUTLINE, ON_SURFACE, 1.0

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
