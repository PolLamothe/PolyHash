#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de résolution du projet Poly#.
"""
from enum import Enum
from solvers.empty import EmptySolver
from polystructure import Solver

class AvailableSolutions(Enum):
    EMPTY : Solver = EmptySolver

    def getFromName(name : str) -> Solver:
        for solution in AvailableSolutions:
            if solution.name.lower() == name.lower():
                return solution.value
        raise ValueError("Solution "+name+" not found")