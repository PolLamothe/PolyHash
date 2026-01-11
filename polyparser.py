#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de parsing des fichiers d'entrée pour la mise en oeuvre du projet Poly#.
"""
import re
from polystructure import Challenge, RawStreet, RawCar

def parse_challenge(filename: str) -> Challenge:
    
    """Lit un fichier de challenge et extrait les informations nécessaires.

    Vous pouvez choisir la structure de données structurées qui va
    représenter votre challenge: dictionnaire, objet, etc
    """
    print(filename)
    with open("./challenges/"+filename+".in", 'r') as f:
        # Lire la première ligne, la découper, et convertir les valeurs en entier
        line = f.readline().strip()
        # Strip everything after #
        line = re.sub(r'\s*#.*', '', line)
        # rows, columns, altitudes = [ int(v) for v in line.split() ]
        simulation_time, number_intersections, number_streets, number_cars, score_per_car = [ int(v) for v in line.split() ]
        challenge:Challenge = Challenge(simulation_time,number_intersections,number_streets,number_cars,score_per_car,[],[])
        for cpt_rues in range(number_streets):
            street = f.readline().strip().split()
            rue:RawStreet = RawStreet(street[0], street[1], street[2],int(street[3]))
            challenge.getDataManager().addstreet(rue)

        for cpt_cars in range(number_cars):
            path = f.readline().strip().split()
            voiture:RawCar = RawCar(path[1:])
            challenge.getDataManager().addCar(voiture)

    return challenge
