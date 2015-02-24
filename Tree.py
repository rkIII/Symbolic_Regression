"""
Node class to represent an equation tree for use in Symbolic regression.

Author: Rich Korzelius, Caroline Thompson
"""

import random
from Node import Node
from copy import deepcopy

class Tree():

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

    def evaluate(self, x):
        temp = deepcopy(self)
        return temp.evaluate_helper(temp.root, x)

    def evaluate_helper(self, node, x):

        operations = ['*', '/', '+', '-', '^']

        if type(node) is int:
            return node

        if node.element not in operations:
            if node.element == 'x':
                return x
            else:
                return node.element
        else:
            left = self.evaluate_helper(node.left, x)
            right = self.evaluate_helper(node.right, x)

            if node.element == '*':
                return left * right
            elif node.element == '+':
                return left + right
            elif node.element == '-':
                return left - right
            elif node.element == '^':
                try:
                    p = int(abs(right))
                    return left ** p
                except OverflowError:
                    return 1
            else:

                if right == 0:
                    return 1
                else:
                   return left/right


        # if node.element in operations:
        #     if node.element == '*':
        #         node.element = self.evaluate_helper(node.left, x) * self.evaluate_helper(node.right, x)
        #         return node.element
        #     elif node.element == '+':
        #         node.element = self.evaluate_helper(node.left, x) + self.evaluate_helper(node.right, x)
        #         return node.element
        #     elif node.element == '-':
        #         node.element = self.evaluate_helper(node.left, x) - self.evaluate_helper(node.right, x)
        #         return node.element
        #     elif node.element == '^':
        #         p = int(abs(self.evaluate_helper(node.right, x)))
        #         node.element = self.evaluate_helper(node.left, x) ** p
        #         return node.element
        #     else:
        #         r = self.evaluate_helper(node.right, x)
        #         if r == 0:
        #             node.element = 1.0
        #         else:
        #             node.element = self.evaluate_helper(node.left, x) / self.evaluate_helper(node.right, x)
        #
        #         return node.element
        # else:
        #     if node.element == 'x':
        #         return x
        #     else:
        #         return node.element


    def find_fitness(self, x_values, y_actual):
        error = 0
        for i in range(len(x_values)):
            x = x_values[i]
            error += abs(y_actual[i] - self.evaluate(x))

        self.error = error


    def mutate(self, node):

        operations = ['*', '/', '+', '-', '^']
        terminals = ['x','x','x','x','x','x','x','x','x','x', -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
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

                if new == '^' and (node.right == 'x' or node.right < 0):
                    while node.right == 'x' or node.right < 0:
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
        terminals = ['x','x','x','x','x','x','x','x','x','x', -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]

        if depth == maxDepth:
            l = random.randint(0, 20)
            r = random.randint(0, 20)

            node.left = Node(terminals[l])

            if 0 <= r <= 9 and node.element == '^':
                r = random.randint(10, 20)
                node.right = Node(terminals[r])
            elif r == 15 and node.element == '/':
                while r == 15:
                    r = random.randint(0,20)
                node.right = Node(terminals[r])

            else:
                node.right = Node(terminals[r])

        else:

            if node.element not in terminals:
                l = random.randint(-10, 20)
                r = random.randint(-10, 20)

                if l == -1 and node.element == '^':
                    while l == -1:
                        l = random.randint(-10, 20)

                if r <= 0 and node.element == '^':
                    while r <= 0:
                        r = random.randint(-10, 20)
                elif r == 15 and node.element == '/':
                    while r == 15:
                        r = random.randint(0,20)

                if l < 0:
                    node.left = Node(operators[l % 5])
                    self.generate_random_tree(node.left, depth + 1, maxDepth)
                else:
                    node.left = Node(terminals[l])
                    self.generate_random_tree(node.left, depth + 1, maxDepth)

                if r < 0:
                    node.right = Node(operators[r % 5])
                    self.generate_random_tree(node.right, depth + 1, maxDepth)
                else:
                    node.right = Node(terminals[r])
                    self.generate_random_tree(node.right, depth + 1, maxDepth)

