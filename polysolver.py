#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de résolution du projet Poly#.
"""
from enum import Enum
from solvers.empty import EmptySolver
from solvers.solver1 import EfficientSolver
from polystructure import Solver
from solvers.unused import UnusedStreetSolver

class AvailableSolutions(Enum):
    EMPTY : Solver = EmptySolver
    UNUSED : Solver = UnusedStreetSolver
    EFFICIENT : Solver = EfficientSolver
    
    def getFromName(name : str) -> Solver:
        for solution in AvailableSolutions:
            if solution.name.lower() == name.lower():
                return solution.value
        raise ValueError("Solution "+name+" not found")