from time import time
import Common


def AC_1(n, adj_mat, adj_list, domain):

    # print(adj_mat)
    # print(adj_list)
    # print(domain)

    startTime = time()

    edges = []
    for i in range(n):
        for j in adj_list[i]:
            edges.append((i, j))
    # print(edges)

    change = True
    while change:
        change = False
        for edge in edges:
            x = edge[0]
            y = edge[1]
            (flag, domain) = Common.REVISE(x, y, adj_mat[x][y], domain)
            change |= flag

    endTime = time()

    # print(domain)

    satisfied = Common.isConsistent(n, domain)

    print("AC-1:")
    if satisfied:
        print("Output: Consistent")
    else:
        print("Output: Inconsistent")

    print("Time: " + str(endTime-startTime))

    return endTime - startTime, satisfied
