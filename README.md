# IMRATEL

Outil de dimensionnement des réseaux de télécommunications développé en Python/Tkinter.

## Modules

| Module | Fonctionnalité |
|--------|----------------|
| **Décibels** | Conversion dB ↔ linéaire et dBm ↔ mW |
| **Shannon / Nyquist** | Calcul du débit maximal théorique (deux formules séparées) |
| **Bilan Fibre Optique** | Calcul de P_out, P_in ou L selon les paramètres fournis + marge système |
| **Dimensionnement Cellulaire** | Calcul de N = i² + ij + j² et affichage dynamique du motif hexagonal |

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python3 main.py
```

## Structure

```
imratel/
├── main.py           # Point d'entrée
├── interface.py      # Fenêtre principale et navigation
├── modules/
│   ├── decibels.py
│   ├── shannon.py
│   ├── fibre.py
│   └── cellulaire.py
├── tests/
│   └── test_modules.py
└── requirements.txt
```

## Tests

```bash
python3 tests/test_modules.py
```

## Build (exécutable)

```bash
pyinstaller --onefile --windowed --name IMRATEL main.py
```

L'exécutable sera généré dans `dist/`.
