from queue import Queue
from time import time
import Common


def AC_3(n, adj_mat, adj_list, domain):

    # print(adj_mat)
    # print(adj_list)
    # print(domain)

    startTime = time()

    Q = Queue()
    for i in range(n):
        for j in adj_list[i]:
            Q.put((i, j))

    while not Q.empty():
        (x, y) = Q.get()
        (flag, domain) = Common.REVISE(x, y, adj_mat[x][y], domain)

        if not len(domain[x]):
            break

        if flag:
            for i in adj_list[x]:
                if i is not y:
                    Q.put((i, x))

    endTime = time()

    # print(domain)

    satisfied = Common.isConsistent(n, domain)

    print("AC-3:")
    if satisfied:
        print("Output: Consistent")
    else:
        print("Output: Inconsistent")

    print("Time: " + str(endTime - startTime))

    return endTime - startTime, satisfied
