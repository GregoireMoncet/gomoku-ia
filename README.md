# Gomoku IA

Intelligence artificielle du jeu de Gomoku (alignement de 5 pions) écrite en Python. Projet de groupe réalisé dans le cadre d'un cours d'IA, publié avec l'accord des autres membres du groupe.

## Principe

L'IA choisit son coup avec l'algorithme Minimax et l'élagage alpha-bêta. Une fonction d'évaluation note les positions du plateau (victoire immédiate, chaînes ouvertes, autres alignements). Pour garder des temps de réponse courts, seules les cases vides voisines de pions déjà posés sont envisagées comme coups.

## Contenu

Le dépôt contient trois variantes du programme :

- `PROJET DIA GOMOKU A3`
- `gomoku+dynamic depth` (profondeur de recherche dynamique)
- `IA BIEN RAPIDE.py`

Chaque fichier définit une classe `Plateau` (affichage, coups valides, détection de victoire) et une classe `IA_Gomoku` (évaluation, génération des coups, minimax).

## Lancer le programme

Python 3 et NumPy sont nécessaires.

```bash
pip install numpy
python "IA BIEN RAPIDE.py"
```

## Notions mises en pratique

Programmation orientée objet, algorithme Minimax, élagage alpha-bêta, fonction d'évaluation, NumPy, travail en équipe.
