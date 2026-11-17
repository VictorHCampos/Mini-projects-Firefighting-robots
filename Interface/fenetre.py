import math
import tkinter as tk
from pathlib import Path

# Dossier des icônes PNG des boutons de contrôle
DOSSIER_ICONES = Path(__file__).parent / "icones"
COULEUR_CARTE_VIDE = "#333333"
TAILLE_BOUTON = 30      # taille fixe des boutons de contrôle (pixels)
TAILLE_ICONE_MAX = 25   # l'icône doit tenir dans le bouton, bordure comprise


class FenetrePrincipale(tk.Tk):
    """Fenêtre principale du simulateur de robots pompiers."""

    def __init__(self):
        super().__init__()
        self.title("Simulateur de robots pompiers")
        self.geometry("1100x720")
        self.minsize(800, 500)

        self._creer_barre_superieure()
        self._creer_zone_principale()

    # ---------- Construction de l'interface ----------

    def _creer_barre_superieure(self):
        barre = tk.Frame(self)
        barre.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))

        tk.Button(barre, text="Import Map", command=self.importer_carte).pack(side=tk.LEFT, padx=(0, 15))

        # (texte, fichier icône, action)
        controles = [
            ("C", "C.png", self.demarrer_simulation),
            ("P", "P.png", self.arreter_simulation),
            ("R", "R.png", self.reinitialiser_simulation),
            ("A", "A.png", self.accelerer_simulation),
        ]
        for texte, icone, action in controles:
            self._creer_bouton_controle(barre, texte, icone, action).pack(side=tk.LEFT, padx=(0, 5))

    def _creer_bouton_controle(self, parent, texte, fichier_icone, action):
        """Bouton de 30x30 px : icône si icones/<fichier_icone> existe, sinon texte."""
        # Cadre de taille fixe ; le bouton le remplit entièrement
        cadre = tk.Frame(parent, width=TAILLE_BOUTON, height=TAILLE_BOUTON)
        cadre.pack_propagate(False)

        chemin = DOSSIER_ICONES / fichier_icone
        if chemin.exists():
            image = self._charger_icone(chemin)
            bouton = tk.Button(cadre, image=image, command=action)
            bouton.image = image  # garde une référence, sinon l'image disparaît
        else:
            bouton = tk.Button(cadre, text=texte, command=action)
        bouton.pack(fill=tk.BOTH, expand=True)
        return cadre

    def _charger_icone(self, chemin):
        """Charge un PNG et le réduit pour tenir dans TAILLE_ICONE_MAX.

        subsample() réduit d'un facteur entier identique en x et y :
        les proportions et la transparence sont conservées, le fichier n'est pas modifié.
        """
        image = tk.PhotoImage(file=str(chemin))
        facteur = max(1, math.ceil(max(image.width(), image.height()) / TAILLE_ICONE_MAX))
        return image.subsample(facteur, facteur)

    def _creer_zone_principale(self):
        zone = tk.Frame(self)
        zone.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))

        # Colonne de droite (packée avant la carte pour garder sa largeur fixe)
        colonne = tk.Frame(zone, width=180)
        colonne.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        colonne.pack_propagate(False)

        self.liste_bases = self._creer_panneau(colonne, "Base", self.ajouter_base, self.retirer_base)
        self.liste_robots = self._creer_panneau(colonne, "Robots", self.ajouter_robot, self.retirer_robot)
        self.liste_feux = self._creer_panneau(colonne, "Fire", self.ajouter_feu, self.retirer_feu)

        # Zone de la carte
        self.carte = tk.Canvas(zone, bg=COULEUR_CARTE_VIDE, highlightthickness=1, highlightbackground="black")
        self.carte.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)

    def _creer_panneau(self, parent, titre, action_plus, action_moins):
        """Crée un panneau avec un en-tête (titre, +, -) et une liste vide."""
        panneau = tk.Frame(parent, bd=1, relief=tk.SOLID)
        panneau.pack(fill=tk.BOTH, expand=True, pady=5)

        entete = tk.Frame(panneau)
        entete.pack(fill=tk.X)
        tk.Label(entete, text=titre).pack(side=tk.LEFT, padx=5)
        tk.Button(entete, text="-", width=2, command=action_moins).pack(side=tk.RIGHT)
        tk.Button(entete, text="+", width=2, command=action_plus).pack(side=tk.RIGHT)

        liste = tk.Listbox(panneau, bd=0, highlightthickness=0)
        liste.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        return liste

    # ---------- Actions des boutons (à implémenter plus tard) ----------

    def importer_carte(self):
        pass

    def demarrer_simulation(self):
        pass

    def arreter_simulation(self):
        pass

    def reinitialiser_simulation(self):
        pass

    def accelerer_simulation(self):
        pass

    def ajouter_base(self):
        pass

    def retirer_base(self):
        pass

    def ajouter_robot(self):
        pass

    def retirer_robot(self):
        pass

    def ajouter_feu(self):
        pass

    def retirer_feu(self):
        pass
