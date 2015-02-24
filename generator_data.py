
import subprocess as sub


def run(filename, arg):

    process = sub.Popen(['java', '-jar', filename, str(arg)], stdout = sub.PIPE)
    (out, err) = process.communicate()
    return out

MAX = 5
MIN = -5
NUM_DATA_POINTS = 1000
INCREMENT = (2*MAX)/NUM_DATA_POINTS

def main():

    x_data = [None] * NUM_DATA_POINTS
    y_data = [None] * NUM_DATA_POINTS

    x = MIN

    for i in range(NUM_DATA_POINTS):
        x_data[i] = x
        y_data[i] = run("Generator1.jar", x)
        x += INCREMENT

    gen1_txt = open("generator1data_3.txt", "wb")

    for i in range(NUM_DATA_POINTS):
        data = str(x_data[i]) + " " + str(y_data[i])
        gen1_txt.write(data)

    gen1_txt.close()

    print "DONE"

if __name__ == '__main__':
    main()