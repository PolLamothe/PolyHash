#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module contenant les data stuctures utilisé durant le projet
"""

from dataclasses import dataclass

@dataclass
class RawRue:
    def __init__(self,sourceId : int, destinationId : int, name : str, length : int):
        self.sourceid = sourceId
        self.destinationId = destinationId
        self.name = name
        self.length = length

@dataclass
class RawVoiture:
    def __init__(self,rue : list[str]):
        self.rue = rue

class Challenge:
    def __init__(self,
        duration : int,
        intersectionsNumber : int,
        streetsNumber : int,
        carsNumber : int,
        pointForFinishing : int,
        streets : list[RawRue],
        voitures : list[RawVoiture]) -> DataManager:
        self.duration = duration
        self.intersectionsNumber = intersectionsNumber
        self.streetsNumber = streetsNumber
        self.carsNumber = carsNumber
        self.pointForFinishing = pointForFinishing

        dataManager = DataManager()

        for street in streets:
            dataManager.addRue(street)

        for voiture in voitures:
            dataManager.addVoiture(voiture)
        
        return dataManager

@dataclass
class Rue:
    
    def __init__(self,rue : str,length : int,source : Intersection, destination : Intersection):
        self.rue = rue
        self.length = length
        self.source = source
        self.destination = destination

@dataclass
class Schedule:

    def __init__(self, time : int = 1):
        self.time = time

@dataclass
class Intersection:
    
    def __init__(self,id : int,rues : list[Rue]):
        self.id = id
        self.rues = rues
        self.schedule : dict[Rue,Schedule] = {}
        #schedule par défaut
        for rue in rues:
            self.schedule[rue] = Schedule()
    
@dataclass
class Voiture:
    
    def __init__(self,rues : list[Rue]):
        self.rues = rues

class DataManager:
    
    def __init__(self):
        self.rues : list[Rue] = []
        self.intersections : dict[int,Intersection] = {}
    
    def addRue(self,rue : RawRue) -> Rue:
        source : Intersection = None
        if rue.sourceId in self.intersections:
            source = self.intersections
        else:
            source = Intersection(rue.sourceId,[])

        destination : Intersection = None
        if rue.destinationId in self.intersections:
            destination = self.intersections
        else:
            destination = Intersection(rue.destinationId,[])

        newRue = Rue(rue.name,rue.length,source,destination)
        source.rues.append(newRue)
        destination.rues.append(newRue)
        return newRue
    
    def addVoiture(self,voiture : RawVoiture) -> Voiture:
        rue : list[Rue] = []
        for rue1 in voiture.rue:
            for rue2 in self.rues:
                if rue2.rue == rue1:
                    rue.append(rue2)
                    break
        if len(voiture.rue) != rue:
            raise Exception("Erreur insertion Voiture : Rue Inexistante")
        return Voiture(rue)