from __future__ import annotations
from polystructure import Challenge, Car, Street, Intersection,ScorerResult,ScorerIntersectionStreet,ScorerIntersection,ScorerIntersectionStreetHistory
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
        self.currentTurn = 0 if len(intersection.getSchedule()) else -1
        self.timeLeft = intersection.getSchedule()[0][1].time
        self.streets = []
        if dataManager.verbose: print(f" I{intersection.getId()} instanciée")

    def initStreets(self):
        for street, _ in self.intersection.getSchedule():
            self.streets.append(self.dataManager.getStreetFromName(street.street))

    def decrementTimeLeft(self):
        if self.currentTurn == -1:
            if self.dataManager.verbose: print(f"    I{self.intersection.id} /!\\ : Toujours rouge")
            return
        if self.timeLeft - 1 == 0:
            self.currentTurn = (self.currentTurn + 1) % len(self.intersection.getSchedule())
            self.timeLeft = self.intersection.getSchedule()[self.currentTurn][1].time
            if self.dataManager.verbose: print(f"    I{self.intersection.getId()} : {self.streets[self.currentTurn].street.street} est vert")
        else:
            self.timeLeft -= 1
    
    def getGreenStreet(self) -> StreetSolver:
        return self.streets[self.currentTurn]
    
    def isLightGreenForStreet(self, street: StreetSolver):
        """
        Renvoie vrai si le feu est vert pour la rue donnée en paramètre, et faux si la rue n'est pas liée à l'intersection ou si le feu est rouge.
        """
        return self.getGreenStreet().street.street == street.street.street
    
    def __str__(self):
        return f"(IntersectionSolver I{self.intersection.id})"
    
    def __repr__(self):
        return self.__str__()

class StreetSolver:
    dataManager: DataManagerSolver
    street: Street
    carsWaitingAtLight: list[CarSolver] # Pile contenant les voitures
    intersectionAtEnd: IntersectionSolver

    def __init__(self, street: Street, dataManager: DataManagerSolver):
        self.dataManager = dataManager
        self.street = street
        self.carsWaitingAtLight = []
        self.intersectionAtEnd = dataManager.getIntersectionFromId(street.destination.getId())
        if dataManager.verbose: print(f" R{street.street} instanciée")
    
    def isLightGreen(self):
        return self.intersectionAtEnd.isLightGreenForStreet(self)
    
    def pushWaitingCar(self, car: CarSolver):
        self.carsWaitingAtLight.append(car)

    def getWaitingCarPosition(self, car: CarSolver):
        return next((index for index, item in enumerate(self.carsWaitingAtLight) if car.car.id == item.car.id), -1)
    
    def popWaitingCar(self) -> CarSolver | None:
        if self.intersectionAtEnd is None:
            raise AttributeError("No intersection at the end.")
        if not self.carsWaitingAtLight:
            return None
        return self.carsWaitingAtLight.pop(0)

    def __str__(self):
        return f"(StreetSolver R{self.street.streets})"
    
    def __repr__(self):
        return self.__str__()

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
        self.currentStreet = dataManager.getStreetFromName(car.getStreets()[0].street)
        self.timeLeftInStreet = 0
        self.timeLost = 0
        self.currentStreet.pushWaitingCar(self)
        if dataManager.verbose: print(f" V{car.getId()} instanciée")
    
    def changeStreet(self):
        """
        La voiture passe à la rue suivante.
        """
        if self.isArrived:
            return
        oldStreet = self.currentStreet.street.street
        self.currentStreetIndex += 1
        self.currentStreet = self.dataManager.getStreetFromName(self.car.getStreets()[self.currentStreetIndex].street)
        self.timeLeftInStreet = int(self.currentStreet.street.length)
        if self.dataManager.verbose: print(f"    V{self.car.getId()} : {oldStreet} -> {self.currentStreet.street.street}")
        return
    
    def decrementTimeLeft(self):
        """
        Décrémente le temps restant à parcourir la rue actuelle de la voiture.
        """
        if self.isArrived:
            return
        if self.timeLeftInStreet - 1 == 0:
            if self.currentStreetIndex + 1 == len(self.car.getStreets()):
                self.currentStreetIndex += 1
                self.isArrived = True
                self.dataManager.addScore()
                if self.dataManager.verbose: print(f"   V{self.car.getId()} : Arrivée à destination")
                return
            self.currentStreet.pushWaitingCar(self)
        if self.timeLeftInStreet > 0:
            self.timeLeftInStreet -= 1
        else:
            self.timeLost += 1
    
    def __str__(self):
        return f"(CarSolver V{self.car.id})"
    
    def __repr__(self):
        return self.__str__()

