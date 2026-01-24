#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementation d'un solveur qui donnera le plus de temps à la rue qui aura le plus de trafic
"""

from polystructure import Challenge, Intersection, Street, Solver

class MostUsedStreetsSolver(Solver):
    def solve(self, challenge: Challenge) -> list[Intersection]:
        listeIntersections: dict[Street, Intersection] = challenge.getDataManager().getIntersections()
        dict_rues: dict[str, int] = {}
        for car in challenge.getDataManager().getCars():
            rues: list[Street] = car.getStreets()
            for rue in rues:
                if rue.name in dict_rues:
                    dict_rues[rue.name]+=1
                else: dict_rues[rue.name] = 1

        dict_rues = dict(sorted(dict_rues.items(), key=lambda item: item[1]))

        for intersection in listeIntersections.values():
            if len(intersection.getStreets()) == 1:
                intersection.getSchedule()[0][1].time = 1
            else:    
                for i, (street, skdl) in enumerate(intersection.getSchedule()):
                    if street.name in dict_rues:
                        skdl.time = max(1, dict_rues[street.name] // 6)
        
        return [ intersection for intersection in listeIntersections.values() ]