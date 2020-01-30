from math import gcd


def check(constraint, x, y, val_x, val_y):

    if constraint == 1:
        if val_x == val_y:
            return False
        return True

    elif constraint == 2:
        if val_x == val_y:
            return True
        return False

    elif constraint == 3:
        if x < y:
            if val_x < val_y:
                return True
            return False
        else:
            if val_x > val_y:
                return True
            return False

    elif constraint == 4:
        if x < y:
            if val_x > val_y:
                return True
            return False
        else:
            if val_x < val_y:
                return True
            return False

    elif constraint == 5:
        if gcd(val_x, val_y) == 1:
            return True
        return False

    elif constraint == 6:
        if gcd(val_x, val_y) == 1:
            return False
        return True

    elif constraint == 7:
        if not ((val_x + val_y) & 1):
            return True
        return False

    elif constraint == 8:
        if (val_x + val_y) & 1:
            return True
        return False

    return False


def REVISE(x, y, constraint, domain):

    change = False
    remove_list = []

    for dx in domain[x]:
        flag = False
        for dy in domain[y]:
            if check(constraint, x, y, dx, dy):
                flag = True
                break

        if not flag:
            change = True
            remove_list.append(dx)

    list = [i for i in domain[x] if i not in remove_list]
    domain[x] = list

    return change, domain


def isConsistent(n, domain):

    # print(domain)

    for i in range(0, n):
        if not len(domain[i]):
            # print("Inconsistent")
            return False

    # print("Consistent")
    return True
