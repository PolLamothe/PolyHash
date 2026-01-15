"""Ce solver s'inspire de la solution décrite dans ce repo Github : https://github.com/sagishporer/hashcode-2021-qualification
"""

from polystructure import Challenge, Intersection, Solver, Schedule,Car
import copy
from dataclasses import dataclass
from polyscorer import scorer,ScorerResult,ScorerIntersectionStreetHistory,ScorerIntersection,ScorerIntersectionStreet

@dataclass
class WrappedCar:
    car : Car
    canArrive : bool

@dataclass
class Conflict:
    scorerIntersectionStreet1 : ScorerIntersectionStreet
    scorerIntersectionStreet2 : ScorerIntersectionStreet
    count : int

def addIntoList(conflicts : list[Conflict],newConflict : Conflict) -> list[Conflict]:
    for conflict in conflicts:
        if conflict.scorerIntersectionStreet1 == newConflict.scorerIntersectionStreet1 or conflict.scorerIntersectionStreet1 == newConflict.scorerIntersectionStreet2:
            if conflict.scorerIntersectionStreet2 == newConflict.scorerIntersectionStreet2 or conflict.scorerIntersectionStreet2 == newConflict.scorerIntersectionStreet1:
                conflict.count += 1
                return conflicts
    conflicts.append(newConflict)
    return conflicts

class AdvancedSolver(Solver): 

    def solve(self, challenge: Challenge) -> list[Intersection]:
        cars : list[WrappedCar] = []

        for car in challenge.getDataManager().getCars():
            count = 0
            for street in car.getStreets()[1:]:
                count += street.length
            if count <= challenge.getDuration():
                cars.append(WrappedCar(car,True))
            else:
                cars.append(WrappedCar(car,False))
        
        intersections = challenge.getDataManager().getIntersections()

        usedStreets = []
        startingStreets = []

        for car in cars:
            if not car.canArrive:
                continue
            for index,street in enumerate(car.car.getStreets()[:-1]):
                if index == 0:
                    startingStreets.append(street.name)
                usedStreets.append(street.name)

        for i in intersections.values():
            streets = copy.copy(i.getStreets())
            for s in streets:
                if s.name in usedStreets:
                    i.updateSchedule(s,Schedule(1))
                else:
                    i.updateSchedule(s,Schedule(0))

        for i in intersections.values():
            for index,street in enumerate(i.getStreets()):
                if street.name in startingStreets:
                    i.changeOrder(i.getStreets()[0],street)

        challenge.removeEmptySchedule()
        challenge.removeUnused()

        feedback = scorer(challenge,[intersection for intersection in intersections.values()],False,True)
        print("Score apres l'étape 1 : ",feedback.score)

        #Puisque toutes les schedules ont une durée de 1, nous allons essayer d'échanger certain d'entre eux pour voir si cela fluidifie le traffic

        currentConficts : list[Conflict] = []
        for index,intersection in enumerate(intersections.values()):
            scorerIntersection : ScorerIntersection = ScorerIntersection.getScorerIntersection(feedback.intersections,intersection)
            for instant in range(challenge.getDuration()):
                green = scorerIntersection.getGreeenStreetAtInstant(instant)
                if green.waitingCars > 0:
                    continue
                for street in scorerIntersection.streets:
                    if street == green.scorerIntersectionStreet:
                        continue
                    state = street.getStateAtInstant(instant)
                    if state.waitingCars > 0:
                        addIntoList(currentConficts,Conflict(green.scorerIntersectionStreet,street,1))

        currentConficts.sort(key=lambda x: x.count,reverse=True)
        if len(currentConficts) > 0:
            print("Plus grand conflit : ",currentConficts[0].count)

            for conflict in currentConficts[:int(len(currentConficts)*0.1)]:
                conflict.scorerIntersectionStreet1.scorerIntersections.intersection.changeOrder(conflict.scorerIntersectionStreet1.street,conflict.scorerIntersectionStreet2.street)
            feedback = scorer(challenge,[intersection for intersection in intersections.values()],False,True)
            print("Remplacements effectués, nouveau score : ",feedback.score)
                    
        return [intersection for intersection in intersections.values()]