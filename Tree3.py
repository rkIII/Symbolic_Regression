"""
Node class to represent an equation tree for use in Symbolic regression.

Author: Rich Korzelius, Caroline Thompson
"""

import random
from Node import Node
from copy import deepcopy

class Tree3():

    def __init__(self, root):
        self.root = root
        self.fitness = None

    def print_expression(self):
        temp = deepcopy(self)
        return temp.print_helper(temp.root)

    def print_helper(self, node):
        operations = ['*', '/', '+', '-', '^']
        if node:
            if type(node) is int:
                return str(node)
            elif node.element not in operations:
                return str(node.element)
            else:
                node.element = '(' + self.print_helper(node.left)+' '+node.element+' '+self.print_helper(node.right)+')'

        if type(node) is int:
            return str(node)
        else:
            return node.element

    def evaluate(self, x1, x2, x3):
        temp = deepcopy(self)
        return temp.evaluate_helper(temp.root, x1, x2, x3)

    def evaluate_helper(self, node, x1, x2, x3):

        operations = ['*', '/', '+', '-', '^']

        if type(node) is int:
            return node
        elif node.element not in operations:
            if node.element == 'x1':
                return x1
            elif node.element == 'x2':
                return x2
            elif node.element == 'x3':
                return x3
            else:
                return node.element
        else:
            if node.left != None and node.right != None:
                if node.element == '*':
                    try:
                        node.element = self.evaluate_helper(node.left, x1, x2, x3) * self.evaluate_helper(node.right, x1, x2, x3)
                        return node.element
                    except AttributeError:
                        return node.element
                    except OverflowError:
                        return 1
                elif node.element == '+':
                    try:
                        node.element = self.evaluate_helper(node.left, x1, x2, x3) + self.evaluate_helper(node.right, x1, x2, x3)
                        return node.element
                    except AttributeError:
                        return node.element
                    except OverflowError:
                        return 1

                elif node.element == '-':
                    try:
                        node.element = self.evaluate_helper(node.left, x1, x2, x3) - self.evaluate_helper(node.right, x1, x2, x3)
                        return node.element
                    except AttributeError:
                        return node.element
                    except OverflowError:
                        return 1
                elif node.element == '^':
                    try:
                        p = int(abs(self.evaluate_helper(node.right, x1, x2, x3)))
                        return self.evaluate_helper(node.left, x1, x2, x3) ** p
                    except OverflowError or AttributeError:
                        return 1

                else:
                    try:
                        left = self.evaluate_helper(node.left, x1, x2, x3)
                        right = self.evaluate_helper(node.right, x1, x2, x3)
                        if right == 0:
                            return 1
                        else:
                           return left/right
                    except AttributeError:
                        return node.element
                    except OverflowError:
                        return 1

            else:
                return node.element


    def find_fitness(self, x1_data, x2_data, x3_data, y_data):
        error = 0

        for i in range(len(x1_data)):
            x1 = x1_data[i]
            x2 = x2_data[i]
            x3 = x3_data[i]

            error += abs(y_data[i] - float(self.evaluate(x1, x2, x3)))

        self.fitness = error


    def mutate(self, node):

        operations = ['*', '/', '+', '-', '^']
        terminals = ['x1','x2','x3','x1','x2','x3','x1','x2','x3', -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        n = random.random()
        if node:
            #print 'node valid'
            #if n < mutation_rate:
            #print 'mutation started'
            if node.element not in terminals:
                #print 'Mutating operation'
                old = node.element
                new = node.element

                while (new == old):
                    new = random.choice(operations)

                if new == '^' and (node.right == 'x1' or node.right == 'x2' or node.right == 'x3' or node.right < 0):
                    while node.right == 'x'or node.right == 'x2' or node.right == 'x3' or node.right < 0:
                        node.right = random.choice(terminals)

                node.element = new
            else:
                #print 'Mutating terminal'
                old = node.element
                new = node.element

                while (new == old):
                    new = random.choice(terminals)

                node.element = new

    def crossover(self, other):
        a = random.randint(1,2)
        b = random.randint(1,2)

        if a == 1:
            temp_self = self.root.left
        else:
            temp_self = self.root.right

        if b == 1:
            temp_other = other.root.left
        else:
            temp_other = other.root.right

        if a == 1:
            self.root.left = temp_other
        else:
            self.root.right = temp_other

        if b == 1:
            other.root.left = temp_self
        else:
            other.root.right = temp_self

    def choose_random_node(self, node, current_depth, max_depth):
        node_choose_rate = 0.5
        n = random.random()

        if node:
            if type(node) is int:
                return
            if n < node_choose_rate:
                #print 'wow'
                #print type(node)
                return node
            elif current_depth == max_depth:
                return node
            else:
                PARSE_DIRECTION = 0.5
                direction = random.random()
                if direction < PARSE_DIRECTION:
                    self.choose_random_node(node.left, current_depth+1, max_depth)
                else:
                    self.choose_random_node(node.right, current_depth + 1, max_depth)

    def generate_random_tree(self, node, depth, maxDepth):
        operators = ['*', '/', '+', '-','^']
        terminals = ['x1','x2','x3','x1','x2','x3','x1','x2','x3', -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]

        if depth == maxDepth:
            l = random.randint(0, 19)
            r = random.randint(0, 19)

            node.left = Node(terminals[l])

            if 0 <= r <= 8 and node.element == '^':
                r = random.randint(9, 19)
                node.right = Node(terminals[r])
            elif r == 15 and node.element == '/':
                while r == 15:
                    r = random.randint(0,19)
                node.right = Node(terminals[r])

            else:
                node.right = Node(terminals[r])

        else:

            #if node.element not in terminals:
            l = random.randint(0, 4)
            r = random.randint(0, 4)

            if terminals[l] == '^' and node.element == '^':
                while l == operators.index('^'):
                    l = random.randint(0,4)

            if terminals[r] == '^' and node.element == '^':
                while r == operators.index('^'):
                    r = random.randint(0, 4)

            node.left = Node(operators[l])
            self.generate_random_tree(node.left, depth + 1, maxDepth)

            node.right = Node(operators[r])
            self.generate_random_tree(node.right, depth + 1, maxDepth)


