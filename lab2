n, o = input("имя:"), int(input("возрост:"))
for i in range(1, 11):
    print(f"{i}: Меня зовут {n} и мне {o} лет")

h = int(input("от 1 до 9:"))
for i in range(1, 11):
    print(f"{i}: {h} * {i} = {h * i}")

for i in range(0, 101, 3):
    print(i)

n, f = int(input("число, для факториал:")), 1
for i in range(1, n + 1):
    f *= i
print(f)

i = 20
while i != -1:
    print(i)
    i -= 1

n = int(input("введите число, до которого расчитаем числа фибоначи:"))
i = 0
fa = [0, 1, 1]
f = 0
while f < n and f != n:
    if i >= 3:
        f = fa[i-2] + fa[i-1]
        if f > n:
            break
        fa.append(f)
        print(f)
    elif f <= 1:
        f = fa[i]
        print(f)
    i += 1

s = input("строку:")
sn = ""
for i in range(len(s)):
    sn += (s[i] + str(i+1))
print(sn)

s = input("Введите два числа через пробел:")
while True:
    if s in "абвгдеёжзиклмнопрстуфхцчшщъьэюя":
        break
    else:
        s1, s2 = int(s.split()[0]), int(s.split()[1])
        print(s1 + s2)
        s = input("Введите два числа через пробел:")