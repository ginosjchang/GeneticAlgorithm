
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
        

if __name__ == '__main__':
    input = [
    [10, 20, 23, 4],
    [15, 13, 6, 25],
    [ 2, 22, 35, 34],
    [12, 3, 14, 17]
    ]
    
    solver = Problem(input)
    solver.assign(0,[])

    yourAssignment = solver.assignment
    print('Assignment:', yourAssignment) # print 出分配結果
    print('Cost:', solver.cost(yourAssignment)) # print 出 cost 是多少