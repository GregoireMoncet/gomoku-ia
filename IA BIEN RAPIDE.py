# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 10:54:33 2025

@author: hugoa
"""

import numpy as np
import time

class Plateau:
    def __init__(self):
        self.taille = 15
        self.plateau = np.full((self.taille, self.taille), '.')

    def afficher(self):
        print("   " + "   ".join(map(str, range(self.taille))))
        print("  +" + "---+" * self.taille)
        for i, ligne in enumerate(self.plateau):
            affichage_ligne = " | ".join(ligne)
            print(f"{chr(65 + i)} | {affichage_ligne} |")
            print("  +" + "---+" * self.taille)

    def est_coup_valide(self, x, y):
        return 0 <= x < self.taille and 0 <= y < self.taille and self.plateau[x, y] == '.'

    def jouer_coup(self, x, y, joueur):
        if self.est_coup_valide(x, y):
            self.plateau[x, y] = joueur
            return True
        elif joueur == '.':
            self.plateau[x, y] = '.'
            return True
        return False

    def verifier_victoire(self, joueur):
        def verifier_ligne(ligne):
            return ''.join(ligne).find(joueur * 5) != -1

        for i in range(self.taille):
            if verifier_ligne(self.plateau[i, :]) or verifier_ligne(self.plateau[:, i]):
                return True

        for d in range(-self.taille + 1, self.taille):
            if verifier_ligne(np.diagonal(self.plateau, d)) or verifier_ligne(np.diagonal(np.fliplr(self.plateau), d)):
                return True

        return False

    def est_plein(self):
        return not (self.plateau == '.').any()

class IA_Gomoku:
    def __init__(self, joueur):
        self.joueur = joueur
        self.adversaire = 'O' if joueur == 'X' else 'X'
        self.noeuds_evalues = 0

    def evaluer_plateau(self, plateau):
        score = 0
        for i in range(plateau.taille):
            for ligne in [plateau.plateau[i, :], plateau.plateau[:, i], 
                         np.diagonal(plateau.plateau, i), np.diagonal(np.fliplr(plateau.plateau), i)]:
                chaine_ligne = ''.join(ligne)
                
                # Victoire immédiate
                if f".{self.joueur * 4}." in chaine_ligne or f"{self.joueur * 4}." in chaine_ligne:
                    score += 5000
                if f".{self.adversaire * 4}." in chaine_ligne or f"{self.adversaire * 4}." in chaine_ligne:
                    score -= 5000
    
                # Favoriser des chaînes ouvertes
                score += chaine_ligne.count(f".{self.joueur * 3}.") * 200
                score -= chaine_ligne.count(f".{self.adversaire * 3}.") * 200
    
                # Autres chaînes
                score += chaine_ligne.count(f"{self.joueur * 3}.") * 100
                score -= chaine_ligne.count(f"{self.adversaire * 3}.") * 100
    
                score += chaine_ligne.count(f"{self.joueur * 2}.") * 10
                score -= chaine_ligne.count(f"{self.adversaire * 2}.") * 10
        return score



    def generer_coups(self, plateau):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        priorites = {}
    
        for x in range(plateau.taille):
            for y in range(plateau.taille):
                if plateau.plateau[x, y] == self.joueur:
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < plateau.taille and 0 <= ny < plateau.taille and plateau.plateau[nx, ny] == '.':
                            if (nx, ny) not in priorites:
                                priorites[(nx, ny)] = 1
                            priorites[(nx, ny)] += 1  
        return sorted(priorites.keys(), key=lambda c: -priorites[c])


    def minimax(self, plateau, profondeur, maximiser, alpha, beta):
        self.noeuds_evalues += 1
        if plateau.verifier_victoire(self.joueur):
            return 10000 - (3 - profondeur)
        if plateau.verifier_victoire(self.adversaire):
            return -10000 + (3 - profondeur)
        if profondeur == 0 or plateau.est_plein():
            return self.evaluer_plateau(plateau)

        if maximiser:
            max_eval = float('-inf')
            for coup in self.generer_coups(plateau):
                x, y = coup
                plateau.jouer_coup(x, y, self.joueur)
                eval = self.minimax(plateau, profondeur - 1, False, alpha, beta)
                plateau.jouer_coup(x, y, '.')
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for coup in self.generer_coups(plateau):
                x, y = coup
                plateau.jouer_coup(x, y, self.adversaire)
                eval = self.minimax(plateau, profondeur - 1, True, alpha, beta)
                plateau.jouer_coup(x, y, '.')
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
        
    def trouver_meilleur_coup(self, plateau, profondeur):
        meilleur_coup = None
        meilleure_valeur = float('-inf')
    
        for coup in self.generer_coups(plateau):
            x, y = coup
            plateau.jouer_coup(x, y, self.joueur)
            
            if plateau.verifier_victoire(self.joueur):
                plateau.jouer_coup(x, y, '.')
                return (x, y)
            
            valeur_coup = self.minimax(plateau, profondeur - 1, False, float('-inf'), float('inf'))
            plateau.jouer_coup(x, y, '.')
    
            if valeur_coup > meilleure_valeur:
                meilleure_valeur = valeur_coup
                meilleur_coup = (x, y)
        return meilleur_coup



if __name__ == "__main__":
    plateau = Plateau()
    premier = None
    while premier not in ['1', '2']:
        print("Qui commence ? Tapez '1' pour vous ou '2' pour l'IA :")
        premier = input()
        if premier not in ['1', '2']:
            print("Entrée invalide. Veuillez taper '1' ou '2'.")

    joueur = 'X' if premier == '1' else 'O'
    ia = IA_Gomoku('X' if joueur == 'O' else 'O')

    print("Jeu de Gomoku")
    premier_coup_joueur = premier == '1'
    premier_coup_ia = premier == '2'
    deuxieme_coup_restreint = premier == '1'
    deuxieme_coup_ia = premier == '2'
    plateau.afficher()

    while not plateau.est_plein():
        if joueur == 'X':
            coup = input("Entrez votre coup : ").upper()
            try:
                x, y = ord(coup[0]) - 65, int(coup[1:])
                if premier_coup_joueur:
                    if (x, y) != (7, 7):
                        print("Vous devez jouer en H7 pour votre premier coup.")
                        continue
                    premier_coup_joueur = False
                elif deuxieme_coup_restreint:
                    if (abs(x - 7) < 4 and abs(y - 7) < 4):
                        print("Votre deuxième coup doit être à au moins 4 cases de H7.")
                        continue
                    deuxieme_coup_restreint = False
                if not plateau.jouer_coup(x, y, 'X'):
                    print("Coup invalide ou déjà joué par l'IA. Essayez à nouveau.")
                    continue
            except:
                print("Entrée invalide. Essayez à nouveau.")
                continue

            plateau.afficher()
            if plateau.verifier_victoire('X'):
                print("Vous gagnez!")
                break

            joueur = 'O'

        else:
            print("L'IA réfléchit...")
            debut = time.time()
            if premier_coup_ia:
                coup_ia = (7, 7)
                plateau.jouer_coup(7, 7, 'O')
                print("L'IA joue : H7")
                premier_coup_ia = False
            elif deuxieme_coup_ia:
                if plateau.est_coup_valide(3, 7):
                    plateau.jouer_coup(3, 7, 'O')
                    print("L'IA joue : D7")
                elif plateau.est_coup_valide(11, 7):
                    plateau.jouer_coup(11, 7, 'O')
                    print("L'IA joue : L7")
                deuxieme_coup_ia = False
            else:
                coup_ia = ia.trouver_meilleur_coup(plateau, profondeur=3)
                fin = time.time()
                temps_reflexion = round(fin - debut, 2)
                print(f"Temps de réflexion de l'IA : {temps_reflexion} secondes")
            
            if coup_ia:
                plateau.jouer_coup(coup_ia[0], coup_ia[1], 'O')
                print(f"L'IA joue : {chr(coup_ia[0] + 65)}{coup_ia[1]}")
            elif plateau.est_plein():
                print("Match nul! Le plateau est plein.")
                break
            else:
                plateau.jouer_coup(7, 6, 'O')
                print("L'IA joue : H6")

            plateau.afficher()
            if plateau.verifier_victoire('O'):
                print("L'IA gagne!")
                break

            joueur = 'X'

    print(f"L'IA a évalué {ia.noeuds_evalues} noeuds.")
