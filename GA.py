# 2022 INTRODUCTION TO ARTIFICIAL INTELLIGENCE HW2 P76114545
import random
import json

class Problem:
    def __init__(self, input):
        self.input = input
        self.numTasks = len(input)
    
    def cost(self, ans):
        totalTime = 0
        if -1 in ans : return -1
        for task, agent in enumerate(ans):
            totalTime += self.input[task][agent]
        return totalTime

class GeneticAlgorithm:
    def __init__(self, numTasks, cost, population_size, crossover_rate, mutation_rate):
        #store input arg
        self.numTasks = numTasks
        self.cost = cost
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

        #determine each size
        self.population_size = population_size
        self.crossover_size = int(self.population_size * crossover_rate)
        if self.crossover_size % 2 == 1:
            self.crossover_size -= 1
        self.mutation_size = int(self.population_size * mutation_rate)
        self.total_size = self.population_size + self.crossover_size + self.mutation_size

        self.chromosomes = []
        self.fitness = []
        self.record =[]

    def initialize(self):
        self.chromosomes.clear()
        
        #Generate initial population
        for i in range(self.population_size):
            self.chromosomes.append([])
            for j in range(self.numTasks):
                self.chromosomes[i].append(j)
            random.shuffle(self.chromosomes[i])
        
        #Generate space to store the result of crossover and mutation
        for i in range(self.population_size, self.total_size):
            self.chromosomes.append([])
            for j in range(self.numTasks):
                self.chromosomes[i].append(-1)

    def _partial_mapped_crossover(self, parent1, parent2, child1, child2):
        rand1 = random.randint(0, self.numTasks - 2)
        rand2 = random.randint(rand1 + 1, self.numTasks - 1)

        mapping = []

        for i in range(self.numTasks):
            mapping.append(-1)

        for i in range(rand1, rand2 + 1):
            gene1 = parent1[i]
            gene2 = parent2[i]

            if gene1 == gene2: continue
            elif mapping[gene1] == -1 and mapping[gene2] == -1:
                mapping[gene1] = gene2
                mapping[gene2] = gene1
            elif mapping[gene1] == -1:
                mapping[gene1] = mapping[gene2]
                mapping[gene2] = -1
                mapping[mapping[gene1]] = gene1
            elif mapping[gene2] == -1:
                mapping[mapping[gene1]] = gene2
                mapping[gene2] = mapping[gene1]
                mapping[gene1] = -1
            else:
                mapping[mapping[gene1]] = mapping[gene2]
                mapping[mapping[gene2]] = mapping[gene1]
                mapping[gene1] = -1
                mapping[gene2] = -1
        
        for i in range(self.numTasks):
            if i >= rand1 and i <= rand2:
                child1[i] =  parent2[i]
                child2[i] =  parent1[i]
            else:
                if(mapping[parent1[i]] >=0): 
                    child1[i] = mapping[parent1[i]]
                else: 
                    child1[i] = parent1[i]        
                if(mapping[parent2[i]] >=0):
                    child2[i] = mapping[parent2[i]]
                else:
                    child2[i] = parent2[i]
        
    def _invers_mutation(self, chromosome):
        rand1 = random.randint(0, self.numTasks - 2)
        rand2 = random.randint(rand1 + 1, self.numTasks - 1)
        
        origin = chromosome.copy()
        for i in range(self.numTasks):
            if i < rand1 or i > rand2:
                chromosome[i] = origin[i]
            else:
                index = rand2 - (i - rand1)
                chromosome[i] = origin[index]
    
    def fitness_func(self, chromosome):
        return 1 / self.cost(chromosome)
    
    def count_fitness(self):
        self.fitness.clear()
        for i in range(self.total_size):
            self.fitness.append([i, self.fitness_func(self.chromosomes[i])])
    
    #Virtual
    def crossover(self):
        pass

    #Virtual
    def mutation(self):
        pass
    
    def sort_func(self, e):
        return e[1]

    def select(self):
        #Sort fitness in decreased.
        self.fitness.sort(reverse = True ,key = self.sort_func)
        
        selected_chromosomes = []

        for i in range(self.population_size):
            selected_chromosomes.append(self.chromosomes[self.fitness[i][0]].copy())

        for i in range(self.population_size):
            self.chromosomes[i] = selected_chromosomes[i]
        
        self.record.append(self.cost(self.chromosomes[0]))

    def evolution(self, times = 100):
        try:
            self.initialize()
            self.count_fitness()
            self.select()

            for t in range(times):
                self.crossover()
                self.mutation()
                self.count_fitness()
                self.select()
        except:
            print("exception")
            return 0
        return self.chromosomes[0]
    
    def show_chromosomes(self):
        print("Population size : ", self.population_size)
        print("Crossover size : ", self.crossover_size)
        print("Mutation size :", self.mutation_size)
        print("Population")
        for i in range(self.population_size):
            print(i, self.chromosomes[i])
        print("Crossover")
        for i in range(self.population_size , self.population_size + self.crossover_size):
            print(i, self.chromosomes[i])
        print("Mutation")
        for i in range(self.total_size - self.mutation_size, self.total_size):
            print(i, self.chromosomes[i])    

