#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module principal pour la mise en oeuvre du projet Poly#.
"""

# Vous pouvez structurer votre code en modules pour améliorer la
# compréhension et faciliter le travail collaboratif
from polyparser import parse_challenge
#from polysolver import solve, score_solution, save_solution

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
    parser.add_argument('output', type=str, default=None,
                        help='output filename',
                        metavar="sortie.txt")
    args = parser.parse_args()

    challenge = parse_challenge(args.challenge)
    print(challenge.dataManager.streets)
    exit(0)
    solution = solve(challenge)
    if args.output is not None:
        # Sauvegarder le fichier généré
        save_solution(args.output, solution)
        print(f"Solution saved in {args.output}")
    print(f"Score: {score_solution(solution)}")
