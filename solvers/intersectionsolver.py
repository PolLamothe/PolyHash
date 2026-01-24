"""
Solveur qui attribut un budget de 10 seconde à une intersections et le divise entre chaque en fonctions de leur fréquentations
"""


from polystructure import Challenge, Solver, Intersection, Schedule, Street


class IntersectionSolver(Solver):

    def solve(self, challenge: Challenge) -> list[Intersection]:
        data = challenge.getDataManager()
        intersections = data.getIntersections()
        allStreets = data.getStreets()

        streets_by_name: dict[str, Street] = {}

        for street in allStreets:
            streets_by_name[street.name] = street

        dict_streets: dict[str, int] = {}
        for car in challenge.getDataManager().getCars():
            streets: list[Street] = car.getStreets()
            for strt in streets:
                if strt.name in dict_streets:
                    dict_streets[strt.name] = dict_streets.get(strt.name, 0) + 1

        dict_intersections: dict[int, dict[str, int]] = {}

        for intersection in intersections.values():
            dict_intersections[intersection.getId()] = {}

            for strt in intersection.getStreets():
                dict_intersections[intersection.getId()][strt.name] = dict_streets.get(strt.name, 0)

        for num_inter, inter in dict_intersections.items():
            total_cars = sum(inter.values())

            allotted_time_inter = 10

            intersection_obj = intersections.get(num_inter)
            if intersection_obj is None:
                continue

            for street, cars in inter.items():
                if total_cars == 0 :
                    allotted_time_street = 1
                else:
                    allotted_time_street = (cars * allotted_time_inter) / total_cars

                street_obj = None
                for s in intersection_obj.getStreets():
                    if s.name == street:
                        street_obj = s
                        break

                if street_obj is not None:
                    intersection_obj.updateSchedule(street_obj, Schedule(round(allotted_time_street)))


        return list(intersections.values())




