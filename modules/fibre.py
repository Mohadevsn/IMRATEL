import tkinter as tk
import customtkinter as ctk

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
# Interface simplifiée : pertes_totales = n_c·A_c + n_e·A_e saisis en une valeur
# Bilan : P_out = P_in - α·L - pertes_totales
# Marge  = P_out - P_sensibilité

def calc_pout(pin, alpha, L, n_c, A_c, n_e, A_e):
    return pin - alpha * L - (n_c * A_c + n_e * A_e)

def calc_pin(pout, alpha, L, n_c, A_c, n_e, A_e):
    return pout + alpha * L + (n_c * A_c + n_e * A_e)

def calc_length(pin, pout, alpha, n_c, A_c, n_e, A_e):
    if alpha == 0:
        raise ValueError("L'atténuation α ne peut pas être nulle.")
    return (pin - pout - (n_c * A_c + n_e * A_e)) / alpha

def calc_marge(pout, p_sens):
    return pout - p_sens

def _calc(pin, alpha, L, pertes_totales):
    return pin - alpha * L - pertes_totales


# ── Frame principale ──────────────────────────────────────────────────────────

class FibreFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # ── Carte gauche ──────────────────────────────────────────────────────
        left = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=RADIUS,
                             border_width=1, border_color=OUTLINE)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)
        left.grid_columnconfigure(1, weight=1)
        left.grid_rowconfigure(3, weight=1)

        # Header
        h = ctk.CTkFrame(left, fg_color=WHITE, corner_radius=0)
        h.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(18, 14))
        ctk.CTkLabel(h, text="⇄  Paramètres d'Entrée",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=ON_SURFACE).pack(side="left")
        ctk.CTkFrame(left, height=1, fg_color=OUTLINE).grid(
            row=1, column=0, columnspan=2, sticky="ew")

        # Grille 2x2 de champs
        fields_frame = ctk.CTkFrame(left, fg_color=WHITE, corner_radius=0)
        fields_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=16)
        fields_frame.grid_columnconfigure(0, weight=1)
        fields_frame.grid_columnconfigure(1, weight=1)

        specs = [
            ("PUISSANCE D'ENTRÉE [DBM]", "pin",    "0.0",  0, 0),
            ("LONGUEUR [KM]",            "L",      "40.0", 0, 1),
            ("ATTÉNUATION [DB/KM]",      "alpha",  "0.22", 1, 0),
            ("PERTES CONN./ÉPISSURES [DB]","pertes","2.5",  1, 1),
        ]
        self.vars: dict[str, ctk.StringVar] = {}
        self.entries: dict[str, ctk.CTkEntry] = {}

        for label, key, ph, row, col in specs:
            f = ctk.CTkFrame(fields_frame, fg_color=WHITE, corner_radius=0)
            f.grid(row=row, column=col, sticky="nsew",
                   padx=(0, 8) if col == 0 else (8, 0), pady=6)
            f.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(f, text=label, text_color=ON_SURFACE_VAR,
                         font=ctk.CTkFont(size=9, weight="bold")).grid(
                row=0, column=0, sticky="w", pady=(0, 2))

            var = ctk.StringVar(value=ph)
            e = ctk.CTkEntry(f, textvariable=var, font=ctk.CTkFont(size=13),
                              height=44, corner_radius=RADIUS,
                              border_color=OUTLINE, fg_color=WHITE)
            e.grid(row=1, column=0, sticky="ew")
            self.vars[key] = var
            self.entries[key] = e

        # Champ sensibilité optionnel
        ctk.CTkLabel(fields_frame, text="SEUIL DE RÉCEPTION [DBM]  (optionnel pour la marge)",
                     text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=9, weight="bold")).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(12, 2))
        self.vars["p_sens"] = ctk.StringVar()
        self.entries["p_sens"] = ctk.CTkEntry(
            fields_frame, textvariable=self.vars["p_sens"],
            placeholder_text="ex: -18.0",
            font=ctk.CTkFont(size=13), height=44,
            corner_radius=RADIUS, border_color=OUTLINE, fg_color=WHITE)
        self.entries["p_sens"].grid(row=3, column=0, columnspan=2, sticky="ew")

        # Note typique
        ctk.CTkLabel(fields_frame,
                     text="Typique: 0.2 - 0.3 dB/km @ 1550nm",
                     text_color=ON_SURFACE_VAR,
                     font=ctk.CTkFont(size=9, slant="italic")).grid(
            row=4, column=0, sticky="w", pady=(4, 0))

        # Bouton calculer
        ctk.CTkButton(left, text="▣  CALCULER LE BILAN", command=self._calculate,
                       font=ctk.CTkFont(size=13, weight="bold"),
                       height=46, corner_radius=RADIUS,
                       fg_color=PRIMARY, hover_color=DEEP_NAVY).grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(4, 12))

        # Schéma visualisation
        viz = ctk.CTkFrame(left, fg_color=SURFACE_CARD, corner_radius=RADIUS)
        viz.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 20))
        ctk.CTkLabel(viz, text="⚡  Visualisation de la Liaison",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=ON_SURFACE).pack(anchor="w", padx=14, pady=(12, 8))

        self.canvas = tk.Canvas(viz, height=90, bg=SURFACE_CARD,
                                 highlightthickness=0, bd=0)
        self.canvas.pack(fill="x", padx=14, pady=(0, 12))
        self.canvas.bind("<Configure>", self._draw_schematic)

        # ── Carte droite : résultats ──────────────────────────────────────────
        right = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=RADIUS,
                              border_width=1, border_color=OUTLINE)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)

        rh = ctk.CTkFrame(right, fg_color=WHITE, corner_radius=0)
        rh.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 14))
        ctk.CTkLabel(rh, text="▣  Résultats du Calcul",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=ON_SURFACE).pack(side="left")
        ctk.CTkFrame(right, height=1, fg_color=OUTLINE).grid(
            row=1, column=0, sticky="ew")

        rbody = ctk.CTkFrame(right, fg_color=WHITE, corner_radius=0)
        rbody.grid(row=2, column=0, sticky="nsew", padx=16, pady=16)
        rbody.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        # Carte P_out (navy)
        self.card_pout = ctk.CTkFrame(rbody, fg_color=DEEP_NAVY, corner_radius=RADIUS)
        self.card_pout.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.card_pout.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.card_pout, text="PUISSANCE DE SORTIE [DBM]",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color="#8ab4d4").grid(row=0, column=0, sticky="w",
                                                  padx=16, pady=(12, 2))
        self.r_pout_val = ctk.CTkLabel(self.card_pout, text="—",
                                        font=ctk.CTkFont(size=32, weight="bold"),
                                        text_color=WHITE)
        self.r_pout_val.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))

        # Carte Marge (amber)
        self.card_marge = ctk.CTkFrame(rbody, fg_color=SURFACE_CARD, corner_radius=RADIUS,
                                        border_width=1, border_color=OUTLINE)
        self.card_marge.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        self.card_marge.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.card_marge, text="MARGE SYSTÈME [DB]",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=ON_SURFACE_VAR).grid(row=0, column=0, sticky="w",
                                                       padx=16, pady=(12, 2))
        self.r_marge_val = ctk.CTkLabel(self.card_marge, text="—",
                                         font=ctk.CTkFont(size=32, weight="bold"),
                                         text_color=ON_SURFACE_VAR)
        self.r_marge_val.grid(row=1, column=0, sticky="w", padx=16)
        self.r_marge_status = ctk.CTkLabel(self.card_marge, text="",
                                            font=ctk.CTkFont(size=10),
                                            text_color=OK)
        self.r_marge_status.grid(row=2, column=0, sticky="w", padx=16, pady=(2, 12))

        # Détails
        ctk.CTkFrame(rbody, height=1, fg_color=OUTLINE).grid(
            row=2, column=0, sticky="ew", pady=(0, 12))

        details = ctk.CTkFrame(rbody, fg_color=WHITE, corner_radius=0)
        details.grid(row=3, column=0, sticky="ew")
        details.grid_columnconfigure(1, weight=1)

        for i, (lbl, attr) in enumerate([
            ("Atténuation Totale", "r_att"),
            ("Seuil de Réception", "r_seuil"),
        ]):
            ctk.CTkLabel(details, text=lbl, font=ctk.CTkFont(size=11),
                         text_color=ON_SURFACE).grid(row=i, column=0, sticky="w", pady=4)
            lbl_w = ctk.CTkLabel(details, text="—", font=ctk.CTkFont(size=11, weight="bold"),
                                  text_color=ON_SURFACE)
            lbl_w.grid(row=i, column=1, sticky="e", pady=4)
            setattr(self, attr, lbl_w)

        # Observation
        self.obs_frame = ctk.CTkFrame(rbody, fg_color="#fff8e8", corner_radius=RADIUS,
                                       border_width=1, border_color=ACCENT_AMBER)
        self.obs_frame.grid(row=4, column=0, sticky="ew", pady=(16, 0))
        ctk.CTkLabel(self.obs_frame, text="OBSERVATION",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=ACCENT_AMBER).pack(anchor="w", padx=12, pady=(10, 2))
        self.r_obs = ctk.CTkLabel(self.obs_frame, text="Entrez les paramètres et calculez.",
                                   font=ctk.CTkFont(size=10), text_color=ON_SURFACE,
                                   wraplength=260, justify="left")
        self.r_obs.pack(anchor="w", padx=12, pady=(0, 10))

        self.r_err = ctk.CTkLabel(rbody, text="", font=ctk.CTkFont(size=11),
                                   text_color=ERR, wraplength=260)
        self.r_err.grid(row=5, column=0, sticky="w", pady=(8, 0))

    def _draw_schematic(self, event=None):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        if w < 10:
            return
        h = 90
        cx = w // 2
        # Ligne fibre
        self.canvas.create_line(80, h//2, w-80, h//2,
                                 fill=PRIMARY, width=3)
        # Points connecteurs
        for px in [cx - 60, cx + 60]:
            self.canvas.create_oval(px-6, h//2-6, px+6, h//2+6,
                                    fill=ACCENT_AMBER, outline="")
        # Label fibre
        self.canvas.create_text(cx, h//2 - 16, text="Fibre Optique",
                                 fill=ON_SURFACE_VAR, font=("Helvetica", 9))
        # Émetteur
        self.canvas.create_oval(20, h//2-22, 64, h//2+22,
                                 fill=SURFACE_CARD, outline=OUTLINE, width=1)
        self.canvas.create_text(42, h//2, text="((•))", fill=PRIMARY,
                                 font=("Helvetica", 9, "bold"))
        self.canvas.create_text(42, h-10, text="ÉMETTEUR",
                                 fill=ON_SURFACE_VAR, font=("Helvetica", 8))
        # Récepteur
        self.canvas.create_oval(w-64, h//2-22, w-20, h//2+22,
                                 fill=SURFACE_CARD, outline=OUTLINE, width=1)
        self.canvas.create_text(w-42, h//2, text="(•))", fill=PRIMARY,
                                 font=("Helvetica", 9, "bold"))
        self.canvas.create_text(w-42, h-10, text="RÉCEPTEUR",
                                 fill=ON_SURFACE_VAR, font=("Helvetica", 8))

    def _get(self, key):
        v = self.vars[key].get().strip()
        return float(v) if v else None

    def _calculate(self):
        try:
            pin    = self._get("pin")
            alpha  = self._get("alpha")
            L      = self._get("L")
            pertes = self._get("pertes") or 0.0
            p_sens = self._get("p_sens")

            if pin is None or alpha is None or L is None:
                self.r_err.configure(text="P_in, α et L sont obligatoires.")
                return

            pout     = _calc(pin, alpha, L, pertes)
            att_tot  = alpha * L + pertes

            self.r_pout_val.configure(text=f"{pout:.2f}  dBm")
            self.r_att.configure(text=f"{att_tot:.1f} dB")
            self.r_seuil.configure(text=f"{p_sens:.1f} dBm" if p_sens is not None else "—")

            if p_sens is not None:
                marge = calc_marge(pout, p_sens)
                self.r_marge_val.configure(text=f"{marge:.1f}", text_color=ACCENT_AMBER)
                if marge >= 3:
                    self.r_marge_status.configure(
                        text="✓  Conforme aux spécifications", text_color=OK)
                    self.r_obs.configure(
                        text=f"La marge système est supérieure à 3 dB, "
                             f"garantissant une robustesse face au vieillissement des composants.")
                else:
                    self.r_marge_status.configure(
                        text="✗  Marge insuffisante", text_color=ERR)
                    self.r_obs.configure(
                        text=f"La marge est inférieure à 3 dB. "
                             f"Réduire la longueur ou augmenter la puissance d'émission.")
                self.card_marge.configure(fg_color=DEEP_NAVY if marge >= 0 else "#fdf0f0",
                                           border_color=OK if marge >= 0 else ERR)
                self.r_marge_val.configure(text_color=WHITE if marge >= 0 else ERR)
            else:
                self.r_marge_val.configure(text="—", text_color=ON_SURFACE_VAR)
                self.r_marge_status.configure(text="Seuil de réception non renseigné")
                self.card_marge.configure(fg_color=SURFACE_CARD, border_color=OUTLINE)
                self.r_obs.configure(text="Renseignez le seuil de réception pour calculer la marge.")

            self.r_err.configure(text="")
        except ValueError as e:
            self.r_err.configure(text=str(e) or "Entrée invalide.")
        except TypeError:
            self.r_err.configure(text="Vérifiez les champs P_in, α et L.")
