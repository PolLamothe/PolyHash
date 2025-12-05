"""

 def __init__(self,id : int,streets : list[Street]):
        self.id = id
        self.streets = streets
        self.schedule : dict[Street,Schedule] = {}
        #schedule par défaut
        for street in streets:
            self.schedule[street] = Schedule()


"""
from polystructure import Intersection
from polyparser import parse_challenge


def export_file(intersections : list[Intersection],challenge : str,outputFile : str) :
    f = open("./solutions/"+challenge+"/"+outputFile+".txt", "w")
    f.write(f"{len(intersections)}\n")

    for intersection in intersections:
        f.write(f"{intersection.getId()}\n")
        f.write(f"{len(intersection.getStreets())}\n")
        sched = intersection.getSchedule()
        for street, schedule in sched:
            f.write(f"{street.street} {schedule.time}\n")

if __name__ == "__main__":
    challenge = parse_challenge("./challenges/b_ocean.in")
    export_file(list(challenge.getDataManager().getIntersections().values()))