class DataManagerSolver:
    """
    Ordre de chargement:
    - Intersections
    - Rues
    - Rues au bout des intersections
    - Voitures
    """
    t: int
    score: int
    challenge: Challenge
    cars: list[CarSolver]
    streets: list[StreetSolver]
    intersections: list[IntersectionSolver]
    verbose: bool

    def __init__(self, challenge: Challenge, intersections : list[Intersection], verbose: bool = False):
        self.t = 1
        self.score = 0
        self.challenge = challenge
        self.cars = []
        self.streets = []
        self.intersections = []
        self.verbose = verbose

        for intersection in intersections:
            self.addIntersection(intersection)
        for street in challenge.getDataManager().getStreets():
            self.addStreet(street)
        for intersection in self.intersections:
            intersection.initStreets()
        for car in challenge.getDataManager().getCars():
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
        return next((i for i in self.intersections if i.intersection.getId() == id), None)
    
    def addScore(self):
        self.score += self.challenge.getPointForFinishing() + (self.challenge.getDuration() - (self.t - 1))

def tour(dataManager: DataManagerSolver, t: int,scorerIntersections : list[ScorerIntersection]):
    if dataManager.verbose:
        print(f"Tour n°{t}")
        print("  Score actuel :", dataManager.score)
        print("  Nombre de voitures inactives :", len([c for c in dataManager.cars if c.timeLeftInStreet == 0]))
        print("  Temps perdu :", sum([c.timeLost for c in dataManager.cars]))
        print("  Nombre de voitures sorties :", len([c for c in dataManager.cars if c.isArrived]))

    dataManager.t = t

    for car in dataManager.cars:
        if dataManager.verbose: print(f"    V{car.car.getId()} : {car.currentStreetIndex}/{len(car.car.getStreets())} [{car.currentStreet.street.street}]")
        if car.isArrived:
            continue
        car.decrementTimeLeft()

    for intersection in dataManager.intersections:
        if intersection.currentTurn != -1:
            street = intersection.getGreenStreet()
            car = street.popWaitingCar()
            if car: car.changeStreet()

        scorerIntersection = ScorerIntersection.getScorerIntersection(scorerIntersections,intersection.intersection)
        for street in intersection.streets:
            ScorerIntersection.getScorerIntersectionStreet(scorerIntersection,street.street).history.append(ScorerIntersectionStreetHistory(street.isLightGreen(),len(street.carsWaitingAtLight),t))
        intersection.decrementTimeLeft()

def scorer(challenge: Challenge, intersections : list[Intersection], verbose: bool = False) -> ScorerResult:
    if verbose: print("== Création des instances ==")
    dataManager = DataManagerSolver(challenge, intersections, verbose = verbose)

    scorerIntersections = []
    for intersection in challenge.getDataManager().getIntersections().values():
        scorerIntersections.append(ScorerIntersection(intersection,[]))
        for street in intersection.getStreets():
            scorerIntersections[-1].streets.append(ScorerIntersectionStreet(street,scorerIntersections,[]))
    
    if dataManager.verbose: print("== Début de la simulation ==")
    for i in range(1, challenge.getDuration() + 1):
        tour(dataManager, i,scorerIntersections)
    if dataManager.verbose:
        print("== Fin de la simulation ==")
        print(f"Le score final est de {dataManager.score}.")
    return ScorerResult(dataManager.score,scorerIntersections)

def exportCSV(scorerResult : ScorerResult) -> list:
    result = [["IntersectionId","StreetName","Time","GreenState","WaitingCars"]]
    for intersection in scorerResult.intersections:
        for street in intersection.streets:
            for data in street.history:
                result.append([intersection.intersection.getId(),street.street.street,data.time,data.greenState,data.waitingCars])
    return result

if __name__ == "__main__":
    challenge = parse_challenge("./challenges/b_ocean.in")
    scorer(challenge)