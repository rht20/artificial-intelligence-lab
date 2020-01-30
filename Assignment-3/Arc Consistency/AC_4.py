from queue import Queue
from copy import deepcopy
from time import time
import Common


def AC_4(n, adj_mat, adj_list, domain):

    # print(adj_mat)
    # print(adj_list)
    # print(domain)

    S = {}
    for x in range(n):
        for i in domain[x]:
            S[(x, i)] = []

    counter = {}
    for x in range(n):
        for i in domain[x]:
            for y in adj_list[x]:
                counter[(x, i, y)] = 0

    startTime = time()

    Q = Queue()
    satisfied = True
    for x in range(n):
        for y in adj_list[x]:
            domain_x = deepcopy(domain[x])
            for i in domain_x:
                for j in domain[y]:
                    if Common.check(adj_mat[x][y], x, y, i, j):
                        S[(y, j)].append((x, i))
                        counter[(x, i, y)] += 1

                if not counter[(x, i, y)]:
                    Q.put((x, i))
                    if i in domain[x]:
                        domain[x].remove(i)

    while not Q.empty():
        item1 = Q.get()
        for item2 in S[item1]:
            if item2[1] in domain[item2[0]]:
                tup = (item2[0], item2[1], item1[0])
                counter[tup] -= 1
                if not counter[tup]:
                    Q.put(item2)
                    domain[item2[0]].remove(item2[1])

    endTime = time()

    # print(domain)

    satisfied = Common.isConsistent(n, domain)

    print("AC-4:")
    if satisfied:
        print("Output: Consistent")
    else:
        print("Output: Inconsistent")

    print("Time: " + str(endTime - startTime))

    return endTime - startTime, satisfied
