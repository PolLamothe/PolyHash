"""
 Implementation d'un scorer qui donnera le plus de tempss a la rue qui aura le plus de traffic
"""

from polystructure import Challenge, Intersection, Street, Solver
# from polyscorer import DataManagerSolver

class EfficientSolver(Solver):
    def solve(challenge: Challenge)->list[Intersection]:
        listeIntersections:dict[Street, Intersection] = challenge.getDataManager().getIntersections()
        dict_rues:dict[str,int] = {}
        for car in challenge.getDataManager().getCars():
            rues:list[Street] = car.getStreets()
            for rue in rues:
                if rue.street in dict_rues:
                    dict_rues[rue.street]+=1
                else: dict_rues[rue.street] = 1

        # dataManager = DataManagerSolver(challenge, intersections=list(challenge.getDataManager().getIntersections()))
        dict_rues = dict(sorted(dict_rues.items(), key=lambda item: item[1]))

        for intersection in listeIntersections.values():
            if len(intersection.getStreets())==1:
                 intersection.getSchedule()[0][1].time = 1
            else:    
                for i, (street, skdl) in enumerate(intersection.getSchedule()):
                        if street.street in dict_rues:
                            skdl.time = max(1, dict_rues[street.street]//3)
        
        return [ intersection for intersection in listeIntersections.values() ]
        
        ''' Le solver doit retourner une liste d'intersections'''

            # streetSolver = dataManager.getStreetFromName(element)
        
        # recreer les intersections en mettant a jour les schedules de chaque rue en fonction de sa valeur dans le dict_rues
        # dans Intersection.addStreet(), Schedule(valeurTemp)


    