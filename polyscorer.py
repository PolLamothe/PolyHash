#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module calculant le score d'une solution à un challenge.
"""

from __future__ import annotations
from collections import deque
from polystructure import Challenge, Car, Street, Intersection, ScorerResult, ScorerIntersectionStreet, ScorerIntersection, ScorerIntersectionStreetHistory, ScorerCar
from polyparser import parse_challenge

"""
Représente une intersection lors de l'exécution de la simulation.
"""
class IntersectionSolver:
    dataManager: DataManagerSolver
    intersection: Intersection
    currentTurn: int
    timeLeft: int
    streets: list[StreetSolver]
    schedule_len: int

    def __init__(self, intersection: Intersection, dataManager: DataManagerSolver):
        self.dataManager = dataManager
        self.intersection = intersection
        
        schedule = intersection.getSchedule()
        self.schedule_len = len(schedule)
        
        self.currentTurn = 0 if self.schedule_len else -1
        self.timeLeft = schedule[0][1].time if self.schedule_len else 0
        
        self.streets = []
        if dataManager.verbose: print(f" I{intersection.getId()} instanciée")

    def initStreets(self) -> None:
        """
        Initialise la liste des rues de l'intersection à partir du planning de l'intersection.
        """
        for street, _ in self.intersection.getSchedule():
            st_solver = self.dataManager.getStreetFromName(street.name)
            if st_solver:
                self.streets.append(st_solver)

    def decrementTimeLeft(self) -> None:
        """
        Fait passer un tour à l'intersection.
        """
        if self.currentTurn == -1:
            return
        
        self.timeLeft -= 1
        if self.timeLeft <= 0:
            self.currentTurn = (self.currentTurn + 1) % self.schedule_len
            self.timeLeft = self.intersection.getSchedule()[self.currentTurn][1].time
    
    def getGreenStreet(self) -> StreetSolver:
        """
        Récupère la rue qui a le feu au vert.

        Sortie :
        La rue en question
        """
        return self.streets[self.currentTurn]
    
    def isLightGreenForStreet(self, street: StreetSolver) -> bool:
        """
        Retourne vrai si la rue en paramètre a le feu vert, faux sinon.

        Entrées :
        - street : L'objet représentant la rue en question.

        Sortie :
        Booléen
        """
        green_street = self.getGreenStreet()
        return green_street is street
    
    def __str__(self) -> str:
        return f"(IntersectionSolver I{self.intersection.getId()})"
    
    def __repr__(self) -> str:
        return self.__str__()

"""
Représente une rue lors de l'exécution de la simulation.
carsWaitingAtLight est une file.
"""
class StreetSolver:
    dataManager: DataManagerSolver
    street: Street
    carsWaitingAtLight: deque[CarSolver]
    intersectionAtEnd: IntersectionSolver

    def __init__(self, street: Street, dataManager: DataManagerSolver):
        self.dataManager = dataManager
        self.street = street
        self.carsWaitingAtLight = deque()
        self.intersectionAtEnd = dataManager.getIntersectionFromId(street.destination.getId())
        if dataManager.verbose: print(f" R{street.name} instanciée")
    
    def isLightGreen(self) -> bool:
        """
        Retourne vrai si la rue a le feu vert, faux sinon.

        Sortie :
        Booléen
        """
        return self.intersectionAtEnd.isLightGreenForStreet(self)
    
    def pushWaitingCar(self, car: CarSolver) -> None:
        """
        Ajoute une voiture à la file de voiture attendant au feu.

        Entrées :
        - car : L'objet représentant la voiture en question.
        """
        self.carsWaitingAtLight.append(car)

    def popWaitingCar(self) -> CarSolver | None:
        """
        Récupère la première voiture attendant au feu.

        Sortie :
        La première voiture s'il y en a une, None sinon.
        """
        if not self.carsWaitingAtLight:
            return None
        return self.carsWaitingAtLight.popleft()

    def __str__(self) -> str:
        return f"(StreetSolver R{self.street.name})"
    
    def __repr__(self) -> str:
        return self.__str__()

"""
Représente une voiture lors de l'exécution de la simulation.
"""
class CarSolver:
    dataManager: DataManagerSolver
    car: Car
    isArrived: bool
    currentStreet: StreetSolver | None
    currentStreetIndex: int
    timeLeftInStreet: int
    waitingAtLight: bool
    timeLost: int
    path_solvers: list[StreetSolver]

    def __init__(self, car: Car, dataManager: DataManagerSolver):
        self.dataManager = dataManager
        self.car = car
        self.isArrived = False
        self.currentStreetIndex = 0
        
        raw_streets = car.getStreets()
        self.path_solvers = [dataManager.getStreetFromName(s.name) for s in raw_streets]
        self.path_len = len(self.path_solvers)
        
        self.currentStreet = self.path_solvers[0]
        self.timeLeftInStreet = 0
        self.timeLost = 0
        self.waitingAtLight = True
        self.currentStreet.pushWaitingCar(self)
        if dataManager.verbose: print(f" V{car.getId()} instanciée")
    
    def changeStreet(self) -> None:
        """
        Passe à la rue suivante  dans l'itinéraire.
        """
        if self.isArrived:
            return

        self.currentStreetIndex += 1
        self.currentStreet = self.path_solvers[self.currentStreetIndex]

        self.waitingAtLight = False
        self.timeLeftInStreet = self.currentStreet.street.length - 1
        return
    
    def decrementTimeLeft(self) -> bool:
        """
        Fait passer un tour à la voiture.

        Sortie :
        Renvoie vrai si la voiture est arrivée à la fin de son itinéraire, faux sinon.
        """
        if self.isArrived:
            return True

        if self.timeLeftInStreet == 0 and not self.waitingAtLight:
            if self.currentStreetIndex + 1 == self.path_len:
                self.isArrived = True
                self.dataManager.addScore()
                if self.dataManager.verbose: print(f"   V{self.car.getId()} : Arrivée à destination")
                return True
            
            self.waitingAtLight = True
            self.currentStreet.pushWaitingCar(self)
        
        if self.timeLeftInStreet > 0:
            self.timeLeftInStreet -= 1
        else:
            self.timeLost += 1
        
        return False
    
    def __str__(self) -> str:
        return f"(CarSolver V{self.car.getId()})"
    
    def __repr__(self) -> str:
        return self.__str__()

"""
Représente toutes les données en mémoire lors de l'exécution de la simulation.
"""
class DataManagerSolver:
    t: int
    score: int
    challenge: Challenge
    cars: list[CarSolver]
    activeCars: list[CarSolver]
    streets: list[StreetSolver]
    intersections: list[IntersectionSolver]
    
    _streets_map: dict[str, StreetSolver]
    _intersections_map: dict[int, IntersectionSolver]
    
    verbose: bool

    def __init__(self, challenge: Challenge, intersections: list[Intersection], verbose: bool = False):
        self.t = 1
        self.score = 0
        self.challenge = challenge
        self.cars = []
        self.activeCars = []
        self.streets = []
        self.intersections = []
        self._streets_map = {}
        self._intersections_map = {}
        self.verbose = verbose

        for intersection in intersections:
            self.addIntersection(intersection)
        for street in challenge.getDataManager().getStreets():
            self.addStreet(street)
        for intersection in self.intersections:
            intersection.initStreets()
        for car in challenge.getDataManager().getCars():
            self.addCar(car)

    def addCar(self, car: Car) -> None:
        """
        Ajoute une voiture à la simulation.

        Entrées :
        - car : L'objet représentant la voiture en question.
        """
        c = CarSolver(car, self)
        self.cars.append(c)
        self.activeCars.append(c)
    
    def addStreet(self, street: Street) -> None:
        """
        Ajoute une rue à la simulation.

        Entrées :
        - rue : L'objet représentant la rue en question.
        """
        s = StreetSolver(street, self)
        self.streets.append(s)
        self._streets_map[street.name] = s

    def addIntersection(self, intersection: Intersection) -> None:
        """
        Ajoute une intersection à la simulation.

        Entrées :
        - intersection : L'objet représentant l'intersection en question.
        """
        i = IntersectionSolver(intersection, self)
        self.intersections.append(i)
        self._intersections_map[intersection.getId()] = i
    
    def getStreetFromName(self, name: str) -> StreetSolver | None:
        return self._streets_map.get(name)
    
    def getIntersectionFromId(self, id: int) -> IntersectionSolver | None:
        return self._intersections_map.get(id)
    
    def addScore(self) -> None:
        """
        Ajoute au score le nombre de points correspondant au tour actuel.
        """
        self.score += self.challenge.getPointForFinishing() + (self.challenge.getDuration() - (self.t))

def tour(dataManager: DataManagerSolver, t: int, diagnose_links: list[tuple[StreetSolver, ScorerIntersectionStreet]]) -> None:
    """
    Exécute un tour de la simulation.

    Entrées :
    - dataManager : La mémoire de la simulation
    - t : Le numéro du tour actuel
    - diagnose_links : Données utiles à l'outil de diagnostique
    """
    if dataManager.verbose:
        print(f"Tour n°{t}")

    dataManager.t = t

    # Traite le tour des voitures
    next_active_cars = []
    for car in dataManager.activeCars:
        just_arrived = car.decrementTimeLeft()
        if not just_arrived:
            next_active_cars.append(car)
    dataManager.activeCars = next_active_cars

    if diagnose_links:
        for street_solver, scorer_street in diagnose_links:
            scorer_street.history.append(
                ScorerIntersectionStreetHistory(
                    street_solver.isLightGreen(),
                    len(street_solver.carsWaitingAtLight),
                    t,
                    scorer_street
                )
            )

    # Traite le tour des intersections
    for intersection in dataManager.intersections:
        if intersection.currentTurn != -1:
            street = intersection.getGreenStreet()
            car = street.popWaitingCar()
            if car:
                car.changeStreet()
        intersection.decrementTimeLeft()

def scorer(challenge: Challenge, intersections: list[Intersection], verbose: bool = False, diagnose: bool = False) -> ScorerResult:
    """
    Calcule les résultats de la simulation.

    Entrées :
    - challenge : L'objet contenant le challenge à résoudre
    - intersections : La liste des intersections
    - verbose : Affiche des logs à chaque étape importante
    - diagnose : Exporte un diagnostique

    Sortie :
    Dataclass ScorerResult
    """
    if verbose: print("== Création des instances ==")
    dataManager = DataManagerSolver(challenge, intersections, verbose = verbose)

    scorerIntersections = []
    diagnose_links = []
    scorerCars = {}

    if diagnose:
        scorer_streets_map = {}

        for intersection in intersections:
            sc_inter = ScorerIntersection(intersection, [])
            scorerIntersections.append(sc_inter)
            
            for street in intersection.getStreets():
                sc_street = ScorerIntersectionStreet(street, sc_inter, [])
                sc_inter.streets.append(sc_street)
                scorer_streets_map[street.name] = sc_street
        
        for inter_solver in dataManager.intersections:
            for street_solver in inter_solver.streets:
                sc_street_target = scorer_streets_map.get(street_solver.street.name)
                if sc_street_target:
                    diagnose_links.append((street_solver, sc_street_target))
    
    if dataManager.verbose: print("== Début de la simulation ==")
    
    duration = challenge.getDuration()
    for i in range(0, duration + 1):
        tour(dataManager, i, diagnose_links)

    for car in dataManager.cars:
        scorerCars[car.car] = ScorerCar(car.isArrived, car.car)
        
    if dataManager.verbose:
        print("== Fin de la simulation ==")
        print(f"Le score final est de {dataManager.score}.")
        
    return ScorerResult(dataManager.score, scorerIntersections, scorerCars)

def exportCSV(scorerResult : ScorerResult) -> list:
    """
    Exporte le CSV du diagnostique

    Entrées :
    - scorerResult

    Sortie :
    CSV contenant toutes les informations (sous forme de matrice)
    """
    result = [["IntersectionId", "StreetName", "Time", "GreenState", "WaitingCars"]]
    for intersection in scorerResult.intersections:
        for street in intersection.streets:
            for data in street.history:
                result.append([intersection.intersection.getId(), street.street.name, data.time, data.greenState, data.waitingCars])
    return result

if __name__ == "__main__":
    challenge = parse_challenge("./challenges/b_ocean.in")
    scorer(challenge)