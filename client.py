import sys
import json
import time

"""
Készíts programot, ami leszimulálja az erőforrások lefoglalását és felszabadítását a JSON fájlban megadott topológia, kapacitások és igények alapján!

Script paraméterezése: python3 client.py cs.json

A program kimenete:

    esemény sorszám. <esemény név>: <node1><-><node2> st:<szimuálciós idő> [- <sikeres/sikertelen>]

Pl.:

    igény foglalás: A<->C st:1 – sikeres

    igény foglalás: B<->C st:2 – sikeres

    igény felszabadítás: A<->C st:5

    igény foglalás: D<->C st:6 – sikeres

    igény foglalás: A<->C st:7 – sikertelen

"""

def GetLinkCapacityIndex(argPointA, argPointB): #Returns capacity of linked points
    for i in range(len(links)):
        for j in range(2):
            if(argPointA == links[i]["points"][j]):
                for k in range(2):
                    if(argPointB == links[i]["points"][k]):
                        return i
    return 0        
def GetPossibleRoute(argPointA, argPointB): #returns the route between two points
    for i in possible_circuits:
        if(i[0] == argPointA and i[-1] == argPointB):
            return i
def CanReserve(argRouteList, argDemand): #Checks if there's enough capacity on the route
    for i in range(len(argRouteList)-1):
        if(links[GetLinkCapacityIndex(argRouteList[i],argRouteList[i+1])]["capacity"] < argDemand):
            return False
    return True
def ReserveRoute(argRouteList, argDemand, argTime, argCounter):
    for i in range(len(argRouteList)-1):
        links[GetLinkCapacityIndex(argRouteList[i],argRouteList[i+1])]["capacity"] -= argDemand
    argCounter += 1
    print(str(argCounter)+". igény foglalás: "+argRouteList[0]+"<->"+argRouteList[-1]+" st:"+str(argTime) +" - sikeres")    
    return argCounter
def ReleaseRoute(argRouteList, argDemand, argTime, argCounter):
    for i in range(len(argRouteList)-1):
        links[GetLinkCapacityIndex(argRouteList[i],argRouteList[i+1])]["capacity"] += argDemand
    argCounter += 1
    print(str(argCounter)+". igény felszabadítás: "+argRouteList[0]+"<->"+argRouteList[-1]+" st:"+str(argTime))    
    return argCounter

with open(sys.argv[1], "r") as read_file:
    data = json.load(read_file)
    end_points = data["end-points"]
    switches = data["switches"]
    links = data["links"]
    possible_circuits = data["possible-circuits"]
    simulation = data["simulation"]
EventCounter = 0
for i in range(simulation["duration"]):
    for j in simulation["demands"]:

        if (i == j["start-time"]):
            Route = GetPossibleRoute(j["end-points"][0],j["end-points"][1])
            if(CanReserve(Route,j["demand"])):
                EventCounter = ReserveRoute(Route, j["demand"],i,EventCounter)
            else:
                j["end-time"] = -5 #elérhetetlen a ciklus tekintetében
                EventCounter += 1
                print(str(EventCounter)+". igény foglalás: "+j["end-points"][0]+"<->"+j["end-points"][1]+" st:"+str(i)+" - sikertelen")

        if (i == j["end-time"]):
            E_Route = GetPossibleRoute(j["end-points"][0],j["end-points"][1])
            EventCounter = ReleaseRoute(E_Route, j["demand"], i, EventCounter)




