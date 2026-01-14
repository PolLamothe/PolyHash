#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de résolution du projet Poly#.
"""
from enum import Enum
from solvers.empty import EmptySolver
from solvers.mostused import MostUsedStreetsSolver
from polystructure import Solver
from solvers.unused import UnusedStreetSolver
from solvers.intersectionsolver import IntersectionSolver

class AvailableSolutions(Enum):
    EMPTY : Solver = EmptySolver
    UNUSED : Solver = UnusedStreetSolver
    MOSTUSED : Solver = MostUsedStreetsSolver
    INTERSECTIONSOLVER : Solver = IntersectionSolver

    def getFromName(name : str) -> Solver:
        for solution in AvailableSolutions:
            if solution.name.lower() == name.lower():
                return solution.value
        raise ValueError("Solution "+name+" not found")
