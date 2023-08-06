#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 17:06:08 2023

@author: tom.ebermeyer
"""
from numpy import zeros
from random import randint

class Grid:
    """Classe de Map"""

    def __init__(self, nb_lignes, nb_colonnes, positions_robot=[[0,0]]):
        """Initialisation de la grille"""
        if (4 < nb_lignes < 10 or 4 < nb_colonnes < 10) and (
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
        self.grid = zeros((self.nb_lignes, self.nb_colonnes), int)

        self.X_robot = []
        self.Y_robot = []
        if len(positions_robot) <= 4 :         
            for pos in positions_robot:
                if isinstance(pos[0],int) and isinstance(pos[1],int):
                    self.X_robot.append(pos[0])
                    self.Y_robot.append(pos[1])
                else:
                    raise ValueError("Positions in grid must be integer !")
            
            for rob in range(len(positions_robot)):
                if (0 <= self.X_robot[rob] <= self.nb_lignes and 0 <= self.Y_robot[rob] <= self.nb_colonnes):
                    self.grid[self.X_robot[rob]][self.Y_robot[rob]] = 1
                else : 
                    raise ValueError("Out of the Grid !")
        else:
            raise ValueError("Too much robots in grid !") 

        self.obstacles = []
        self.creatObstacles()
        self.ajoutObstacles()

    def print_grid(self):
        """Affichage de la grille"""
        print(self.grid)
        print("-------------------------------\n")

    def clean(self,robot):
        """Retire l'ancienne position du robot"""
        self.grid[self.X_robot[robot]][self.Y_robot[robot]] = 0

    def update(self,robot):
        """Met à jour la nouvelle position du robot"""
        self.grid[self.X_robot[robot]][self.Y_robot[robot]] = 1

    def down(self,robot):
        """Descendre d'un cran dans la grille"""
        if self.X_robot[robot] < self.nb_lignes - 1:
            if self.grid[self.X_robot[robot] + 1][self.Y_robot[robot]] == 0 :
                self.clean(robot)
                self.X_robot[robot] += 1
                self.update(robot)      
                return True
            else:
                raise ValueError("Tu as heurté un obstacle !")
        else:
            return False

    def up(self,robot):
        """Monter d'un cran dans la grille"""
        if self.X_robot[robot] > 0:
            if self.grid[self.X_robot[robot] - 1][self.Y_robot[robot]] == 0 :
                self.clean(robot)
                self.X_robot[robot] -= 1
                self.update(robot)
                return True
            else:
                raise ValueError("Tu as heurté un obstacle !")
        else:
            return False

    def right(self,robot):
        """Monter d'un cran dans la grille"""
        if self.Y_robot[robot] < self.nb_colonnes - 1:
            if self.grid[self.X_robot[robot]][self.Y_robot[robot] + 1] == 0 :
                self.clean(robot)
                self.Y_robot[robot] += 1
                self.update(robot)
                return True
            else:
                raise ValueError("Tu as heurté un obstacle !")
        else:
            return False

    def left(self,robot):
        """Monter d'un cran dans la grille"""
        if self.Y_robot[robot] > 0:
            if self.grid[self.X_robot[robot]][self.Y_robot[robot] - 1] == 0:
                self.clean(robot)
                self.Y_robot[robot] -= 1
                self.update(robot)
                return True
            else:
                raise ValueError("Tu as heurté un obstacle !")
        else:
            return False
        
        
    def creatObstacles(self):
        """Création aléatoirement des obstacles"""
        for i in range(randint(2,5)):
            posx = randint(1,self.nb_lignes-1)
            posy = randint(1,self.nb_colonnes-1)
            if [posx,posy] not in self.obstacles and self.grid[posx][posy] == 0:
                self.obstacles.append([posx,posy])
                
    def ajoutObstacles(self):
        """ajout des obstacles dans la grille"""
        for obs in self.obstacles:
            self.grid[obs[0]][obs[1]] = 2



  
            
       

   
        
        
        
        
        
