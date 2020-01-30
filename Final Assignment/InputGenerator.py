from random import randint
from math import ceil


def generate(file, n, e):
    fp = open(file, "w")
    fp.write(str(n) + " " + str(e) + "\n")
    fp.write("\n")

    for i in range(1, n+1, 1):
        w = randint(1, 1000)
        fp.write(str(i) + " " + str(w) + "\n")
    fp.write("\n")

    for i in range(0, e, 1):
        while True:
            x = randint(1, n)
            y = randint(1, n)
            if x != y:
                break
        fp.write(str(x) + " " + str(y) + "\n")


def edit():
    in_file = "InputFiles/bio-celegans.mwvc"
    out_file = "InputFiles/bio-celegans.txt"
    fpI = open(in_file, "r")
    fpO = open(out_file, "w")
    flag = False

    for line in fpI:
        list = line.split()
        if list[0] == 'p':
            fpO.write(str(list[2]) + " " + str(list[3]) + "\n\n")
        else:
            if list[0] == 'e' and not flag:
                fpO.write("\n")
                flag = True
            fpO.write(str(list[1]) + " " + str(list[2]) + "\n")


def main():
    for i in range(0, 5, 1):
        n = randint(50, 1000)
        e = ceil(n + (n * 0.8))
        print(str(n) + " " + str(e))
        file = "InputFiles/input" + str(i) + ".txt"
        generate(file, n, e)

    edit()


if __name__ == main():
    main()
