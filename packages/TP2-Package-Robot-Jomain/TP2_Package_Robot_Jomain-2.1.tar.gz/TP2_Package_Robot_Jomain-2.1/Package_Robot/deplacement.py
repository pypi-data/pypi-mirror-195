#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:38:51 2023

@author: benoit.jomain
"""
from numpy import zeros
import random
class deplacement:
    """Classe qui instancie une grille ainsi que des obstacles et qui gère les déplacements d'un robot"""

    def __init__(self,lines,columns, nb_obs):
        """Instanciation de la classe : positionnement du robot, 
        génération de la grille, génération et placement des obstacles"""
        self.lines = lines
        self.columns = columns
        self.nb_obs = nb_obs
        # Test des entrées 
        if not isinstance(lines, int) or not isinstance(columns,int) or not isinstance(nb_obs,int):
            raise ValueError("You don't give an integer")
        # Création d'une grille en 20x20 si l'utilisateur entre des valeurs en dehors de 3 et 30
        if (lines or columns) < 3 or (lines or columns) >= 31 :  
            self.lines = 20
            self.columns = 20 
        # Position initiale du robot
        self.pos_X = 1
        self.pos_Y = 1
        # Création de la grille et positionnement du robot
        self.grid = zeros((self.lines, self.columns),int)
        self.grid[self.pos_X][self.pos_Y] = 1
        # Création et gestion des obstacles
        self.pos_obs = []
        # Si on a un nb plus grand que la grille pour la génération d'obstacles, on met un seul obstacle sur la grille
        if nb_obs > ((lines * columns) - 1) :
            self.nb_obs = 1
            self.pos_obs = [2,0]
            self.grid[2][0] = 7
        # Génération des obstacles aléatoirement
        else :
            while len(self.pos_obs) < self.nb_obs :
                X = random.randint(0,self.lines - 1)
                Y = random.randint(0,self.columns - 1)
                # Vérification de ne pas mettre l'obstacle sur le robot : position (1,1)
                if (X and Y) != 1 :
                    couple = [X,Y]
                    # On vérifie qu'on a pas généré déjà cet obstacle
                    if couple not in self.pos_obs :
                        self.pos_obs.append(couple)
                        if self.grid[X][Y] != 7 :
                            # On ajoute l'obstacle dans la grille
                            self.grid[X][Y] = 7

    def Print(self):
        """Affichage de la grille avec le robot et les obstacles"""
        print("grille :")
        for line in self.grid :
            print(line)

    def up(self):
        """Fonction qui vérifie et fait le déplacement up s'il est possible"""
        if self.pos_X > 1 and self.grid[self.pos_X - 1][self.pos_Y] != 7 :
            # On efface la position actuelle du robot
            self.grid[self.pos_X][self.pos_Y] = 0
            self.pos_X -= 1
            # On le met dans la grille à son nouvel emplacement
            self.grid[self.pos_X][self.pos_Y] = 1
            return True
        return "ERROR"

    def down(self):
        """Fonction qui vérifie et fait le déplacement down s'il est possible"""
        if self.pos_X < self.lines and self.grid[self.pos_X + 1][self.pos_Y] != 7 :
            # On efface la position actuelle du robot
            self.grid[self.pos_X][self.pos_Y] = 0
            self.pos_X += 1
            # On le met dans la grille à son nouvel emplacement
            self.grid[self.pos_X][self.pos_Y] = 1
            return True
        return "ERROR"
 
    def left(self):
        """Fonction qui vérifie et fait le déplacement left s'il est possible"""
        if self.pos_Y > 1 and self.grid[self.pos_X][self.pos_Y - 1] != 7 :
            # On efface la position actuelle du robot
            self.grid[self.pos_X][self.pos_Y] = 0
            self.pos_Y -= 1
            # On le met dans la grille à son nouvel emplacement
            self.grid[self.pos_X][self.pos_Y] = 1
            return True
        return "ERROR"

    def right(self):
        """Fonction qui vérifie et fait le déplacement right s'il est possible"""
        if self.pos_Y < self.columns and self.grid[self.pos_X][self.pos_Y + 1] != 7:
            # On efface la position actuelle du robot
            self.grid[self.pos_X][self.pos_Y] = 0
            self.pos_Y += 1
            # On le met dans la grille à son nouvel emplacement
            self.grid[self.pos_X][self.pos_Y] = 1
            return True
        return "ERROR"   

if __name__ == "__main__":
    # Création d'une grille, d'un robot et d'obstacles
    G1 = deplacement(5,4,4)
    # Appel des différentes méthodes pour déplacer le robot sur la grille
    G1.Print()
    G1.right()
    G1.down()
    G1.Print()