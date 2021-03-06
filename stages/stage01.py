from stageSolver import Stage

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