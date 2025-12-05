#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module principal pour la mise en oeuvre du projet Poly#.
"""

# Vous pouvez structurer votre code en modules pour améliorer la
# compréhension et faciliter le travail collaboratif
from polyparser import parse_challenge
from polystructure import Challenge,Solver
from polysolver import AvailableSolutions
from polyscorer import scorer
from polyexport import export_file

if __name__ == "__main__":
    # La syntaxe exigée pour appeler le programme est
    # polyhash.py chemin/fichier_entree.txt chemin/fichier_sortie.txt

    # On fournit ici un exemple permettant de passer en paramètre le
    # fichier du challenge et le fichier de sortie. N'hésitez pas si
    # besoin à compléter avec d'autres paramètres/options - en
    # conservant la possibilité de l'appel ci-dessus - en consultant
    # la documentation du module argparse:
    # https://docs.python.org/3/library/argparse.html

    import argparse
    parser = argparse.ArgumentParser(description='Solve Poly# challenge.')
    parser.add_argument('challenge', type=str,
                        help='challenge definition filename',
                        metavar="challenge.txt")
    parser.add_argument('solution', type=str, default="empty",
                        help='solution program')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='output filename',
                        metavar="sortie.txt")
    parser.add_argument('-v',help='verbose mode',action="store_true")

    args = parser.parse_args()

    challenge = parse_challenge(args.challenge)
    challenge.setSolver(AvailableSolutions.getFromName(args.solution))
    solution = challenge.solve()
    if args.output is not None:
        # Sauvegarder le fichier généré
        export_file(solution,args.challenge.split("/")[-1].split(".")[0],args.output)
    print(f"Score: {scorer(challenge,solution,args.v)}")
