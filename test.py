
def tt():
    a = 2
    b = 3
    return a,b


def tt22(*args):
    print(type(*args))
    # for i in args:
    print(args[0][0])
    # print(*args[0])
    # print(type(*args[1]))

if __name__ == '__main__':

    c = tt()
    tt22(c)
