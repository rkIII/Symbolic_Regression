
#inconsistent
#still ironing out bugs unfortunately
from random import shuffle
from Generation3 import Generation3


def get_data(filename):

    x1_data = []
    x2_data = []
    x3_data = []
    y_data = []

    with open(filename, 'r') as f:
        data = f.readlines()
        for line in data:
            values = line.split(' ')

            x1_data.append(float(values[0]))
            x2_data.append(float(values[1]))
            x3_data.append(float(values[2]))
            y_data.append(float(values[3]))


        return x1_data, x2_data, x3_data, y_data


def main():


    # x1, x2, x3, y = get_data('data.txt')
    # x1_training = x1[0::5]
    # x2_training = x2[0::5]
    # x3_training = x3[0::5]
    # y_training = y[0::5]
    #
    # x1_test = [x for x in x1 if x not in x1_training]
    # x2_test = [x for x in x2 if x not in x2_training]
    # x3_test = [x for x in x1 if x not in x1_training]
    # y_test = [y for y in y if y not in y_training]

    x = [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
    x1 = [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
    shuffle(x)
    x2 = x
    x = [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
    shuffle(x)
    x3 = x
    print x1
    print x2
    print x3
    y = [-2.0,1.0,6.0,13.0,22.0,33.0,46.0,61.0,78.0,97.0]

    population_size = 100
    max_depth = 5
    reproduction_rate = 0.01
    mutation_rate = 0.1
    num_generations = 10
    final_population = []
    for i in range(3):
        print 'RUNNING'
        gen3 = Generation3([], population_size, max_depth, x1, x2, x3, y)
        gen3.evolution(num_generations)
        best_tree = gen3.generation.pop(0)
        print best_tree.print_expression()
        print 'error: ' + str(best_tree.fitness)

    # for i in range(5):
    #     print 'RUNNING TRIAL ' + str(i)
    #     gen3 = Generation3([], population_size, max_depth, x1_training, x2_training, x3_training, y_training)
    #     gen3.evolution(num_generations)
    #     best_tree = gen3.generation.pop(0)
    #     best_tree.append(final_population)
    #     print best_tree.print_expression()
    #     print 'error: ' + str(best_tree.fitness)
    #     print "DONE WITH TRIAL" + str(i)
    #
    # final_gen = Generation3([], population_size, max_depth, x1_test, x2_test, x3_test, y_test)
    # final_gen.evolution(num_generations)
    # tree = final_gen.generation.pop(0)
    # print tree.print_expression()
    # print 'error: ' + str(tree.fitness)
    # print "DONE"








if __name__ == '__main__':
    main()