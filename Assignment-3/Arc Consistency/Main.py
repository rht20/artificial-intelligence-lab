from copy import deepcopy
from math import ceil
import PreProcessor, AC_1, AC_2, AC_3, AC_4, PlotData


def main():

    # variable number of nodes, (50% of nC2[n is number of nodes]) edges, and fixed size domain

    numOfNodeList = []
    timeListAC_1 = []
    timeListAC_2 = []
    timeListAC_3 = []
    timeListAC_4 = []

    for i in range(5, 201, 5):

        timeAC_1 = 0
        timeAC_2 = 0
        timeAC_3 = 0
        timeAC_4 = 0

        for j in range(0, 5):

            # build graph and set domain for each node
            m = ceil(((i * (i-1))//2) * 0.5)
            # print(m)
            (adj_mat, adj_list, domain) = PreProcessor.preProcess(i, m, 100)
            # print(adj_mat)
            # print(adj_list)
            # print(domain)

            print("***************************")
            print("N: " + str(i) + ", " + "Iteration: " + str(j))
            t1, f1 = AC_1.AC_1(i, adj_mat, adj_list, deepcopy(domain))
            t2, f2 = AC_2.AC_2(i, adj_mat, adj_list, deepcopy(domain))
            t3, f3 = AC_3.AC_3(i, adj_mat, adj_list, deepcopy(domain))
            t4, f4 = AC_4.AC_4(i, adj_mat, adj_list, deepcopy(domain))

            if f1 != f2 or f1 != f3 or f1 != f4:
                print("Error :(")
                return

            timeAC_1 += t1
            timeAC_2 += t2
            timeAC_3 += t3
            timeAC_4 += t4

        timeAC_1 /= 5
        timeAC_2 /= 5
        timeAC_3 /= 5
        timeAC_4 /= 5

        numOfNodeList.append(i)
        timeListAC_1.append(timeAC_1)
        timeListAC_2.append(timeAC_2)
        timeListAC_3.append(timeAC_3)
        timeListAC_4.append(timeAC_4)

    # make plot
    PlotData.makePlot(numOfNodeList, timeListAC_1, timeListAC_2, timeListAC_3, timeListAC_4, 1)

    print("\n\n\n***************************")
    print("AC-1:")
    for t in timeListAC_1:
        print(t)
    print("\nAC-2:")
    for t in timeListAC_2:
        print(t)
    print("\nAC-3:")
    for t in timeListAC_3:
        print(t)
    print("\nAC-4:")
    for t in timeListAC_4:
        print(t)

    # # variable size domain, fixed number of nodes and fixed (50% of nC2[n is number of nodes]) number of edges
    #
    # domainSizeList = []
    # timeListAC_1 = []
    # timeListAC_2 = []
    # timeListAC_3 = []
    # timeListAC_4 = []
    #
    # i = 10
    # m = ceil(((100 * (100 - 1)) // 2) * 0.5)
    # # print(m)
    # while i < 201:
    #
    #     timeAC_1 = 0
    #     timeAC_2 = 0
    #     timeAC_3 = 0
    #     timeAC_4 = 0
    #
    #     for j in range(0, 10):
    #         # build graph and set domain for each node
    #         (adj_mat, adj_list, domain) = PreProcessor.preProcess(100, m, i)
    #         # print(adj_mat)
    #         # print(adj_list)
    #         # print(domain)
    #
    #         print("***************************")
    #         print("Domain Size: " + str(i) + ", " + "Iteration: " + str(j))
    #         t1, f1 = AC_1.AC_1(100, adj_mat, adj_list, deepcopy(domain))
    #         t2, f2 = AC_2.AC_2(100, adj_mat, adj_list, deepcopy(domain))
    #         t3, f3 = AC_3.AC_3(100, adj_mat, adj_list, deepcopy(domain))
    #         t4, f4 = AC_4.AC_4(100, adj_mat, adj_list, deepcopy(domain))
    #
    #         if f1 != f2 or f1 != f3 or f1 != f4:
    #             print("Error :(")
    #             return
    #
    #         timeAC_1 += t1
    #         timeAC_2 += t2
    #         timeAC_3 += t3
    #         timeAC_4 += t4
    #
    #     timeAC_1 /= 10
    #     timeAC_2 /= 10
    #     timeAC_3 /= 10
    #     timeAC_4 /= 10
    #
    #     domainSizeList.append(i)
    #     timeListAC_1.append(timeAC_1)
    #     timeListAC_2.append(timeAC_2)
    #     timeListAC_3.append(timeAC_3)
    #     timeListAC_4.append(timeAC_4)
    #
    #     i += 10
    #
    # # make plot
    # PlotData.makePlot(domainSizeList, timeListAC_1, timeListAC_2, timeListAC_3, timeListAC_4, 2)
    #
    # print("\n\n\n***************************")
    # print("AC-1:")
    # for t in timeListAC_1:
    #     print(t)
    # print("\nAC-2:")
    # for t in timeListAC_2:
    #     print(t)
    # print("\nAC-3:")
    # for t in timeListAC_3:
    #     print(t)
    # print("\nAC-4:")
    # for t in timeListAC_4:
    #     print(t)

    # # variable number of edges, fixed number of nodes, and fixed size domain
    #
    # numOfedgeList = []
    # timeListAC_1 = []
    # timeListAC_2 = []
    # timeListAC_3 = []
    # timeListAC_4 = []
    #
    # i = 50
    # while i < 501:
    #
    #     timeAC_1 = 0
    #     timeAC_2 = 0
    #     timeAC_3 = 0
    #     timeAC_4 = 0
    #
    #     for j in range(0, 5):
    #         # build graph and set domain for each node
    #         (adj_mat, adj_list, domain) = PreProcessor.preProcess(30, 50, i)
    #         # print(adj_mat)
    #         # print(adj_list)
    #         # print(domain)
    #
    #         print("Number of Edges: " + str(i) + ", " + "Iteration: " + str(j))
    #         timeAC_1 += AC_1.AC_1(30, adj_mat, adj_list, deepcopy(domain))
    #         timeAC_2 += AC_2.AC_2(30, adj_mat, adj_list, deepcopy(domain))
    #         timeAC_3 += AC_3.AC_3(30, adj_mat, adj_list, deepcopy(domain))
    #         timeAC_4 += AC_4.AC_4(30, adj_mat, adj_list, deepcopy(domain))
    #
    #     timeAC_1 /= 5
    #     timeAC_2 /= 5
    #     timeAC_3 /= 5
    #     timeAC_4 /= 5
    #
    #     numOfedgeList.append(i)
    #     timeListAC_1.append(timeAC_1)
    #     timeListAC_2.append(timeAC_2)
    #     timeListAC_3.append(timeAC_3)
    #     timeListAC_4.append(timeAC_4)
    #
    #     i += 50
    #
    # # make plot
    # PlotData.makePlot(numOfedgeList, timeListAC_1, timeListAC_2, timeListAC_3, timeListAC_4, 3)


if __name__ == main():
    main()
