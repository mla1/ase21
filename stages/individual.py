from stageSolver import Stage
import json
from collections import deque

class Planet:
    def __init__(self, id, portals):
        self.id = id
        self.portals = portals

def GetPlanetDict(planetList):
    planets = {}

    for p in planetList:
        id = p["id"]
        planets[id] = Planet(id,p["portals"])
    
    return planets

class Stage01(Stage):
    def __init__(self):
        pass

    def solveTask(self, testcase: dict):
        solutions = []
        planets = GetPlanetDict(testcase["planets"])

        for k, v in planets.items():
            print("id: {}, v: {}".format(k,v))
        
        questions = testcase["questions"]

        for q in questions:
            q["id"]
            q["type"]
            origin = q["originId"]
            dest = q["destinationId"]

            visited = set()

            if origin in planets:
                start = planets[origin]
                
                visited = self.reachable(planets, start, set())
                if dest in visited:
                    solutions.append({"questionId":q["id"], "reachable": True})
                else:
                    solutions.append({"questionId":q["id"], "reachable": False})

        return {'answers': solutions }

    def reachable(self, planets, current: Planet, visited: set):
        if current.id not in visited:
            visited.add(current.id)

            #loop over neighbours
            for portal in current.portals:
                destId = portal["destinationId"]
                neighbour = planets[destId]
                self.reachable(planets,neighbour, visited)
            
            return visited
            

class Stage02(Stage):
    def __init__(self):
        pass

    def solveTask(self, testcase: dict):
        solutions = []
        planets = GetPlanetDict(testcase["planets"])
        questions = testcase["questions"]

        handledPlanets = []
        allreachable = True

        for id, p in planets.items():
            visited = set()
            visited = self.reachable(planets, p, set())

            if len(visited) != len(planets):
                allreachable = False
                break
        
        print("all reachable: {}".format(allreachable))


        for q in questions:
            origin = q["originId"]
            dest = q["destinationId"]
            visited = set()

            if origin in planets:
                start = planets[origin]
                
                visited = self.reachable(planets, start, set())
                if dest in visited:
                    solutions.append({"questionId":q["id"], "reachable": True})
                else:
                    solutions.append({"questionId":q["id"], "reachable": False})

        return {'answers': solutions, "allReachable": allreachable }


    def reachable(self, planets, current: Planet, visited: set):
        print("current: {}, visited: {}".format(current,visited))
        if current.id not in visited:
            visited.add(current.id)

            #loop over neighbours
            for portal in current.portals:
                destId = portal["destinationId"]
                neighbour = planets[destId]
                self.reachable(planets,neighbour, visited)
            
            return visited          


class Stage03(Stage):
    def __init__(self):
        self.__MAXINT = 9223372036854775807

    def solveTask(self, testcase: dict):
        solutions = []
        planets = GetPlanetDict(testcase["planets"])
        questions = testcase["questions"]

        handledPlanets = []
        allreachable = True

        reachablePlanets = {}
        
        # all reachable
        for id, p in planets.items():
            visited = set()
            visited = self.traverse(planets, p, set())
            reachablePlanets[id] = visited

            if len(visited) != len(planets):
                allreachable = False
        
        print("all reachable: {}".format(allreachable))


        # run SPF for all CHEAPEST questions
        shortestPaths = {}

        for q in questions:
            if q["type"] == "REACHABLE":
                if q["destinationId"] in reachablePlanets[q["originId"]]:
                    solutions.append({"questionId":q["id"], "reachable": True})
                else:
                    solutions.append({"questionId":q["id"], "reachable": False})
            elif q["type"] == "CHEAPEST":
                if not q["originId"] in shortestPaths:
                    shortestPaths[q["originId"]] = self.spf(planets,q["originId"], q["destinationId"])
                
                solutions.append(self.constructAnswer(q, shortestPaths[q["originId"]]))

        return {'answers': solutions, "allReachable": allreachable }


    def constructAnswer(self, question, t):
        qid = question["id"]
        origin = question["originId"]
        dest = question["destinationId"]

        (costs, prev) = t
        # costs {0: 0, 1: 42, 2: 84}
        # prev  {0: None, 1: 0, 2: 1}

        # same planet
        if dest == origin:
            return {"questionId": qid, "jumps": [], "costs": 0 }  
        
        # not reachable
        if prev[dest] is None:
            return {"questionId": qid, "jumps": [], "costs": -1 } 

        jumps = []
        cur = dest

        while prev[cur] is not None:
            prevPlanet = prev[cur]["planetId"]
            prevPortal = prev[cur]["portalId"]
            jumps.insert(0, {"originPlanet": prevPlanet, "portal": prevPortal, "destinationPlanet": cur})          
            cur = prevPlanet
            
        return {"questionId": qid, "jumps": jumps, "costs": costs[dest] } 

    def spf(self, planets, origin, destination):
        path = {}
        prev = {}

        queue = deque()

        for id, p in planets.items():
            path[id] = self.__MAXINT
            prev[id] = None
            queue.append(id)
        
        path[origin] = 0

        while queue:
            current = None
            val = self.__MAXINT+1

            for node in queue:
                if path[node] < val:
                    current = node
                    val = path[node]
            
            queue.remove(current)
            print(current)

            #iterate over neighbours of current
            currentPlanet = planets[current]
            for portal in currentPlanet.portals:
                cost = portal["costs"]
                neighbour = portal["destinationId"]
                if neighbour in queue:
                    costToNeighbourOverCurrent = path[current] + cost
                    if costToNeighbourOverCurrent < path[neighbour]:
                        path[neighbour] = costToNeighbourOverCurrent
                        prev[neighbour] = { "planetId": current, "portalId": portal["id"] }
        
        print(path)
        print(prev)
        return (path, prev)


    def traverse(self, planets, current: Planet, visited: set):
        print("current: {}, visited: {}".format(current,visited))
        if current.id not in visited:
            visited.add(current.id)

            #loop over neighbours
            for portal in current.portals:
                destId = portal["destinationId"]
                neighbour = planets[destId]
                self.traverse(planets,neighbour, visited)
            
            return visited