class Struct1(GeneticAlgorithm):
    def __init__(self, numTasks, cost, population_size = 50, crossover_rate = 0.2, mutation_rate = 0.1):
        super().__init__(numTasks, cost, population_size, crossover_rate, mutation_rate)

    def crossover(self):
        child = self.population_size
        for i in range(int(self.crossover_size / 2)):
            parent1 = self.chromosomes[random.randint(0, self.population_size - 1)]
            parent2 = self.chromosomes[random.randint(0, self.population_size - 1)]
            self._partial_mapped_crossover(parent1, parent2, self.chromosomes[child], self.chromosomes[child + 1])
            child += 2

    def mutation(self):
        for i in range(self.mutation_size):
            self.chromosomes[self.total_size - 1 - i] = self.chromosomes[random.randint(0, self.population_size + self.crossover_size)]
            self._invers_mutation(self.chromosomes[self.total_size - 1 - i])

class Struct2(GeneticAlgorithm):
    def __init__(self, numTasks, cost, population_size = 50, crossover_rate = 0.2, mutation_rate = 0.1):
        super().__init__(numTasks, cost, population_size, crossover_rate, mutation_rate)

    def crossover(self):
        pop_size = self.population_size - self.crossover_size
        child = pop_size

        for i in range(int(self.crossover_size / 2)):
            parent1 = self.chromosomes[random.randint(0, pop_size - 1)]
            parent2 = self.chromosomes[random.randint(0, pop_size - 1)]
            self._partial_mapped_crossover(parent1, parent2, self.chromosomes[child], self.chromosomes[child + 1])
            child += 2

    def mutation(self):
        for i in range(self.mutation_size):
            rand = random.randint(1, self.crossover_size)
            self._invers_mutation(self.chromosomes[self.population_size - rand])

class Struct3(GeneticAlgorithm):
    def __init__(self, numTasks, cost, population_size = 50, crossover_rate = 0.2, mutation_rate = 0.1):
        super().__init__(numTasks, cost, population_size, crossover_rate, mutation_rate)

    def crossover(self):
        parents_size = int(self.population_size/2)
        parents = self.chromosomes[0:parents_size].copy()
        child = 0
        #print(self.crossover_size)
        for i in range(int(self.crossover_size / 2)):
            parent1 = parents[random.randint(0, parents_size - 1)]
            parent2 = parents[random.randint(0, parents_size - 1)]
            self._partial_mapped_crossover(parent1, parent2, self.chromosomes[child], self.chromosomes[child + 1])
            child += 2

    def mutation(self):
        for i in range(self.mutation_size):
            rand = random.randint(0, self.crossover_size)
            self._invers_mutation(self.chromosomes[self.population_size - rand])

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
        ga1 = Struct1(solver.numTasks, solver.cost)
        yourAssignment = ga1.evolution(times = 10000)
        print('Assignment:', yourAssignment) # print 出分配結果
        print('Cost:', solver.cost(yourAssignment)) # print 出 cost 是多少