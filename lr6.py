# Задача 1. Заштфровать открытый текст,
# используя алфавит, используется кривая E751(-1, 1) и генерирующая точка G=(0,1)
# Вариант - 6
# Открытый текст - терновик
# Открытый ключ (188, 93)
# Значения случайныйх чисел k для букв открытого текста = {8 14 17 17 2 10 8 2 2}

from math import sqrt

alpha = (
    " !\"#$%&'()*+,-./"
    + "0123456789"
    + ":;<=>?@"
    + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    + "[\\]^_`"
    + "abcdefghijklmnopqrstuvwxyz"
    + "{|}~"
    + "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    + "абвгдежзийклмнопрстуфхцчшщъыьэюя"
)

p = 751
E = (-1, 1)


def search_euler_points(start, E):
    points = []

    for x in range(start, p):
        w = (x**3 + E[0] * x + E[1]) % p

        # Проверка через критерий Эйлера: является ли w квадратом
        if pow(w, (p - 1) // 2, p) == 1:
            y = pow(w, (p + 1) // 4, p)

            points.append((x, y))
            if y != 0:
                points.append((x, p - y))

        elif w == 0:
            points.append((x, 0))

    return points


points = search_euler_points(33, E)

sorted_points = sorted([p for p in points if p is not None])

map = {}
a = 0
for i in range(len(sorted_points)):
    if a >= len(alpha):
        break

    if i + 1 > 95 and sorted_points[i][0] < 189:
        continue

    print(a + 1, ")", alpha[a], sorted_points[i])
    map[alpha[a]] = sorted_points[i]
    a += 1


def sum_point(first_point, second_point):
    if first_point[0] == second_point[0]:
        numerator = 3 * first_point[0] ** 2 + E[0]
        if numerator < 0:
            numerator += p
        denominator = 2 * first_point[1]
        if denominator < 0:
            denominator += p
        denominator = (denominator ** (p - 2)) % p
        lamb = (numerator * denominator) % p
    else:
        numerator = second_point[1] - first_point[1]
        if numerator < 0:
            numerator += p
        denominator = second_point[0] - first_point[0]
        if denominator < 0:
            denominator += p
        denominator = (denominator ** (p - 2)) % p

        lamb = (numerator * denominator) % p

        # print(numerator, "*", denominator, "=", lamb)
    # print(lamb)
    new_x = (lamb**2 - first_point[0] - second_point[0]) % p
    if new_x < 0:
        new_x += p

    new_y = (lamb * (first_point[0] - new_x) - first_point[1]) % p
    if new_y < 0:
        new_y += p
    # print(new_x, new_y)
    return (new_x, new_y)


def mult_number_on_point(number, point):
    start_point = point
    for _ in range(number - 1):
        start_point = sum_point(start_point, point)

    return start_point


sum_point((66, 552), mult_number_on_point(3, (406, 397)))

G = (0, 1)

text = "терновник"
k = [8, 14, 17, 17, 2, 16, 10, 8, 2]

B = (188, 93)


def encoder(text, map, k, B, G):
    cipher = []

    for i in range(len(text)):
        character = text[i]
        point = map[character]

        G_i = mult_number_on_point(k[i], G)

        P = sum_point(point, mult_number_on_point(k[i], B))

        cipher.append((G_i, P))

    return cipher


cipher = encoder(text, map, k, B, G)
print("Шифровка", cipher)

for n in range(p):
    Q = mult_number_on_point(n, G)
    if Q[0] == B[0] and Q[1] == B[1]:
        print("n =", n)
        break

# print(mult_number_on_point(45, (56, 419)))

# Задача 2. Дан шифртекст.
# Используя алфавит(Еспользуется кпривая Е751(-1,1) и генерирующая точка G = (-1, 1))
# И зная секретный ключ n, найти открытый текст


def minus_points(first_point, second_point):
    second_point = (second_point[0], p - second_point[1])
    return sum_point(first_point, second_point)


# print(minus_points((301, 734), mult_number_on_point(45, (56, 419))))
def decoder(cipher, map, n):
    text = ""

    for item in cipher:
        point = minus_points(item[1], mult_number_on_point(n, item[0]))

        character = next((k for k, v in map.items() if v == point), None)
        text += str(character)

    return text


detext = decoder(cipher, map, 2)
print(detext)

cipher = [
    ((377, 456), (367, 360)),
    ((425, 663), (715, 398)),
    ((188, 93), (279, 353)),
    ((179, 275), (128, 79)),
    ((568, 355), (515, 67)),
    ((568, 355), (482, 230)),
    ((377, 456), (206, 645)),
    ((188, 93), (300, 455)),
    ((489, 468), (362, 446)),
    ((16, 416), (69, 510)),
    ((425, 663), (218, 601)),
]

detext = decoder(cipher, map, 44)
print(detext)
