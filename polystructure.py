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
        self.__id = id
        self.__streets : list[Street] = []
        self.__schedule : list[tuple[Street,Schedule]] = []

    def addStreet(self,street : Street):
        if not isinstance(street,Street):
            raise Exception(street," is not a Street")
        self.__streets.append(street)
        self.__schedule.append((street,Schedule()))

    def getId(self) -> int:
        return self.__id
    
    def getStreets(self) -> list[Street]:
        return self.__streets
    
    def getSchedule(self) -> list[tuple[Street,Schedule]]:
        return self.__schedule

class Car:
    carIdCount = 0
    def __init__(self,streets : list[Street]):
        self.__streets : list[Street] =  streets
        Car.carIdCount += 1
        self.__id :int = Car.carIdCount
    
    def getStreets(self) -> list[Street]:
        return self.__streets
    
    def getId(self) -> int:
        return self.__id

class DataManager:
    
    def __init__(self):
        self.__streets : list[Street] = []
        self.__intersections : dict[int,Intersection] = {}
        self.__cars : list[Car] = []
    
    def addstreet(self,street : RawStreet) -> Street:
        if not isinstance(street,RawStreet):
            raise Exception(street," is not a RawStreet")
        
        source : Intersection = None
        if street.sourceId in self.__intersections:
            source = self.__intersections[street.sourceId]
        else:
            self.__intersections[street.sourceId] = Intersection(street.sourceId)
            source = self.__intersections[street.sourceId]

        destination : Intersection = None
        if street.destinationId in self.__intersections:
            destination = self.__intersections[street.destinationId]
        else:
            self.__intersections[street.destinationId] = Intersection(street.destinationId)
            destination = self.__intersections[street.destinationId]

        newstreet = Street(street.name,street.length,source,destination)
        destination.addStreet(newstreet)
        self.__streets.append(newstreet)
        return newstreet
    
    def addCar(self,car : RawCar) -> Car:
        if not isinstance(car,RawCar):
            raise Exception(car," is not a RawCar")

        street : list[Street] = []
        for street1 in car.street:
            for street2 in self.__streets:
                if street2.street == street1:
                    street.append(street2)
                    break
        if len(car.street) != len(street):
            raise Exception("Erreur insertion Car : street Inexistante : ")
        self.__cars.append(Car(street))
        return Car(street)
    
    def getStreets(self) -> list[Street]:
        return self.__streets
    
    def getCars(self) -> list[Car]:
        return self.__cars
    
    def getIntersections(self) -> dict[int,Intersection]:
        return self.__intersections
    
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

        self.__duration = duration
        self.__intersectionsNumber = intersectionsNumber
        self.__streetsNumber = streetsNumber
        self.__carsNumber = carsNumber
        self.__pointForFinishing = pointForFinishing

        self.__dataManager = DataManager()

        for street in streets:
            self.__dataManager.addstreet(street)

        for car in car:
            self.__dataManager.addCar(car)

        self.__solver = None
    
    def setSolver(self,solver : Solver):
        if solver is None:
            raise Exception("Solver is None")
        self.__solver = solver
    
    def getSolver(self) -> Solver:
        if self.__solver is None:
            raise Exception("Solver not set")
        return self.__solver
    
    def getDuration(self) -> int:
        return self.__duration

    def getIntersectionsNumber(self) -> int:
        return self.__intersectionsNumber
    
    def getStreetsNumber(self) -> int:
        return self.__streetsNumber
    
    def getCarsNumber(self) -> int:
        return self.__carsNumber
    
    def getPointForFinishing(self) -> int:
        return self.__pointForFinishing
    
    def getDataManager(self) -> DataManager:
        return self.__dataManager
    
    def solve(self) -> list[Intersection]:
        if self.__solver is None:
            raise Exception("Solver not set")
        return self.__solver.solve(self)
    
class Solver:
    def solve(challenge : Challenge):
        raise NotImplementedError()

@dataclass
class ScorerIntersectionStreetHistory:
    greenState : bool
    waitingCars : int
    time : int

@dataclass
class ScorerIntersectionStreet:
    street : Street
    scorerIntersections : ScorerIntersection
    history : list[ScorerIntersectionStreetHistory]

@dataclass
class ScorerIntersection:
    intersection : Intersection
    streets : list[ScorerIntersectionStreet]

    def getScorerIntersection(scorerIntersections : list[ScorerIntersection],intersection : Intersection) -> ScorerIntersection:
        for scorerIntersection in scorerIntersections:
            if scorerIntersection.intersection == intersection:
                return scorerIntersection
        return None
    
    def getScorerIntersectionStreet(self,street : Street) -> ScorerIntersectionStreet:
        for scorerIntersectionStreet in self.streets:
            if scorerIntersectionStreet.street == street:
                return scorerIntersectionStreet
        return None

@dataclass
class ScorerResult:
    score : int
    intersections : list[ScorerIntersection]