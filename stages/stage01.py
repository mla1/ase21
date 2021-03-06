from stageSolver import Stage

class Stage01(Stage):
    
    def __init__(self):
        self.test = 1
        self.map = {
            1: [1],
            2: [2,3],
            3: [3,2],
            4: [4],
            5: [5],
            6: [0,6,9],
            7: [7],
            8: [8],
            9: [0,6,9],
            0: [0,6,9]
        }

        print(self.map)
    
    def solveTask(self, testcase):
        equ = testcase['equation']

        solutions = []
        while True:
            line = input("->")
            if line == "done":
                break
            else:
                solutions.append(line)
        
        return {'correctedEquations': solutions }