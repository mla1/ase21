from stageSolver import Stage
import operator
from itertools import permutations

map = {
    1: [1],
    2: [2,3],
    3: [3,2,5],
    4: [4],
    5: [5,3],
    6: [0,6,9],
    7: [7],
    8: [8],
    9: [0,6,9],
    0: [0,6,9]
}

map_add = {
    1: [7],
    2: [],
    3: [9],
    4: [],
    5: [6,9],
    6: [8],
    7: [],
    8: [],
    9: [8],
    0: [8]
}

map_sub = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [5],
    7: [1],
    8: [0,6,9],
    9: [3,5],
    0: []
}

class Stage01(Stage):
    
    def __init__(self):
        self.test = 1
        self.map = {
            1: [1],
            2: [2,3],
            3: [3,2,5],
            4: [4],
            5: [5,3],
            6: [0,6,9],
            7: [7],
            8: [8],
            9: [0,6,9],
            0: [0,6,9]
        }
    
    def solveTask(self, testcase: dict):
        if not isinstance(testcase, dict):
            raise TypeError('testcase')

        equ = testcase['equation']

        a = int(equ[0])
        b = int(equ[2])

        solutions = []

        if a == b:
            solutions.append("{}={}".format(a,a))
        else:
            candidates = self.map[a]
            if b in candidates:
                solutions.append("{}={}".format(a,a))
                solutions.append("{}={}".format(b,b))
        
        return {'correctedEquations': solutions }

class Stage02(Stage):
    
    def __init__(self):
        pass

    def solveTask(self, testcase: dict):
        if not isinstance(testcase, dict):
            raise TypeError('testcase')

        equ = testcase['equation']

        a = int(equ[0])
        opStr = equ[1]
        op = operator.add if equ[1] == "+" else operator.sub
        b = int(equ[2])
        c = int(equ[4])
      
        solutions = []
        
        if op(a,b) == c:
            solutions.append("{}{}{}={}".format(a,opStr,b,c))
        else:
            for candidate_a in map[a]:
                if op(candidate_a,b)==c:
                    solutions.append("{}{}{}={}".format(candidate_a,opStr,b,c))
            for candidate_b in map[b]:
                if op(a,candidate_b)==c:
                    solutions.append("{}{}{}={}".format(a,opStr,candidate_b,c))
            for candidate_c in map[c]:
                if op(a,b)==candidate_c:
                    solutions.append("{}{}{}={}".format(a,opStr,b,candidate_c))

        return {'correctedEquations': solutions }

class Stage03(Stage):
    
    def __init__(self):
        pass

    def solveTask(self, testcase: dict):
        if not isinstance(testcase, dict):
            raise TypeError('testcase')

        equ = testcase['equation']

        a = int(equ[0])
        opStr = equ[1]
        op = operator.add if equ[1] == "+" else operator.sub
        b = int(equ[2])
        c = int(equ[4])
      
        solutions = []
        
        if op(a,b) == c:
            solutions.append("{}{}{}={}".format(a,opStr,b,c))
        else:
            for candidate_a in map[a]:
                if op(candidate_a,b)==c:
                    solutions.append("{}{}{}={}".format(candidate_a,opStr,b,c))
            for candidate_b in map[b]:
                if op(a,candidate_b)==c:
                    solutions.append("{}{}{}={}".format(a,opStr,candidate_b,c))
            for candidate_c in map[c]:
                if op(a,b)==candidate_c:
                    solutions.append("{}{}{}={}".format(a,opStr,b,candidate_c))


        # additional solutions with moving digit
        # a op b = c
        # sub(a) op add(b) = c    und sub(a) op b = add(c)
        # add(a) op sub(b) = c    und a op sub(b) = add(c)
        # add(a) op b = sub(c)    und a op add(b) = sub(c)

        operators = [a,b,c]

        for perm in permutations(["add", "sub", "ident"]):
            # a:
            if perm[0] == "add":
                candidates_a = map_add[a]
            elif perm[0] == "sub":
                candidates_a = map_sub[a]
            else:
                candidates_a = [a]

            # b:
            if perm[1] == "add":
                candidates_b = map_add[b]
            elif perm[1] == "sub":
                candidates_b = map_sub[b]
            else:
                candidates_b = [b]

            # c:
            if perm[2] == "add":
                candidates_c = map_add[c]
            elif perm[2] == "sub":
                candidates_c = map_sub[c]
            else:
                candidates_c = [c]

            for ai in candidates_a:
                for bi in candidates_b:
                    for ci in candidates_c:
                        if op(ai, bi) == ci:
                            solutions.append("{}{}{}={}".format(ai,opStr,bi,ci))
        
        return {'correctedEquations': solutions }

class Stage04(Stage):
    
    def __init__(self):
        pass

    def solveTask(self, testcase: dict):
        if not isinstance(testcase, dict):
            raise TypeError('testcase')

        equ = testcase['equation']

        a = int(equ[0])
        #opStr = equ[1]
        #op = operator.add if equ[1] == "+" else operator.sub
        b = int(equ[2])
        c = int(equ[4])
      
        solutions = []
        
        for (op, opStr) in [(operator.add, "+"), (operator.sub, "-")]:
            if op(a,b) == c:
                solutions.append("{}{}{}={}".format(a,opStr,b,c))
            else:
                for candidate_a in map[a]:
                    if op(candidate_a,b)==c:
                        solutions.append("{}{}{}={}".format(candidate_a,opStr,b,c))
                for candidate_b in map[b]:
                    if op(a,candidate_b)==c:
                        solutions.append("{}{}{}={}".format(a,opStr,candidate_b,c))
                for candidate_c in map[c]:
                    if op(a,b)==candidate_c:
                        solutions.append("{}{}{}={}".format(a,opStr,b,candidate_c))


        # additional solutions with moving digit
        # a op b = c
        # sub(a) op add(b) = c    und sub(a) op b = add(c)
        # add(a) op sub(b) = c    und a op sub(b) = add(c)
        # add(a) op b = sub(c)    und a op add(b) = sub(c)

        operators = [a,b,c]

        for perm in permutations(["add", "sub", "ident"]):
            # a:
            if perm[0] == "add":
                candidates_a = map_add[a]
            elif perm[0] == "sub":
                candidates_a = map_sub[a]
            else:
                candidates_a = [a]

            # b:
            if perm[1] == "add":
                candidates_b = map_add[b]
            elif perm[1] == "sub":
                candidates_b = map_sub[b]
            else:
                candidates_b = [b]

            # c:
            if perm[2] == "add":
                candidates_c = map_add[c]
            elif perm[2] == "sub":
                candidates_c = map_sub[c]
            else:
                candidates_c = [c]

            for ai in candidates_a:
                for bi in candidates_b:
                    for ci in candidates_c:
                        if ai + bi == ci:
                            solutions.append("{}{}{}={}".format(ai,"+",bi,ci))
                        if ai - bi == ci:
                            solutions.append("{}{}{}={}".format(ai,"-",bi,ci))
        
        return {'correctedEquations': solutions }