#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
[Ce bloc est la documentation du module]
Un Tetris avec Pygame.
Ce code est basee sur le code de Sébastien CHAZALLET, auteur du livre "Python 3, les fondamentaux du language"
"""

__author__ = "LACROIX Wyatt"
__copyright__ = "Copyright 2022"
__credits__ = ["Sébastien CHAZALLET", "Vincent NGUYEN", "Wyatt LACROIX"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Wyatt LACROIX"
__email__ = "wyatt.lacroix@etu.univ-orleans.fr"

# Probleme de l'ordre des imports
from pygame.locals import *
import random
import time
import pygame
import sys
from constantes import *




# Classe Tetris
class Jeu:
    """
	Initialisation de la classe
	"""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(TAILLE_FENETRE)
        self.fonts = {
            'defaut': pygame.font.Font('freesansbold.ttf', 18),
            'titre': pygame.font.Font('freesansbold.ttf', 100),
        }
        pygame.display.set_caption('Application Tetris')

    """Démarrage et arrêt du jeu"""

    def start(self):
        self.afficher_texte('Tetris', CENTRE_FENETRE, font='titre')
        self.afficher_texte('Appuyer sur une touche...', POS)
        self.attente()

    def stop(self):
        self.afficher_texte('Perdu', CENTRE_FENETRE, font='titre')
        self.attente()
        self.quitter()

    def afficher_texte(self, text, position, couleur=9, font='defaut'):
        #		print("Afficher Texte")
        font = self.fonts.get(font, self.fonts['defaut'])
        couleur = COULEURS.get(couleur, COULEURS[9])
        rendu = font.render(text, True, couleur)
        rectangle = rendu.get_rect() # get_rect() is used to obtain a rectangle object
        rectangle.center = position
        self.surface.blit(rendu, rectangle)  #blit() put content of rendu on surface at the position given by rectangle 

    def get_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quitter()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.quitter()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continue
                return event.key

    """Quitter le jeu"""

    def quitter(self):
        print("Quitter")
        pygame.quit()
        sys.exit()

    def rendre(self):
        pygame.display.update()
        self.clock.tick()

    def attente(self):
        print("Attente")
        while self.get_event() == None:
            self.rendre()

    def get_piece(self):
        return PIECES.get(random.choice(PIECES_KEYS))

    def get_current_piece_color(self): # to del, previously row was l and cell was c
        for row in self.current[0]:
            for cell in row:
                if cell != 0:
                    return cell
        return 0

    def calculer_donnes_piece_courante(self):
        m = self.current[self.position[2]]
        coords = []
        for i, l in enumerate(m):
            for j, k in enumerate(l):
                if k != 0:
                    coords.append([i + self.position[0], j + self.position[1]])
        self.coordonnees = coords

    def est_valide(self, x=0, y=0, r=0):
        max_x, max_y = DIM_PLATEAU
        if r == 0:
            coordonnees = self.coordonnees
        else:
            m = self.current[(self.position[2] + r) % len(self.current)]
            coords = []
            for i, l in enumerate(m):
                for j, k in enumerate(l):
                    if k != 0:
                        coords.append(
                            [i + self.position[0], j + self.position[1]])
            coordonnees = coords
#			print("Rotation testée: %s" % coordonnees)
        for cx, cy in coordonnees:
            if not 0 <= x + cx < max_x:
                #				print("Non valide en X: cx=%s, x=%s" % (cx, x))
                return False
            elif cy < 0:
                continue
            elif y + cy >= max_y:
                #				print("Non valide en Y: cy=%s, y=%s" % (cy, y))
                return False
            else:
                if self.plateau[cy + y][cx + x] != 0:
                    #					print("Position occupée sur le plateau")
                    return False


#		print("Position testée valide: x=%s, y=%s" % (x, y))
        return True

    def poser_piece(self):
        print("La pièce est posée")
        if self.position[1] <= 0:
            self.perdu = True
        # Ajout de la pièce parmi le plateau
        couleur = self.get_current_piece_color()
        for cx, cy in self.coordonnees:
            self.plateau[cy][cx] = couleur
        completees = []
        # calculer les lignes complétées
        for i, line in enumerate(self.plateau[::-1]):
            for case in line:
                if case == 0:
                    break
            else:
                print(self.plateau)
                print(">>> %s" % (DIM_PLATEAU[1] - 1 - i))
                completees.append(DIM_PLATEAU[1] - 1 - i)
        lignes = len(completees)
        for i in completees:
            self.plateau.pop(i)
        for i in range(lignes):
            self.plateau.insert(0, [0] * DIM_PLATEAU[0])
        # calculer le score et autre
        self.lignes += lignes
        self.score += lignes * self.niveau
        self.niveau = int(self.lignes / 10) + 1
        if lignes >= 4:
            self.tetris += 1
            self.score += self.niveau * self.tetris
        # Travail avec la pièce courante terminé
        self.current = None

    def first(self):
        self.plateau = [[0] * DIM_PLATEAU[0] for i in range(DIM_PLATEAU[1])]
        self.score, self.pieces, self.lignes, self.tetris, self.niveau = 0, 0, 0, 0, 1
        self.current, self.suivante, self.perdu = None, self.get_piece(), False

    def next(self):
        print("Piece suivante")
        self.current, self.suivante = self.suivante, self.get_piece()
        self.pieces += 1
        self.position = [int(DIM_PLATEAU[0] / 2) - 2, -4, 0]
        self.calculer_donnes_piece_courante()
        self.dernier_mouvement = self.derniere_chute = time.time()

    def gerer_evenements(self):
        event = self.get_event()
        if event == K_p:
            print("Pause")
            self.surface.fill(COULEURS.get(0))
            self.afficher_texte('Pause', CENTRE_FENETRE, font='titre')
            self.afficher_texte('Appuyer sur une touche...', POS)
            self.attente()
        elif event == K_LEFT:
            print("Mouvement vers la gauche")
            if self.est_valide(x=-1):
                self.position[0] -= 1
        elif event == K_RIGHT:
            print("Mouvement vers la droite")
            if self.est_valide(x=1):
                self.position[0] += 1
        elif event == K_DOWN:
            print("Mouvement vers le bas")
            if self.est_valide(y=1):
                self.position[1] += 1
        elif event == K_UP:
            print("Mouvement de rotation")
            if self.est_valide(r=1):
                self.position[2] = (self.position[2] + 1) % len(self.current)
        elif event == K_SPACE:
            print("Mouvement de chute %s / %s" %
                  (self.position, self.coordonnees))
            if self.position[1] <= 0:
                self.position[1] = 1
                self.calculer_donnes_piece_courante()
            a = 0
            while self.est_valide(y=a):
                a += 1
            self.position[1] += a - 1
        self.calculer_donnes_piece_courante()

    def gerer_gravite(self):
        if time.time() - self.derniere_chute > 0.35:
            self.derniere_chute = time.time()
            if not self.est_valide():
                print("On est dans une position invalide")
                self.position[1] -= 1
                self.calculer_donnes_piece_courante()
                self.poser_piece()
            elif self.est_valide() and not self.est_valide(y=1):
                self.calculer_donnes_piece_courante()
                self.poser_piece()
            else:
                print("On déplace vers le bas")
                self.position[1] += 1
                self.calculer_donnes_piece_courante()

    def dessiner_plateau(self):
        self.surface.fill(COULEURS.get(0))
        pygame.draw.rect(self.surface, COULEURS[8],
                         START_PLABORD + TAILLE_PLABORD, BORDURE_PLATEAU)
        for i, ligne in enumerate(self.plateau):
            for j, case in enumerate(ligne):
                couleur = COULEURS[case]
                position = j, i
                coordonnees = tuple([
                    START_PLATEAU[k] + position[k] * TAILLE_BLOC[k]
                    for k in range(2)
                ])
                pygame.draw.rect(self.surface, couleur,
                                 coordonnees + TAILLE_BLOC)
        if self.current is not None:
            for position in self.coordonnees:
                couleur = COULEURS.get(self.get_current_piece_color())
                coordonnees = tuple([
                    START_PLATEAU[k] + position[k] * TAILLE_BLOC[k]
                    for k in range(2)
                ])
                pygame.draw.rect(self.surface, couleur,
                                 coordonnees + TAILLE_BLOC)
        self.score, self.pieces, self.lignes, self.tetris, self.niveau  #TODO
        self.afficher_texte('Score: >%s' % self.score, POSITION_SCORE)
        self.afficher_texte('Pièces: %s' % self.pieces, POSITION_PIECES)
        self.afficher_texte('Lignes: %s' % self.lignes, POSITION_LIGNES)
        self.afficher_texte('Tetris: %s' % self.tetris, POSITION_TETRIS)
        self.afficher_texte('Niveau: %s' % self.niveau, POSITION_NIVEAU)

        self.rendre()

    def play(self):
        print("Jouer")
        self.surface.fill(COULEURS.get(0))
        self.first()
        while not self.perdu:
            if self.current is None:
                self.next()
            self.gerer_evenements()
            self.gerer_gravite()
            self.dessiner_plateau()

if __name__ == '__main__':
    j = Jeu()
    print("Jeu prêt")
    j.start()
    print("Partie démarée")
    j.play()
    print("Partie terminée")
    j.stop()
    print("Arrêt du programme")
