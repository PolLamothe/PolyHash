#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module d'exportation des solutions.
"""
from polystructure import Intersection
from polyparser import parse_challenge


def export_file(intersections: list[Intersection], challenge: str, outputFile: str) -> None:
    """
    Exporte le schedule des intersections dans un fichier texte.

    Entrées :
    - intersections : Liste des intersections d'une simulation
    - challenge : Nom du challenge
    - outputFile : Nom du fichier de sortie (ex : test)
    """
    f = open("./solutions/" + challenge + "/" + outputFile + ".txt", "w")
    f.write(f"{len(intersections)}\n")

    # Ajoute le planning de chaque intersection au fichier
    for intersection in intersections:
        f.write(f"{intersection.getId()}\n")
        f.write(f"{len(intersection.getStreets())}\n")
        sched = intersection.getSchedule()
        for street, schedule in sched:
            f.write(f"{street.name} {schedule.time}\n")

if __name__ == "__main__":
    challenge = parse_challenge("./challenges/b_ocean.in")
    export_file(list(challenge.getDataManager().getIntersections().values()))