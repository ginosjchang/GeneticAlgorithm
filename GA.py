import numpy as np
import random
from enum import Enum
import json

class Problem:
    def __init__(self, input):
        self.input = input
        self.numTasks = len(input)
    
    def cost(self, ans):
        totalTime = 0
        for task, agent in enumerate(ans):
            totalTime += self.input[task][agent]
        return totalTime

class GeneticAlgorithm:
    def __init__(self, numTasks, cost, total_size):

        self.total_size = total_size
        self.population_size = int(total_size * 0.7)
        self.crossover_size = int(total_size * 0.2)
        if self.crossover_size % 2 == 1:
            self.crossover_size -= 1
        self.mutation_size = self.total_size - self.population_size - self.crossover_size
        self.numTasks = numTasks
        self.cost = cost
        '''
        print("population_size: ", self.population_size)
        print("crossover_size: ", self.crossover_size)
        print("mutation_size: ", self.mutation_size)
        print("numTasks: ", self.numTasks)
        '''

    def initialize(self):
        self.chromosomes = []
        self.fitness = []
        self.mapping = []
        
        #generate initial population
        for i in range(self.population_size):
            self.chromosomes.append([])
            for j in range(self.numTasks):
                self.chromosomes[i].append(j)
            random.shuffle(self.chromosomes[i])
        
        #generate space to store the result of crossover and mutation
        for i in range(self.population_size, self.total_size):
            self.chromosomes.append([])
            for j in range(self.numTasks):
                self.chromosomes[i].append(-1)

        #self.show_chromosomes()

        for i in range(self.numTasks):
            self.mapping.append(-1)

        self.selected_chromosomes = []

        self.best_chromosome = [0] * self.numTasks

    def crossover(self):
        child_index = [self.population_size, self.population_size + 1]
        for i in range(int(self.crossover_size/2)):
            self.__partial_mapped_crossover(random.randint(0, self.population_size), random.randint(0, self.population_size),
                                            child_index[0], child_index[1])
            child_index[0] += 2
            child_index[1] += 2

    def __partial_mapped_crossover(self, p1, p2, c1, c2):

        for i in range(self.numTasks):
            self.mapping[i] = -1

        rand1 = random.randint(0, self.numTasks - 2)
        rand2 = random.randint(rand1 + 1, self.numTasks - 1)

        for i in range(rand1, rand2 + 1):
            c1_gene = self.chromosomes[p1][i]
            c2_gene = self.chromosomes[p2][i]

            if c1_gene == c2_gene: continue
            elif self.mapping[c1_gene] == -1 and self.mapping[c2_gene] == -1:
                self.mapping[c1_gene] = c2_gene
                self.mapping[c2_gene] = c1_gene
            elif self.mapping[c1_gene] == -1:
                self.mapping[c1_gene] = self.mapping[c2_gene]
                self.mapping[c2_gene] = -1
                self.mapping[self.mapping[c1_gene]] = c1_gene
            elif self.mapping[c2_gene] == -1:
                self.mapping[self.mapping[c1_gene]] = c2_gene
                self.mapping[c2_gene] = self.mapping[c1_gene]
                self.mapping[c1_gene] = -1
            else:
                self.mapping[self.mapping[c1_gene]] = self.mapping[c2_gene]
                self.mapping[self.mapping[c2_gene]] = self.mapping[c1_gene]
                self.mapping[c1_gene] = -1
                self.mapping[c2_gene] = -1

        for i in range(self.numTasks):
            if(i>=rand1 and i<=rand2):
                self.chromosomes[c1][i] =  self.chromosomes[p2][i]
                self.chromosomes[c2][i] =  self.chromosomes[p1][i]
            else:
                if(self.mapping[self.chromosomes[p1][i]] >=0):
                    self.chromosomes[c1][i] = self.mapping[self.chromosomes[p1][i]]
                else:
                    self.chromosomes[c1][i] =self.chromosomes[p1][i]        
                
                if(self.mapping[self.chromosomes[p2][i]] >=0):
                    self.chromosomes[c2][i] = self.mapping[self.chromosomes[p2][i]]
                else:
                    self.chromosomes[c2][i] =self.chromosomes[p2][i]
    
    def mutation(self):
        child_index = self.total_size - self.mutation_size - 1
        for i in range(self.mutation_size):
            parent_index = random.randint(0, self.population_size)
            child_index += 1
            self.invers_mutation(parent_index, child_index)

    def invers_mutation(self, p, c):
        rand1 = random.randint(0, self.numTasks-2)
        rand2 = random.randint(rand1 + 1, self.numTasks - 1)
        for i in range(self.numTasks):
            if(i < rand1 or i > rand2):
                self.chromosomes[c][i] = self.chromosomes[p][i]
            else:
                index = rand2 - (i - rand1)
                self.chromosomes[c][i] = self.chromosomes[p][index]
    
    def sort_func(self, e):
        return e[1]

    def count_fitness(self):
        self.fitness.clear()
        for i, chormosome in enumerate(self.chromosomes):
            self.fitness.append([i, 1 / self.cost(chormosome)])

        self.fitness.sort(reverse = True ,key = self.sort_func)
        
        selected_chromosomes = []

        for i in range(self.population_size):
            selected_chromosomes.append(self.chromosomes[self.fitness[i][0]].copy())
        
        for i in range(self.population_size):
            self.chromosomes[i] = selected_chromosomes[i]
    

    def select(self):
        index = np.argsort(self.finess)[::-1]
    def get_best(self):
        return self.chromosomes[0]
    def show_chromosomes(self):
        print("Population")
        for i in range(self.population_size):
            print(i, self.chromosomes[i])
        print("Crossover")
        for i in range(self.population_size , self.population_size + self.crossover_size):
            print(i, self.chromosomes[i])
        print("Mutation")
        for i in range(self.total_size - self.mutation_size, self.total_size):
            print(i, self.chromosomes[i])

if __name__ == '__main__':
    input = [
    [10, 20, 23, 4],
    [15, 13, 6, 25],
    [ 2, 22, 35, 34],
    [12, 3, 14, 17]
    ]
    
    solver = Problem(input)
    ga = GeneticAlgorithm(solver.numTasks, solver.cost, 50)

    
    ga.initialize()
    for i in range(50):
        ga.crossover()
        ga.mutation()
        ga.count_fitness()
    #ga.show_chromosomes()

    yourAssignment = ga.get_best()
    print('Assignment:', yourAssignment) # print 出分配結果
    print('Cost:', solver.cost(yourAssignment)) # print 出 cost 是多少