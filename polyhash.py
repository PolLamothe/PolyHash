#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module principal pour la mise en oeuvre du projet Poly#.
"""

from polyparser import parse_challenge
from polystructure import Challenge, Solver
from polysolver import AvailableSolutions
from polyscorer import scorer, exportCSV
from polyexport import export_file
import csv
import time

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Solve Poly# challenge.')
    parser.add_argument('challenge', type=str,
                        help='challenge definition filename',
                        metavar="challenge")
    parser.add_argument('solution', type=str, default="empty",
                        help='solution program')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='output filename',
                        metavar="sortie")
    parser.add_argument('-v',help='verbose mode',action="store_true")
    parser.add_argument('-d',help='diagnose mode',action="store_true")

    # Récupère les arguments
    args = parser.parse_args()

    # Utilise la solution demandée pour résoudre le challenge
    challenge = parse_challenge(args.challenge)
    solver = AvailableSolutions.getFromName(args.solution)()
    challenge.setSolver(solver)
    solution = challenge.solve()
    challenge.removeEmptySchedule()
    challenge.removeUnused()

    if args.output is not None:
        # Sauvegarder le fichier généré
        export_file(solution, args.challenge.split("/")[-1].split(".")[0], args.output)

    # Calcule le score de la solution
    scorerResult = scorer(challenge, solution, args.v, args.d)

    # Génère un diagnostique si demandé
    if args.d:
        print("Generating diagnose")
        diagnose = exportCSV(scorerResult)
        with open("./diagnose/" + str(int(time.time())) + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(diagnose)
        print("Diagnose exported")

    print(f"Score: {scorerResult.score}")
