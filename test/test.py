def dist(a, b):
    return abs(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2))

a, b = (1, 1), (3, 3)
print(dist(a, b))