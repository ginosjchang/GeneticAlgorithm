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

def partial_mapped_crossover(chromosomes, population_size, crossover_size):
    numTasks = len(chromosomes[0])

    for offset in range(0, crossover_size, 2):
        mapping = []
        for i in range(numTasks):
            mapping.append(-1)

        p1 = random.randint(0, population_size)
        p2 = random.randint(0, population_size)
        c1 = population_size + offset
        c2 = c1 + 1

        rand1 = random.randint(0, numTasks - 2)
        rand2 = random.randint(rand1 + 1, numTasks - 1)

        for i in range(rand1, rand2 + 1):
            c1_gene = chromosomes[p1][i]
            c2_gene = chromosomes[p2][i]

            if c1_gene == c2_gene: continue
            elif mapping[c1_gene] == -1 and mapping[c2_gene] == -1:
                mapping[c1_gene] = c2_gene
                mapping[c2_gene] = c1_gene
            elif mapping[c1_gene] == -1:
                mapping[c1_gene] = mapping[c2_gene]
                mapping[c2_gene] = -1
                mapping[mapping[c1_gene]] = c1_gene
            elif mapping[c2_gene] == -1:
                mapping[mapping[c1_gene]] = c2_gene
                mapping[c2_gene] = mapping[c1_gene]
                mapping[c1_gene] = -1
            else:
                mapping[mapping[c1_gene]] = mapping[c2_gene]
                mapping[mapping[c2_gene]] = mapping[c1_gene]
                mapping[c1_gene] = -1
                mapping[c2_gene] = -1

        for i in range(numTasks):
            if(i>=rand1 and i<=rand2):
                chromosomes[c1][i] =  chromosomes[p2][i]
                chromosomes[c2][i] =  chromosomes[p1][i]
            else:
                if(mapping[chromosomes[p1][i]] >=0):
                    chromosomes[c1][i] = mapping[chromosomes[p1][i]]
                else:
                    chromosomes[c1][i] = chromosomes[p1][i]        
                    
                if(mapping[chromosomes[p2][i]] >=0):
                    chromosomes[c2][i] = mapping[chromosomes[p2][i]]
                else:
                    chromosomes[c2][i] = chromosomes[p2][i]

def invers_mutation(chromosomes, population_size, mutation_size):
    numTasks = len(chromosomes[0])

    for offset in range(mutation_size):
        p = random.randint(0, population_size)
        c = population_size + offset

        rand1 = random.randint(0, numTasks-2)
        rand2 = random.randint(rand1 + 1, numTasks - 1)
        for i in range(numTasks):
            if(i < rand1 or i > rand2):
                chromosomes[c][i] = chromosomes[p][i]
            else:
                index = rand2 - (i - rand1)
                chromosomes[c][i] = chromosomes[p][index]

class GeneticAlgorithm:
    def __init__(self, numTasks, cost, total_size, 
                crossover_func = partial_mapped_crossover, mutation_func = invers_mutation,
                population_rate = 0.7, crossover_rate = 0.2):

        self.total_size = total_size
        self.population_size = int(total_size * population_rate)
        self.crossover_size = int(total_size * crossover_rate)
        if self.crossover_size % 2 == 1:
            self.crossover_size -= 1
        self.mutation_size = self.total_size - self.population_size - self.crossover_size

        self.numTasks = numTasks
        self.cost = cost

        self.crossover = crossover_func
        self.mutation = mutation_func
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
    
    def sort_func(self, e):
        return e[1]

    def count_fitness(self):
        self.fitness.clear()
        for i in range(self.total_size):
            self.fitness.append([i, 1 / self.cost(self.chromosomes[i])])

    def select_next_generation(self):
        self.fitness.sort(reverse = True ,key = self.sort_func)
        
        selected_chromosomes = []

        for i in range(self.population_size):
            selected_chromosomes.append(self.chromosomes[self.fitness[i][0]].copy())
        
        for i in range(self.population_size):
            self.chromosomes[i] = selected_chromosomes[i]

    def get_best(self):
        return self.chromosomes[0]

    def evolution(self, times = 100):
        self.initialize()
        for t in range(times):
            self.crossover(self.chromosomes, self.population_size, self.crossover_size)
            self.mutation(self.chromosomes, self.population_size + self.crossover_size, self.mutation_size)
            self.count_fitness()
            self.select_next_generation()
    
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
    ga.evolution(times = 10)
    #ga.show_chromosomes()

    yourAssignment = ga.get_best()
    print('Assignment:', yourAssignment) # print 出分配結果
    print('Cost:', solver.cost(yourAssignment)) # print 出 cost 是多少