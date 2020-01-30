import matplotlib.pyplot as plot


def makePlot(xList, timeListAC_1, timeListAC_2, timeListAC_3, timeListAC_4, flag):

    plot.plot(xList, timeListAC_1, marker='o', color='r', label='AC-1')
    plot.plot(xList, timeListAC_2, marker='o', color='g', label='AC-2')
    plot.plot(xList, timeListAC_3, marker='o', color='b', label='AC-3')
    plot.plot(xList, timeListAC_4, marker='o', color='y', label='AC-4')

    plot.legend(loc='upper left')

    if flag == 1:
        plot.xlabel("Number of Nodes")
    elif flag == 2:
        plot.xlabel("Domain Size")
    elif flag == 3:
        plot.xlabel("Number of edges")

    plot.ylabel("Average Run Time")

    plot.title("Comparison between different Arc Consistency Algorithms")

    plot.show()
