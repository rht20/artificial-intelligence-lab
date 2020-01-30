from queue import Queue
from time import time
import Common


def AC_2(n, adj_mat, adj_list, domain):

    # print(adj_mat)
    # print(adj_list)
    # print(domain)

    startTime = time()

    Q1 = Queue()
    Q2 = Queue()
    for i in range(n):
        for j in adj_list[i]:
            if j > i:
                break
            Q1.put((i, j))
            Q2.put((j, i))

        while not Q1.empty():
            while not Q1.empty():
                (x, y) = Q1.get()
                (flag, domain) = Common.REVISE(x, y, adj_mat[x][y], domain)

                if flag:
                    for j in adj_list[x]:
                        if j > i:
                            break
                        if j is not y:
                            Q2.put((j, x))

            while not Q2.empty():
                Q1.put(Q2.get())

    endTime = time()

    # print(domain)

    satisfied = Common.isConsistent(n, domain)

    print("AC-2:")
    if satisfied:
        print("Output: Consistent")
    else:
        print("Output: Inconsistent")

    print("Time: " + str(endTime - startTime))

    return endTime - startTime, satisfied
