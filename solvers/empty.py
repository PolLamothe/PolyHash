#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Solver vide pour tester la structure (toutes les rues sont au vert pendant une seconde)
"""

from polystructure import Challenge, Solver, Intersection

class EmptySolver(Solver):
    def solve(self, challenge: Challenge) -> list[Intersection]:
        intersections = challenge.getDataManager().getIntersections()
        return [intersection for intersection in intersections.values()]