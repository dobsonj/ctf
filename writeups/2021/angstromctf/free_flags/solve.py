goalsum = 1142
goalprod = 302937
for i in range(1, 1141):
    x = i
    y = goalsum - i
    if x + y == goalsum and x * y == goalprod:
        print('Solved', x, y)
        break
