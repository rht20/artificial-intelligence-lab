import numpy as np


def graphGenerator(n, m):

    adj_mat = []
    for i in range(n):
        adj_mat.append([])
        for j in range(n):
            adj_mat[i].append(0)
    # print(adj_mat)

    adj_list = []
    for i in range(n):
        adj_list.append([])

    while m:
        x = np.random.randint(0, n)
        y = np.random.randint(0, n)
        z = np.random.randint(1, 9)
        if (x is y) or adj_mat[x][y]:
            continue
        adj_mat[x][y] = adj_mat[y][x] = z
        adj_list[x].append(y)
        adj_list[y].append(x)
        m -= 1

    for i in range(n):
        adj_list[i].sort()

    # print(adj_mat)
    # print(adj_list)

    return adj_mat, adj_list


def setDomain(n, limit):

    domain = []
    for i in range(0, n):
        domain.append(set())
        while len(domain[i]) < limit:
            x = np.random.randint(1, 1000)
            domain[i].add(x)
    # print(domain)

    return domain


def preProcess(n, m, limit):

    adj_mat, adj_list = graphGenerator(n, m)
    domain = setDomain(n, limit)

    return adj_mat, adj_list, domain
