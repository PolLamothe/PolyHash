#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""solveur trop meilleur que les autres
"""

from polystructure import Challenge, Solver, Intersection,Schedule
import copy

class UnusedStreetSolver(Solver):
    def solve(challenge : Challenge)->list[Intersection]:
        intersections = challenge.getDataManager().getIntersections()

        usedStreets = []
        startingStreets = []

        for car in challenge.getDataManager().getCars():
            for index,street in enumerate(car.getStreets()[:-1]):
                if index == 0:
                    startingStreets.append(street.name)
                usedStreets.append(street.name)

        for i in intersections.values():
            streets = copy.deepcopy(i.getStreets())
            for s in streets:
                if s.name in usedStreets:
                    i.updateSchedule(s,Schedule(1))
                else:
                    i.updateSchedule(s,Schedule(0))

        for i in intersections.values():
            for index,street in enumerate(i.getStreets()):
                if street.name in startingStreets:
                    i.changeOrder(i.getStreets()[0],street)

        return [intersection for intersection in intersections.values()]