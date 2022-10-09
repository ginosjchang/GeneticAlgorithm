# 2022 INTRODUCTION TO ARTIFICIAL INTELLIGENCE HW2 P76114545
import json

class Problem:
    def __init__(self, input):
        self.input = input
        self.numTasks = len(input)
        self.assignment = []
        self.minCost = -1
    
    def cost(self, ans):
        totalTime = 0
        for task, agent in enumerate(ans):
            totalTime += self.input[task][agent]
        return totalTime
    
    def assign(self, num, assignment):
        
        if num == self.numTasks:
            cost = self.cost(assignment)
            if self.minCost == -1 or cost < self.minCost:
                self.assignment = assignment
                self.minCost = cost
            return
        
        assignment.append(-1)

        for i in range(self.numTasks):
            if i not in assignment:
                assignment[num] = i
                self.assign(num + 1, assignment.copy())

def json_read(filename):
    input = []
    with open(filename, 'r') as file:
        data = json.load(file)
        for key in data:
            input.append(data[key].copy())
    return input

if __name__ == '__main__':
    input = json_read('input.json')

    for data in input:
        solver = Problem(data)
        solver.assign(0,[])
        
        yourAssignment = solver.assignment
        print('Assignment:', yourAssignment) # print 出分配結果
        print('Cost:', solver.cost(yourAssignment)) # print 出 cost 是多少    