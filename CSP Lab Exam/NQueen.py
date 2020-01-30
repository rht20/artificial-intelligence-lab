import numpy as np
from time import time

fp = open("output.txt", "w")


def print_board(board):
    for i in board:
        fp.write(str(i))
        fp.write("\n")


def initial_assignment(n):
    board = []

    for i in range(0, n):
        board.append([])
        for j in range(0, n):
            board[i].append(0)

    for i in range(0, n):
        row = np.random.randint(0, n)
        board[row][i] = i + 1

    # print(board)

    return board


def check(i, j, board, n):
    # print(i, j)

    # column wise
    for k in range(0, n):
        if k == j:
            continue
        if board[i][k] > 0:
            return False

    # up left diagonal
    k = i - 1
    l = j - 1
    while k >= 0 and l >= 0:
        if board[k][l] > 0:
            return False
        k -= 1
        l -= 1

    # bottom left diagonal
    k = i + 1
    l = j - 1
    while k < n and l >= 0:
        if board[k][l] > 0:
            return False
        k += 1
        l -= 1

    # up right diagonal
    k = i - 1
    l = j + 1
    while k >= 0 and l < n:
        if board[k][l] > 0:
            return False
        k -= 1
        l += 1

    # bottom right diagonal
    k = i + 1
    l = j + 1
    while k < n and l < n:
        if board[k][l] > 0:
            return False
        k += 1
        l += 1

    return True


def caller(board, n):
    for i in range(0, n):
        for j in range(0, n):
            if board[i][j] and (not check(i, j, board, n)):
                return False

    return True


def conflict_count(i, j, board, n):
    cnt = 0

    # column wise
    for k in range(0, n):
        if k == j:
            continue
        if board[i][k]:
            cnt += 1

    # up left diagonal
    k = i - 1
    l = j - 1
    while k >= 0 and l >= 0:
        if board[k][l]:
            cnt += 1
        k -= 1
        l -= 1

    # bottom left diagonal
    k = i + 1
    l = j - 1
    while k < n and l >= 0:
        if board[k][l]:
            cnt += 1
        k += 1
        l -= 1

    # up right diagonal
    k = i - 1
    l = j + 1
    while k >= 0 and l < n:
        if board[k][l]:
            cnt += 1
        k -= 1
        l += 1

    # bottom right diagonal
    k = i + 1
    l = j + 1
    while k < n and l < n:
        if board[k][l]:
            cnt += 1
        k += 1
        l += 1

    return cnt


def select_conflicted_var(board, n):
    list = []

    for j in range(0, n):
        for i in range(0, n):
            if board[i][j] and (not check(i, j, board, n)):
                list.append((board[i][j], i, j))

    id = np.random.randint(0, len(list))
    return list[id]


def select_value(i, j, board, n):
    min_cnt = 1000000000
    pos = (i, j)

    for k in range(0, n):
        if k == i:
            continue
        cnt = conflict_count(k, j, board, n)
        if min_cnt > cnt:
            min_cnt = cnt
            pos = (k, j)

    # print(min_cnt, pos)
    return pos


def Min_Conflict(board, n, max_steps):

    for i in range(0, max_steps):
        if caller(board, n) is True:
            return True, board, i

        var_pos = select_conflicted_var(board, n)
        # print(var_pos)
        value = select_value(var_pos[1], var_pos[2], board, n)
        # print(value)
        board[var_pos[1]][var_pos[2]] = 0
        board[value[0]][value[1]] = var_pos[0]
        # print_board(board)

    return False, board, max_steps


def pre():
    val_n = []

    val_n.append(8)
    val_n.append(10)
    val_n.append(15)
    val_n.append(20)

    # i = 20
    # while i < 41:
    #     val_n.append(i)
    #     i += 10

    return val_n


def main():

    val_n = pre()

    for i in val_n:
        out_str = "n = " + str(i) + "\n"
        fp.write(out_str)

        board = initial_assignment(i)
        fp.write("Initial board:\n")
        print_board(board)

        startTime = time()
        flag, board, steps = Min_Conflict(board, i, 1000000)
        endTime = time()

        fp.write("Final board:\n")
        print_board(board)

        print(caller(board, i))
        fp.write("Total Steps: ")
        fp.write(str(steps))
        fp.write("\n")
        fp.write("Total Time: ")
        fp.write(str(endTime - startTime))
        fp.write("\n")

        if flag:
            fp.write("Solution: OK")
            fp.write("\n")
        else:
            fp.write("Solution: Not OK")
            fp.write("\n")

    fp.close()


if __name__ == main():
    main()
