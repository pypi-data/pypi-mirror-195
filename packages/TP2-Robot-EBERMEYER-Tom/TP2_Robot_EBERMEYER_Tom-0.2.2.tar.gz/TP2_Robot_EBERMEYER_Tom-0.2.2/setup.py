#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:54:37 2023

@author: tom.ebermeyer
"""

from setuptools import setup

setup(
    name="TP2_Robot_EBERMEYER_Tom",
    version="0.2.2",
    author="Tom Ebermeyer",
    author_email="tom.ebermeyer@cpe.fr",
    description="Deplacement d'un robot (modélisé par un '1') dans un grille de '0' de taille définie par l'user. On a ajouter l'extension avec des obsctacles modélisé par des '2' ainsi que l'extension d'ajout multiples de robots controllables dans la grille par les fonctions de déplacement. On limite au maximum à 4 robots simultanéménent.",
    packages=['Package_robot'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
