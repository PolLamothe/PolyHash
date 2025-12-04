from __future__ import annotations
from polystructure import Challenge, Car, Street, Intersection
from polyparser import parse_challenge

class IntersectionSolver:
    dataManager: DataManagerSolver
    intersection: Intersection
    currentTurn: int
    timeLeft: int
    streets: list[StreetSolver]

    def __init__(self, intersection: Intersection, dataManager: DataManagerSolver):
        self.dataManager = dataManager
        self.intersection = intersection
        self.currentTurn = 0 if len(intersection.schedule) else -1
        self.timeLeft = intersection.schedule[0][1].time
        self.streets = []

    def initStreets(self):
        for street in self.intersection.streets:
            self.streets.append(self.dataManager.getStreetFromName(street.street))

    def decrementTimeLeft(self):
        if self.currentTurn == -1:
            return
        if self.timeLeft - 1 == 0:
            self.currentTurn = (self.currentTurn + 1) % len(self.intersection.schedule)
            self.timeLeft = self.schedule[self.currentTurn][1].time
    
    def isLightGreenForStreet(self, street: StreetSolver):
        """
        Renvoie vrai si le feu est vert pour la rue donnée en paramètre, et faux si la rue n'est pas liée à l'intersection ou si le feu est rouge.
        """
        if street not in self.streets:
            return False
        return self.intersection.schedule[self.currentTurn][0].street == street.street      

class StreetSolver:
    dataManager: DataManagerSolver
    street: Street
    carsWaitingAtLight: list[CarSolver] # Pile contenant les voitures
    intersectionAtEnd: IntersectionSolver

    def __init__(self, street: Street, dataManager: DataManagerSolver):
        self.dataManager = dataManager
        self.street = street
        self.carsWaitingAtLight = []
        self.intersectionAtEnd = dataManager.getIntersectionFromId(street.destination.id)
    
    def isLightGreen(self):
        return self.intersectionAtEnd.isLightGreenForStreet(self)
    
    def pushWaitingCar(self, car: CarSolver):
        self.carsWaitingAtLight.append(car)

    def getWaitingCarPosition(self, car: CarSolver):
        return next((index for index, item in enumerate(self.carsWaitingAtLight) if car.car.id == item.car.id), -1)
    
    def popWaitingCar(self):
        if self.intersectionAtEnd is None:
            raise AttributeError("No intersection at the end.")
        return self.carsWaitingAtLight.pop(0)

class CarSolver:
    dataManager: DataManagerSolver
    car: Car
    isArrived: bool
    currentStreet: StreetSolver | None
    currentStreetIndex: int
    timeLeftInStreet: int
    timeLost: int # Métrique pour connaître le temps attendu en trop

    def __init__(self, car: Car, dataManager: DataManagerSolver):
        self.dataManager = dataManager
        self.car = car
        self.isArrived = False
        self.currentStreetIndex = 0
        self.currentStreet = dataManager.getStreetFromName(car.streets[0].street)
        self.timeLeftInStreet = 0
        self.timeLost = 0
    
    def changeStreet(self):
        """
        La voiture passe à la rue suivante.
        Renvoie vrai si la voiture a terminé son trajet à ce tour, faux sinon
        """
        if self.isArrived:
            return False
        if self.currentStreetIndex + 1 == len(self.car.streets):
            self.isArrived = True
            return True
        self.currentStreetIndex += 1
        self.currentStreet = self.dataManager.getStreetFromName(self.car.streets[self.currentStreetIndex].street)
        self.timeLeftInStreet = self.currentStreet.street.length
        return False
    
    def decrementTimeLeft(self):
        """
        Décrémente le temps restant à parcourir la rue actuelle de la voiture.
        Renvoie vrai si la voiture attend au feu, faux si elle a terminé ou si elle est dans une rue.
        """
        if self.isArrived:
            return False
        res = False
        if self.timeLeftInStreet - 1 == 0:
            self.currentStreet.pushWaitingCar(self)
            res = True
        if self.timeLeftInStreet > 0:
            self.timeLeftInStreet -= 1
            return res
        else:
            self.timeLeftInStreet += 1
            return True

class DataManagerSolver:
    """
    Ordre de chargement:
    - Intersections
    - Rues
    - Rues au bout des intersections
    - Voitures
    """
    score: int
    cars: list[CarSolver]
    streets: list[StreetSolver]
    intersections: list[IntersectionSolver]

    def __init__(self):
        self.score = 0
        self.cars = []
        self.streets = []
        self.intersections = []
    
    def loadDataFromChallenge(self, challenge: Challenge):
        for intersection in challenge.dataManager.intersections.values():
            self.addIntersection(intersection)
        for street in challenge.dataManager.streets:
            self.addStreet(street)
        for intersection in self.intersections:
            intersection.initStreets()
        for car in challenge.dataManager.cars:
            self.addCar(car)

    def addCar(self, car: Car):
        self.cars.append(CarSolver(car, self))
    
    def addStreet(self, street: Street):
        self.streets.append(StreetSolver(street, self))

    def addIntersection(self, intersection: Intersection):
        self.intersections.append(IntersectionSolver(intersection, self))
    
    def getStreetFromName(self, name: str) -> StreetSolver | None:
        return next((s for s in self.streets if s.street.street == name), None)
    
    def getIntersectionFromId(self, id: int) -> IntersectionSolver | None:
        return next((i for i in self.intersections if i.intersection.id == id), None)

def tour(challenge: Challenge, dataManager: DataManagerSolver, t: int):
    if challenge.duration == t:
        return challenge

    for car in dataManager.cars:
        if car.isArrived:
            continue
        isAtEnd = car.decrementTimeLeft()
        if isAtEnd and car.currentStreet.getWaitingCarPosition(car) == 0 and car.currentStreet.isLightGreen():
            hasFinished = car.changeStreet()
            if hasFinished:
                dataManager.score += challenge.pointForFinishing + (challenge.duration - t)

    for intersection in dataManager.intersections:
        intersection.decrementTimeLeft()

def scorer(challenge: Challenge):
    dataManager = DataManagerSolver()
    dataManager.loadDataFromChallenge(challenge)
    # for i in range(1, challenge.duration + 1):
    #     tour(challenge, dataManager, i)
    return dataManager, dataManager.score



if __name__ == "__main__":
    challenge = parse_challenge("./challenges/a_example.in")
    dataManager, score = scorer(challenge)
    print(dataManager, score)