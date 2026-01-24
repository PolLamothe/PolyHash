#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module contenant les data stuctures utilisé durant le projet.
"""

from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class RawStreet:
    sourceId: int
    destinationId: int
    name: str
    length: int

@dataclass
class RawCar:
    street: list[str]

@dataclass
class Street:
    name: str
    length: int
    source: Intersection
    destination: Intersection
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if isinstance(other, Street):
            return self.name == other.name
        return False

@dataclass
class Schedule:
    time: int = 1

"""
Objet contenant toutes les données d'une intersection.
"""
class Intersection:
    __id: int

    __streets: list[Street]
    __streets_map: dict[str, Street]

    __schedule: list[tuple[Street,Schedule]]
    __schedule_map: dict[str, Schedule]

    def __init__(self, id: int):
        self.__id = int(id)
        self.__streets: list[Street] = []
        self.__streets_map: dict[str, Street] = {} 
        
        self.__schedule: list[tuple[Street,Schedule]] = []
        self.__schedule_map: dict[str, Schedule] = {}

    def addStreet(self, street: Street, schedule: Schedule = Schedule()):
        """
        Ajoute une rue à l'intersection.

        Entrées :
        - street : La rue en question
        - schedule : Le planning de la rue
        """
        if not isinstance(street, Street):
            raise Exception(street, " is not a Street")
        
        self.__streets.append(street)
        self.__streets_map[street.name] = street
        self.addSchedule(street, schedule)

    def getId(self) -> int:
        return self.__id
    
    def getStreets(self) -> list[Street]:
        return self.__streets
    
    def getStreetByName(self, name: str) -> Street:
        return self.__streets_map.get(name)
    
    def getSchedule(self, street: Street = None) -> list[tuple[Street, Schedule]] | Schedule:
        if street == None:
            return self.__schedule
        return self.__schedule_map.get(street.name)
    
    def updateSchedule(self, street: Street, schedule: Schedule):
        """
        Met à jour le planning d'une rue.

        Entrées :
        - street : La rue
        - schedule : Le nouvea planning modifié de la rue
        """
        if street.name not in self.__schedule_map:
             raise Exception("Cette intersection n'est pas liée à cette rue")
        
        self.__schedule_map[street.name] = schedule
        
        for index, value in enumerate(self.__schedule):
            if value[0].name == street.name:
                self.__schedule[index] = (value[0], schedule)
                return
        
    def addSchedule(self, street: Street, schedule: Schedule):
        """
        Ajoute un planning à une rue.

        Entrées :
        - street : La rue
        - schedule : Le nouveau planning de la rue
        """
        if street.name not in self.__schedule_map:
            self.__schedule.append((street, schedule))
            self.__schedule_map[street.name] = schedule
        else :
            raise Exception("Cette intersection possède déja un schedule pour cette rue")
    
    def deleteSchedule(self, street: Street):
        """
        Supprime le planning d'une rue.

        Entrées :
        - street : la rue
        """
        if street.name in self.__schedule_map:
            del self.__schedule_map[street.name]
            for index,value in enumerate(self.__schedule):
                if value[0] == street:
                    self.__schedule.pop(index)
                    return
        else:
            raise Exception("Cette intersection n'est pas liée à cette rue")
    
    def changeOrder(self, streetToReplace: Street, streetToPlace: Street):
        """
        Déplace la position d'une rue dans le planning

        Entrées :
        - streetToReplace : La rue à remplacer
        - streetToPlace : La rue à laquelle placer
        """
        indexToReplace = None
        indexToPlace = None
        for index, value in enumerate(self.__streets):
            if value.name == streetToPlace.name:
                indexToPlace = index
            if value.name == streetToReplace.name:
                indexToReplace = index
                
        if indexToPlace is not None and indexToReplace is not None:
            self.__streets[indexToPlace], self.__streets[indexToReplace] = self.__streets[indexToReplace], self.__streets[indexToPlace]

        indexToReplace = None
        indexToPlace = None
        for index, value in enumerate(self.__schedule):
            if value[0].name == streetToPlace.name:
                indexToPlace = index
            if value[0].name  == streetToReplace.name:
                indexToReplace = index
                
        if indexToPlace is not None and indexToReplace is not None:
            self.__schedule[indexToPlace], self.__schedule[indexToReplace] = self.__schedule[indexToReplace], self.__schedule[indexToPlace]
    
    def __str__(self) -> str:
        return f'Intersection ID : {self.__id} | rues : {self.__streets} | schedules : {self.__schedule}'
    
    def removeEmptySchedule(self):
        """
        Supprime les planning ayant un temps d'allumage de 0.
        """
        newSchedule = []
        self.__schedule_map.clear()
        
        streets_to_keep = []
        self.__streets_map.clear()

        for value2 in self.__schedule:
            if value2[1].time == 0:
                pass
            else:
                newSchedule.append(value2)
                self.__schedule_map[value2[0].name] = value2[1]
                streets_to_keep.append(value2[0])
                self.__streets_map[value2[0].name] = value2[0]

        self.__schedule = newSchedule
        self.__streets = [s for s in self.__streets if s in streets_to_keep] 

    def __hash__(self):
        return hash(str(self))

"""
Objet contenant toutes les données d'une voiture.
"""
class Car:
    carIdCount = 0

    __id: int
    __streets: list[Street]

    def __init__(self, streets: list[Street]):
        self.__streets: list[Street] = streets
        Car.carIdCount += 1
        self.__id: int = Car.carIdCount
    
    def getStreets(self) -> list[Street]:
        return self.__streets
    
    def getId(self) -> int:
        return self.__id

"""
Objet contenant toutes les données en mémoire du challenge.
"""
class DataManager:
    __streets: list[Street]
    __streets_map: dict[str, Street]
    __intersections: dict[int, Intersection]
    __cars: list[Car]

    def __init__(self):
        self.__streets: list[Street] = []
        self.__streets_map: dict[str, Street] = {}
        
        self.__intersections: dict[int, Intersection] = {}
        self.__cars: list[Car] = []
    
    def addStreet(self, street: RawStreet) -> Street:
        """
        Ajoute une rue.

        Entrées :
        - street : La rue à ajouter

        Sortie :
        La rue parsée
        """
        if not isinstance(street, RawStreet):
            raise Exception(street, " is not a RawStreet")
        
        source: Intersection = None
        if street.sourceId in self.__intersections.keys():
            source = self.__intersections[street.sourceId]
        else:
            self.__intersections[street.sourceId] = Intersection(street.sourceId)
            source = self.__intersections[street.sourceId]

        destination: Intersection = None
        if street.destinationId in self.__intersections.keys():
            destination = self.__intersections[street.destinationId]
        else:
            self.__intersections[street.destinationId] = Intersection(street.destinationId)
            destination = self.__intersections[street.destinationId]

        newstreet = Street(street.name, street.length, source, destination)
        destination.addStreet(newstreet)
        
        self.__streets.append(newstreet)
        self.__streets_map[newstreet.name] = newstreet # Indexation
        
        return newstreet
    
    def addCar(self, car : RawCar) -> Car:
        """
        Ajoute une voiture.

        Entrées :
        - car : La voiture à ajouter

        Sortie :
        La voiture parsée
        """
        if not isinstance(car, RawCar):
            raise Exception(car, " is not a RawCar")

        street: list[Street] = []
        
        for street_name in car.street:
            if street_name in self.__streets_map:
                street.append(self.__streets_map[street_name])
            else:
                raise Exception(f"Erreur insertion Car : street Inexistante : {street_name}")
                
        self.__cars.append(Car(street))
        return self.__cars[-1]
    
    def removeUnused(self):
        """
        Supprime toutes les intersections n'ayant aucune rue rattachée à celle-ci.
        """
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
    
    def getIntersections(self) -> dict[int, Intersection]:
        return self.__intersections
    
    def removeEmptySchedule(self):
        """
        Supprime les planning ayant un temps d'allumage de 0.
        """
        for intersection in self.__intersections.values():
            intersection.removeEmptySchedule()

class Challenge:
    """
    Classe formalisant toutes les infos du challenge à partir des données extraite du fichier
    """

    __duration: int
    __intersectionsNumber: int
    __streetsNumber: int
    __carsNumber: int
    __pointForFinishing: int

    __dataManager: DataManager
    __solver: Solver | None

    def __init__(self,
        duration: int,
        intersectionsNumber: int,
        streetsNumber: int,
        carsNumber: int,
        pointForFinishing: int,
        streets: list[RawStreet],
        car: list[RawCar]):

        self.__duration = duration
        self.__intersectionsNumber = intersectionsNumber
        self.__streetsNumber = streetsNumber
        self.__carsNumber = carsNumber
        self.__pointForFinishing = pointForFinishing

        self.__dataManager = DataManager()

        for street in streets:
            self.__dataManager.addStreet(street)

        for car in car:
            self.__dataManager.addCar(car)

        self.__solver = None
    
    def setSolver(self, solver: Solver):
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

# Classe uniquement utilisée pour le typage et pour être étendue
class Solver:
    def solve(challenge: Challenge) -> list[Intersection]:
        raise NotImplementedError()

@dataclass
class ScorerIntersectionStreetHistory:
    greenState: bool
    waitingCars: int
    time: int
    scorerIntersectionStreet: ScorerIntersectionStreet

@dataclass
class ScorerIntersectionStreet:
    street: Street
    scorerIntersections: ScorerIntersection
    history: list[ScorerIntersectionStreetHistory]

    def getStateAtInstant(self, time: int) -> ScorerIntersectionStreetHistory:
        if 0 <= time < len(self.history) and self.history[time].time == time:
             return self.history[time]
        
        for data in self.history:
            if data.time == time:
                return data
        return None
    
    def __hash__(self):
        return hash(self.street) + hash(self.scorerIntersections)

@dataclass
class ScorerIntersection:
    intersection: Intersection
    streets: list[ScorerIntersectionStreet]
    _streets_map: dict[str, ScorerIntersectionStreet] = field(default_factory=dict, repr=False)

    def __post_init__(self):
        if self.streets:
            for s in self.streets:
                self._streets_map[s.street.name] = s

    @staticmethod
    def getScorerIntersection(scorerIntersections: list[ScorerIntersection] | dict[int, ScorerIntersection], intersection: Intersection) -> ScorerIntersection:
        if isinstance(scorerIntersections, dict):
            return scorerIntersections.get(intersection.getId())
            
        for scorerIntersection in scorerIntersections:
            if scorerIntersection.intersection.getId() == intersection.getId():
                return scorerIntersection
        raise Exception("Cette intersection n'est pas dans la liste fourni")
    
    def getScorerIntersectionStreet(self, street: Street) -> ScorerIntersectionStreet:
        if self._streets_map and street.name in self._streets_map:
            return self._streets_map[street.name]
            
        for scorerIntersectionStreet in self.streets:
            if scorerIntersectionStreet.street.name == street.name:
                return scorerIntersectionStreet
        raise Exception("Cette rue n'est pas dans cette intersection")
    
    def getGreeenStreetAtInstant(self, instant: int) -> ScorerIntersectionStreetHistory:
        for street in self.streets:
            state = street.getStateAtInstant(instant)
            if state and state.greenState:
                return state
        raise Exception("Aucune rue n'était verte")
    
    def __hash__(self):
        return hash(self.intersection)

@dataclass
class ScorerCar:
    finished: bool
    car: Car

@dataclass
class ScorerResult:
    score: int
    intersections: list[ScorerIntersection]
    cars: dict[Car, ScorerCar]
    
    def getIntersectionsMap(self) -> dict[int, ScorerIntersection]:
        return {i.intersection.getId(): i for i in self.intersections}