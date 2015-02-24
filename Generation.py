import Tree
import random
import Node
from copy import deepcopy



class Generation():

    def __init__(self, population_size, max_depth, x_data, y_data):
        self.pop_size = population_size
        self.max_depth = max_depth
        self.reproduction_rate = 0.01
        self.mutation_rate = 0.1
        self.generation = []
        self.operations = ['*', '/', '+', '-', '^']
        self.terminals = ['x','x','x','x','x','x','x','x','x','x', -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        self.fitness_sum = 0
        self.x_data = x_data
        self.y_data = y_data
        self.populate_initial_generation()


    def populate_initial_generation(self):

        for i in range(self.pop_size):
            n = random.randint(0,3)
            node = Node.Node(self.operations[n])
            tree = Tree.Tree(node)
            tree.generate_random_tree(tree.root, 1, self.max_depth)
            self.generation.append(tree)
            tree.find_fitness(self.x_data, self.y_data)
            self.fitness_sum += tree.fitness


        self.generation.sort(key=lambda tree: tree.fitness)
        #for i in range(len(self.generation)):
            #self.generation[i].set_normalized_fitness(self.fitness_sum)


    def create_new_generation(self):
        new_generation = []
        #

        #Reproduction
        for i in range(int(self.pop_size * self.reproduction_rate)):
            new_generation.append(self.generation[i])
            #new_generation_fitness_sum += self.generation[i].fitness

        #Mutation
        for i in range(int(self.pop_size * self.mutation_rate)):
            tree = self.select_tree()
            # node = None
            # while node == None:
            #     node =
            node = tree.choose_random_node(tree.root, 1, self.max_depth)
            #print 'got here'
            tree.mutate(node)
            #print 'successfully mutated'

        #CrossOver
        while len(new_generation) < self.pop_size:
            parent_1 = self.select_tree()
            parent_2 = self.select_tree()

            while parent_1 == parent_2:
                parent_2 = self.select_tree()

            p_1 = deepcopy(parent_1)
            p_2 = deepcopy(parent_2)
            p_1.crossover(p_2)
            p_1.find_fitness(self.x_data, self.y_data)
            p_2.find_fitness(self.x_data, self.y_data)
            #new_generation_fitness_sum += p_1.fitness + p_2.fitness
            new_generation.append(p_1)
            new_generation.append(p_2)

        #for i in range(len(new_generation)):
            #new_generation[i].set_normalized_fitness(new_generation_fitness_sum)

        new_generation.sort(key=lambda tree:tree.fitness)
        self.generation = new_generation
        #self.fitness_sum = new_generation_fitness_sum

    def evolution(self, num_generations):
        for i in range(num_generations):
            self.create_new_generation()

    def select_tree(self):
        return self.selection_helper(self.pop_size/10)

    def selection_helper(self, size):
        best_tree = None
        sample = random.sample(self.generation, size)
        best_score = -1
        for tree in sample:
            if best_score == -1:
                best_score = tree.fitness
                best_tree = tree
            else:
                if tree.fitness < best_score:
                    best_score = tree.fitness
                    best_tree = tree

        return best_tree










