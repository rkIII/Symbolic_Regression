
#This modules successfully runs, problems with running with 3_variables in symreg3
from Generation import Generation



def get_data(filename):

    x_data = []
    y_data = []

    with open(filename, 'r') as f:
        data = f.readlines()
        for line in data:
            values = line.split(' ')
            x_data.append(float(values[0]))
            y_data.append(float(values[1]))

        return x_data, y_data

def main():
    x, y = get_data('generator1data_3.txt')


    #x= [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
    #y = [-2.0,1.0,6.0,13.0,22.0,33.0,46.0,61.0,78.0,97.0]
    #x^2 - 3


    population_size = 300
    print 'Population size: ' + str(population_size)
    max_depth = 10
    reproduction_rate = 0.01
    mutation_rate = 0.1
    num_generations = 10
    for i in range(10):
        print 'RUNNING TRIAL ' + str(i)
        gen = Generation(population_size, max_depth, x, y)
        gen.evolution(num_generations)
        best_tree = gen.generation.pop(0)
        print 'AFTER 10 GENERATIONS: '
        print best_tree.print_expression()
        print 'error: ' + str(best_tree.fitness)







if __name__ == '__main__':
    main()