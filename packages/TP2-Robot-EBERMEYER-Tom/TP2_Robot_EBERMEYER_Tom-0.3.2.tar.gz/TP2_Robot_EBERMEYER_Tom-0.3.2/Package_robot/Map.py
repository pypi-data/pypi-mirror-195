#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 17:06:08 2023

@author: tom.ebermeyer
"""
from numpy import zeros
from random import randint


class Grid:
    """Classe de Map où le robot va se déplacer dans une grille ∈ [4;10] avec des obstacles déplaçable si on les poussent"""

    def __init__(self, nb_lignes, nb_colonnes, positions_robot=[[0, 0]]):
        """Initialisation de la grille, initialement, il y a un robot en (0;0) et on demande à l'user la taille de la grille"""
        if (
            4 < nb_lignes < 10 or 4 < nb_colonnes < 10
        ) and (  # Gestion de nos limites de grille
            isinstance(nb_lignes, int) and isinstance(nb_colonnes, int)
        ):
            self.nb_lignes = nb_lignes
            self.nb_colonnes = nb_colonnes
        else:
            if not (4 < nb_lignes < 10 or 4 < nb_colonnes < 10):
                raise ValueError("Values can't be superior to 10 !")
            if not (
                isinstance(nb_lignes, int) == True
                and isinstance(nb_colonnes, int) == True
            ):
                raise ValueError("Values must be integer !")
            self.nb_lignes = 10
            self.nb_colonnes = 10
        self.grid = zeros(
            (self.nb_lignes, self.nb_colonnes), int
        )  # Création de la grille

        self.X_robot = []  # liste de positions des lignes des différents robots (<=4)
        self.Y_robot = []
        if len(positions_robot) <= 4:
            for pos in positions_robot:
                if isinstance(pos[0], int) and isinstance(pos[1], int):
                    self.X_robot.append(pos[0])
                    self.Y_robot.append(pos[1])
                else:
                    raise ValueError("Positions in grid must be integer !")

            for rob in range(len(positions_robot)):
                if (
                    0 <= self.X_robot[rob] <= self.nb_lignes
                    and 0 <= self.Y_robot[rob] <= self.nb_colonnes
                ):
                    self.grid[self.X_robot[rob]][
                        self.Y_robot[rob]
                    ] = 1  # ajout des robots dans la grille
                else:
                    raise ValueError("Out of the Grid !")
        else:
            raise ValueError("Too much robots in grid !")

        self.obstacles = []
        self.creatObstacles()  # création puis ajout des obstacles dans la grille à l'initialisation
        self.ajoutObstacles()

    def print_grid(self):
        """Affichage de la grille"""
        print(self.grid)
        print("-------------------------------\n")

    def clean(self, robot):
        """Retire l'ancienne position du robot"""
        self.grid[self.X_robot[robot]][self.Y_robot[robot]] = 0

    def update(self, robot):
        """Met à jour la nouvelle position du robot"""
        self.grid[self.X_robot[robot]][self.Y_robot[robot]] = 1

    def down(self, robot):
        """Descendre d'un cran dans la grille"""
        if self.X_robot[robot] < self.nb_lignes - 1:
            if self.grid[self.X_robot[robot] + 1][self.Y_robot[robot]] == 0:
                self.clean(robot)
                self.X_robot[robot] += 1
                self.update(robot)
                return True
            else:
                try:  # On regarde si on peut déplacer l'obstacles
                    if (
                        self.grid[self.X_robot[robot] + 1][self.Y_robot[robot]] == 2
                        and self.grid[self.X_robot[robot] + 2][self.Y_robot[robot]] == 0
                    ):
                        for obs in self.obstacles:
                            if (
                                obs[0] == self.X_robot[robot] + 1
                                and obs[1] == self.Y_robot[robot]
                            ):
                                self.clearObstacles()  # on supprime virtuellement les obstacles de la grille
                                obs[0] += 1  # on change sa position
                                self.ajoutObstacles()  # on remet tous les obstacles dans la grille
                                return True
                except:
                    raise ValueError("Tu as heurté un obstacle !")
        else:
            return False

    def up(self, robot):
        """Monter d'un cran dans la grille"""
        if self.X_robot[robot] > 0:
            if self.grid[self.X_robot[robot] - 1][self.Y_robot[robot]] == 0:
                self.clean(robot)
                self.X_robot[robot] -= 1
                self.update(robot)
                return True
            else:
                if (
                    self.grid[self.X_robot[robot] - 1][self.Y_robot[robot]] == 2
                    and self.grid[self.X_robot[robot] - 2][self.Y_robot[robot]] == 0
                    and (self.X_robot[robot] - 2) >= 0
                ):
                    for obs in self.obstacles:
                        if (
                            obs[0] == self.X_robot[robot] - 1
                            and obs[1] == self.Y_robot[robot]
                        ):
                            self.clearObstacles()
                            obs[0] -= 1
                            self.ajoutObstacles()
                            return True
                else:
                    raise ValueError("Tu as heurté un obstacle !")
        else:
            return False

    def right(self, robot):
        """Déplacer d'un cran vers la  droite dans la grille"""
        if self.Y_robot[robot] < self.nb_colonnes - 1:
            if self.grid[self.X_robot[robot]][self.Y_robot[robot] + 1] == 0:
                self.clean(robot)
                self.Y_robot[robot] += 1
                self.update(robot)
                return True
            else:
                try:
                    if (
                        self.grid[self.X_robot[robot]][self.Y_robot[robot] + 1] == 2
                        and self.grid[self.X_robot[robot]][self.Y_robot[robot] + 2] == 0
                    ):
                        for obs in self.obstacles:
                            if (
                                obs[0] == self.X_robot[robot]
                                and obs[1] == self.Y_robot[robot] + 1
                            ):
                                self.clearObstacles()
                                obs[1] += 1
                                self.ajoutObstacles()
                                return True
                except:
                    raise ValueError("Tu as heurté un obstacle !")
        else:
            return False

    def left(self, robot):
        """Déplacer d'un cran vers la gauche dans la grille"""
        if self.Y_robot[robot] > 0:
            if self.grid[self.X_robot[robot]][self.Y_robot[robot] - 1] == 0:
                self.clean(robot)
                self.Y_robot[robot] -= 1
                self.update(robot)
                return True
            else:
                if (
                    self.grid[self.X_robot[robot]][self.Y_robot[robot] - 1] == 2
                    and self.grid[self.X_robot[robot]][self.Y_robot[robot] - 2] == 0
                    and (self.Y_robot[robot] - 2) >= 0
                ):
                    for obs in self.obstacles:
                        if (
                            obs[0] == self.X_robot[robot]
                            and obs[1] == self.Y_robot[robot] - 1
                        ):
                            self.clearObstacles()
                            obs[1] -= 1
                            self.ajoutObstacles()
                            return True
                else:
                    raise ValueError("Tu as heurté un obstacle !")
        else:
            return False

    def creatObstacles(self):
        """Création aléatoirement des obstacles"""
        for i in range(
            randint(2, 5)
        ):  # création au nombre aléatoire aux positions aléatoires
            posx = randint(1, self.nb_lignes - 1)
            posy = randint(1, self.nb_colonnes - 1)
            if [posx, posy] not in self.obstacles and self.grid[posx][posy] == 0:
                self.obstacles.append([posx, posy])

    def ajoutObstacles(self):
        """ajout des obstacles dans la grille"""
        for obs in self.obstacles:
            self.grid[obs[0]][obs[1]] = 2

    def clearObstacles(self):
        """ajout des obstacles dans la grille"""
        for obs in self.obstacles:
            self.grid[obs[0]][obs[1]] = 0