class Stage04(Stage):
    def __init__(self):
        self.__MAXINT = 9223372036854775807

    def solveTask(self, testcase: dict):
        solutions = []
        planets = GetPlanetDict(testcase["planets"])
        questions = testcase["questions"]

        handledPlanets = []
        allreachable = True

        reachablePlanets = {}

        # run SPF for all CHEAPEST questions
        shortestPaths = {}

        # all reachable
        for id, p in planets.items():
            (cost_to, prev) = self.spf(planets, id)
            shortestPaths[id] = (cost_to, prev)

            visited = set()
            for dest, cost in cost_to.items():
                if cost != self.__MAXINT:
                    visited.add(dest)
            reachablePlanets[id] = visited

            if len(visited) != len(planets):
                allreachable = False
        
        print("all reachable: {}".format(allreachable))


        # most expensive shortest path
        mostExpensive = {}

        exp_origin = -1
        exp_dest = -1
        max_cost = -1

        for id, p in planets.items():
            (cost_to, _) = shortestPaths[id]

            print("planet {}: {}".format(id, cost_to))
            for dest, cost in cost_to.items():
                if cost != self.__MAXINT and cost > max_cost:
                    exp_origin = id
                    exp_dest = dest
                    max_cost = cost

        print("most exp path: from {} to {} with cost {}".format(exp_origin, exp_dest, max_cost))
        mostExpensive = self.mostExpensiveAnswer(exp_origin, exp_dest, shortestPaths[exp_origin])
        print (mostExpensive)


        for q in questions:
            if q["type"] == "REACHABLE":
                if q["destinationId"] in reachablePlanets[q["originId"]]:
                    solutions.append({"questionId":q["id"], "reachable": True})
                else:
                    solutions.append({"questionId":q["id"], "reachable": False})
            elif q["type"] == "CHEAPEST":
                if not q["originId"] in shortestPaths:
                    shortestPaths[q["originId"]] = self.spf(planets,q["originId"])
                
                solutions.append(self.constructAnswer(q, shortestPaths[q["originId"]]))

        return {'answers': solutions, "allReachable": allreachable, "mostExpensive": mostExpensive }


    def mostExpensiveAnswer(self, origin, dest, t):
        (costs, prev) = t

        # same planet
        if dest == origin:
            return {"originId": origin, "destinationId": dest, "jumps": [], "costs": 0 }  
        
        jumps = []
        cur = dest

        while prev[cur] is not None:
            prevPlanet = prev[cur]["planetId"]
            prevPortal = prev[cur]["portalId"]
            jumps.insert(0, {"originPlanet": prevPlanet, "portal": prevPortal, "destinationPlanet": cur})          
            cur = prevPlanet
            
        return{"originId": origin, "destinationId": dest, "jumps": jumps, "costs": costs[dest] }   

    def constructAnswer(self, question, t):
        qid = question["id"]
        origin = question["originId"]
        dest = question["destinationId"]

        (costs, prev) = t
        # costs {0: 0, 1: 42, 2: 84}
        # prev  {0: None, 1: 0, 2: 1}

        # same planet
        if dest == origin:
            return {"questionId": qid, "jumps": [], "costs": 0 }  
        
        # not reachable
        if prev[dest] is None:
            return {"questionId": qid, "jumps": [], "costs": -1 } 

        jumps = []
        cur = dest

        while prev[cur] is not None:
            prevPlanet = prev[cur]["planetId"]
            prevPortal = prev[cur]["portalId"]
            jumps.insert(0, {"originPlanet": prevPlanet, "portal": prevPortal, "destinationPlanet": cur})          
            cur = prevPlanet
            
        return {"questionId": qid, "jumps": jumps, "costs": costs[dest] } 

    def spf(self, planets, origin):
        path = {}
        prev = {}

        queue = deque()

        for id, p in planets.items():
            path[id] = self.__MAXINT
            prev[id] = None
            queue.append(id)
        
        path[origin] = 0

        while queue:
            current = None
            val = self.__MAXINT+1

            for node in queue:
                if path[node] < val:
                    current = node
                    val = path[node]
            
            queue.remove(current)

            #iterate over neighbours of current
            currentPlanet = planets[current]
            for portal in currentPlanet.portals:
                cost = portal["costs"]
                neighbour = portal["destinationId"]
                if neighbour in queue:
                    costToNeighbourOverCurrent = path[current] + cost
                    if costToNeighbourOverCurrent < path[neighbour]:
                        path[neighbour] = costToNeighbourOverCurrent
                        prev[neighbour] = { "planetId": current, "portalId": portal["id"] }
        
        return (path, prev)


    def traverse(self, planets, current: Planet, visited: set):
        print("current: {}, visited: {}".format(current,visited))
        if current.id not in visited:
            visited.add(current.id)

            #loop over neighbours
            for portal in current.portals:
                destId = portal["destinationId"]
                neighbour = planets[destId]
                self.traverse(planets,neighbour, visited)
            
            return visited

