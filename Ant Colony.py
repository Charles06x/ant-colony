### Imports
import math
from random import randint
from random import random
import matplotlib.pyplot as plt
### End imports

###Functions
def distancesFromCoords():
    f = open('berlin52.tsp')
    data = [line.replace("\n", "").split(" ")[1:] for line in f.readlines()[6:58]]
    coords = list(map(lambda x: [float(x[0]), float(x[1])], data))
    distances = []
    for i in range(len(coords)):
        row = []
        for j in range(len(coords)):
            row.append(math.sqrt((coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2))
        distances.append(row)
    return distances

def convertDistanceMatrix(m):       #Set the distances to 1/distance.
    for i in range(len(m)):
        for j in range(len(m[i])):
            if(m[i][j] != 0):
                m[i][j] = 1/m[i][j]
    return m

def generateInitialCity(m):
    n = randint(0,len(m)-1)
    cities = list(range(0, len(m)))
    cities.remove(n)
    return n, cities

def obtainNextCity(aC, cL, phero, m):
    sum = 0
    for i in range(len(cL)):
        sum += (((phero[aC][cL[i]])**alpha) * ((m[aC][cL[i]])**beta))

    probability = []

    for i in range(len(cL)):
        pr = ((phero[aC][cL[i]])**alpha) * ((m[aC][cL[i]])**beta) / sum
        probability.append(pr)

    n = random()

    acumProbabilities = probability[0]; i = 0
    while acumProbabilities <= n and i < len(cL)-1:
        i+=1
        acumProbabilities += probability[i]
    nCity = cL[i]
    cL.remove(cL[i])
    return nCity, cL

def getTravelCost(l, matrix):
        sum = 0
        for i in range(0, len(l)-1):
            sum += matrix[l[i]][l[i + 1]]
        return sum

def updatePheromonesMatrix(r, p, c):
    for i in range(0, len(r) - 1):
        p[r[i]][r[i+1]] += 1/c
    return p

def evapPheromones(p):
    ro = 0.3
    for i in range(len(p)): 
        for j in range(len(p[i])):
            p[i][j] = (1-ro)*p[i][j]
    return p
###End Functions


pheromones = []; routes = [];  availableCities = []         #Create lists.
alpha = 1; beta = 20; ammountOfAnts = randint(2,6)                #Set the values to constants.
matrix = distancesFromCoords()
localHeuristics = distancesFromCoords()
localHeuristics = convertDistanceMatrix(localHeuristics)     #Set the distances to 1/distance.

print("Ants generated: ", ammountOfAnts)

for i in range(len(localHeuristics)):   #Generate the pheromones matrix.
    aux = [0.0000001]*len(localHeuristics[i])
    pheromones.append(aux)

for i in range(ammountOfAnts):          #Generate ants to start a route
    auxList = []
    auxRoutes, auxCities = generateInitialCity(matrix)
    auxList.append(auxRoutes)
    routes.append(auxList)
    availableCities.append(auxCities)
    
for iterations in range(0,300):
    while len(availableCities[-1]) > 0:
        for i in range(ammountOfAnts):
            if len(availableCities[i]) > 0:
                nextCity, availableCities[i] = obtainNextCity(routes[i][-1], availableCities[i], pheromones, localHeuristics)
                routes[i].append(nextCity)
    lowestCost = getTravelCost(routes[0], matrix)
    bestRoute = routes[0]
    for i in routes:
        if i.count(i[0]) != 2:
            i.append(i[0])
        newCost = (getTravelCost(i, matrix))
        pheromones = updatePheromonesMatrix(i, pheromones, newCost)
        if newCost < lowestCost:
            lowestCost = newCost
            bestRoute = i
    if iterations % 3 == 0:
        pheromones = evapPheromones(pheromones)
            
print(bestRoute)
points = []
for i in bestRoute:
    points.append(i)
#plt.plot(range(len(points)), points, "bo--", markersize=5)
print("\nCosto de mejor ruta: ")
print(lowestCost)
plt.show()