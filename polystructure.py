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
    name : str
    length : int
    source : Intersection
    destination : Intersection

@dataclass
class Schedule:
    time : int = 1

class Intersection:
    
    def __init__(self,id : int):
        self.__id = int(id)
        self.__streets : list[Street] = []
        self.__schedule : list[tuple[Street,Schedule]] = []

    def addStreet(self,street : Street,schedule : Schedule = Schedule()):
        if not isinstance(street,Street):
            raise Exception(street," is not a Street")
        self.__streets.append(street)
        self.addSchedule(street,schedule)

    def getId(self) -> int:
        return self.__id
    
    def getStreets(self) -> list[Street]:
        return self.__streets
    
    def getSchedule(self,street : Street = None) -> list[tuple[Street,Schedule]]:
        if street == None:
            return self.__schedule
        for value in self.__schedule:
            if value[0] == street:
                return value[1]
        return None
    
    def updateSchedule(self, street: Street, schedule: Schedule):
        for index, value in enumerate(self.__schedule):
            if value[0].name == street.name:
                self.__schedule[index] = (value[0], schedule)
                return
        
        raise Exception("Cette intersection n'est pas liée à cette rue")
    
    def addSchedule(self,street : Street,schedule : Schedule):
        if self.getSchedule(street) == None:
            self.__schedule.append((street,schedule))
        else :
            raise Exception("Cette intersection possède déja un schedule")
    
    def deleteSchedule(self,street : Street):
        for index,value in enumerate(self.__schedule):
            if value[0] == street:
                self.__schedule.pop(index)
                return
        raise Exception("Cette intersection n'est pas liée à cette rue")
    
    def changeOrder(self,streetToReplace : Street,streetToPlace : Street):
        indexToReplace = None
        indexToPlace = None
        for index,value in enumerate(self.__streets):
            if value.name == streetToPlace.name:
                indexToPlace = index
            if value.name == streetToReplace.name:
                indexToReplace = index
        temp = self.__streets[indexToPlace]
        self.__streets[indexToPlace] = self.__streets[indexToReplace]
        self.__streets[indexToReplace] = temp

        for index,value in enumerate(self.__schedule):
            if value[0].name == streetToPlace.name:
                indexToPlace = index
            if value[0].name  == streetToReplace.name:
                indexToReplace = index
        temp = self.__schedule[indexToPlace]
        self.__schedule[indexToPlace] = self.__schedule[indexToReplace]
        self.__schedule[indexToReplace] = temp
    
    def __str__(self) -> str:
        return f'Intersection ID : {self.__id} | rues : {self.__streets} | schedules : {self.__schedule}'
    
    def removeEmptySchedule(self):
        newSchedule = []
        for index2,value2 in enumerate(self.__schedule):
            if value2[1].time == 0:
                self.__streets.remove(value2[0])
            else:
                newSchedule.append(value2)
        self.__schedule = newSchedule

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
        if street.sourceId in self.__intersections.keys():
            source = self.__intersections[street.sourceId]
        else:
            self.__intersections[street.sourceId] = Intersection(street.sourceId)
            source = self.__intersections[street.sourceId]

        destination : Intersection = None
        if street.destinationId in self.__intersections.keys():
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
                if street2.name == street1:
                    street.append(street2)
                    break
        if len(car.street) != len(street):
            raise Exception("Erreur insertion Car : street Inexistante : ")
        self.__cars.append(Car(street))
        return self.__cars[-1]
    
    def removeUnused(self):
        deleteId = []
        for id in self.__intersections:
            if len(self.__intersections[id].getStreets()) == 0:
                deleteId.append(id)
        for id in deleteId:
            del self.__intersections[id]

    
    def getStreets(self) -> list[Street]:
        return self.__streets
    
    def getCars(self) -> list[Car]:
        return self.__cars
    
    def getIntersections(self) -> dict[int,Intersection]:
        return self.__intersections
    
    def removeEmptySchedule(self):
        for intersection in self.__intersections.values():
            intersection.removeEmptySchedule()

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
    
    def removeUnused(self):
        self.__dataManager.removeUnused()

    def removeEmptySchedule(self):
        self.__dataManager.removeEmptySchedule()
    
class Solver:
    def solve(challenge : Challenge) -> list[Intersection]:
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
            if scorerIntersectionStreet.street.name == street.name:
                return scorerIntersectionStreet
        return None

@dataclass
class ScorerResult:
    score : int
    intersections : list[ScorerIntersection]