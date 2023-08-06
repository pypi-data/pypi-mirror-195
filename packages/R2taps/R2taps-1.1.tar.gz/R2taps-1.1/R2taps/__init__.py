def qwerty ():
    x1, y1, x2, y2 = [int(input()) for i in range(4)]
    if all([0 < value < 9 for value in [x1, y1, x2, y2]]) \
        and not (x1 == x2 and y1 == y2) \
        and x2 - x1 in [-1, 0, 1] \
        and y2 - y1 in [-1, 0, 1]:
        print("YES")
    else:
        print("NO")

def wartunder ():
    s = input()
    a = list(map(int, s.split()))
    if a[0] + a[1] == a[2]:
        print(a[0], '+', a[1], '=', a[2])
    elif a[0] - a[1] == a[2]:
        print(a[0], '-', a[1], '=', a[2])
    elif a[0] / a[1] == a[2]:
        print(a[0], '/', a[1], '=', a[2])
    elif a[0] * a[1] == a[2]:
        print(a[0], '*', a[1], '=', a[2])
    else:
        print('Error')
