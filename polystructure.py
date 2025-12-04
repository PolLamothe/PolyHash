#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module contenant les data stuctures utilisé durant le projet
"""

from __future__ import annotations
from dataclasses import dataclass

@dataclass
class RawStreet:
    sourceId : int
    destinationId : int
    name : str
    length : int

@dataclass
class RawCar:
    street : list[str]

@dataclass
class Street:
    street : str
    length : int
    source : Intersection
    destination : Intersection

@dataclass
class Schedule:
    time : int = 1

class Intersection:
    
    def __init__(self,id : int):
        self.id = id
        self.streets = []
        self.schedule : list[tuple[Street,Schedule]] = []

    def addStreet(self,street : Street):
        if street.__class__ is not Street:
            raise Exception(street," is not a Street")
        self.streets.append(street)
        self.schedule.append((street,Schedule()))

class Car:
    carIdCount = 0
    def __init__(self,streets : list[Street]):
        self.streets : list[Street] =  streets
        Car.carIdCount += 1
        self.id :int = Car.carIdCount

class DataManager:
    
    def __init__(self):
        self.streets : list[Street] = []
        self.intersections : dict[int,Intersection] = {}
        self.cars : list[Car] = []
    
    def addstreet(self,street : RawStreet) -> Street:
        source : Intersection = None
        if street.sourceId in self.intersections:
            source = self.intersections[street.sourceId]
        else:
            self.intersections[street.sourceId] = Intersection(street.sourceId)
            source = self.intersections[street.sourceId]

        destination : Intersection = None
        if street.destinationId in self.intersections:
            destination = self.intersections[street.destinationId]
        else:
            self.intersections[street.destinationId] = Intersection(street.destinationId)
            destination = self.intersections[street.destinationId]

        newstreet = Street(street.name,street.length,source,destination)
        destination.addStreet(newstreet)
        self.streets.append(newstreet)
        return newstreet
    
    def addCar(self,car : RawCar) -> Car:
        street : list[Street] = []
        for street1 in car.street:
            for street2 in self.streets:
                if street2.street == street1:
                    street.append(street2)
                    break
        if len(car.street) != len(street):
            raise Exception("Erreur insertion Car : street Inexistante : ")
        self.cars.append(Car(street))
        return Car(street)
    
class Challenge:
    """
    Classe formalisant toutes les infos du challenge à partir des données extraite du fichier
    """
    def __init__(self,
        duration : int,
        intersectionsNumber : int,
        streetsNumber : int,
        carsNumber : int,
        pointForFinishing : int,
        streets : list[RawStreet],
        car : list[RawCar]):
        self.duration = duration
        self.intersectionsNumber = intersectionsNumber
        self.streetsNumber = streetsNumber
        self.carsNumber = carsNumber
        self.pointForFinishing = pointForFinishing

        self.dataManager = DataManager()

        for street in streets:
            self.dataManager.addstreet(street)

        for car in car:
            self.dataManager.addCar(car)

        self.solver = None
    
    def setSolver(self,solver : Solver):
        if self.solver is not None:
            raise Exception("Solver already set")
        if solver is None:
            raise Exception("Solver is None")
        self.solver = solver
    
    def getSolver(self) -> Solver:
        if self.solver is None:
            raise Exception("Solver not set")
        return self.solver
    
class Solver:
    def solve(challenge : Challenge):
        raise NotImplementedError()

    def score_solution(solution):
        raise NotImplementedError()
    def save_solution(filename, solution):
        raise NotImplementedError()