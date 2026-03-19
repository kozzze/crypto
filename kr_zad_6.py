# ============================================================
# ЭЦП на эллиптических кривых
# Кривая: y^2 = x^3 + E1*x + E2  над GF(GF)
# ============================================================

# ------------------ ПАРАМЕТРЫ ------------------
GF = 11          # поле GF(11)
E1 = 1           # параметр a
E2 = 2           # параметр b
Gx, Gy = 1, 2    # базовая точка G = (1,2)
d = 3            # закрытый ключ (1 < d < n)
msg = "HELLO"    # сообщение (можно менять)
# ------------------------------------------------

O = None  # точка бесконечности


# ------------------ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ------------------

def mod_inv(x, mod):
    old_r, r = x, mod
    old_s, s_ = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s_ = s_, old_s - q * s_
    return old_s % mod


def point_add(P, Q):
    if P is O:
        return Q
    if Q is O:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 + y2) % GF == 0:
        return O

    if P != Q:
        lam = (y2 - y1) * mod_inv((x2 - x1) % GF, GF) % GF
    else:
        lam = (3 * x1 * x1 + E1) * mod_inv((2 * y1) % GF, GF) % GF

    x3 = (lam * lam - x1 - x2) % GF
    y3 = (lam * (x1 - x3) - y1) % GF
    return (x3, y3)


def scalar_mult(k, P):
    result = O
    addend = P
    while k > 0:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result


def is_on_curve(P):
    if P is O:
        return True
    x, y = P
    return (y*y - (x*x*x + E1*x + E2)) % GF == 0


def point_order(P):
    Q = P
    n = 1
    while True:
        Q = point_add(Q, P)
        n += 1
        if Q is O:
            return n


# ------------------ ОПИСАНИЕ КРИВОЙ ------------------

print("Эллиптическая кривая E(E1,E2) над GF(GF):")
print(f"GF = {GF}")
print(f"Уравнение: y^2 = x^3 + {E1}x + {E2} (mod {GF})\n")

G = (Gx, Gy)
print(f"Проверяем, что точка G = {G} лежит на кривой...")
print("Результат:", "Да" if is_on_curve(G) else "Нет", "\n")

# ------------------ ПОРЯДОК ТОЧКИ G ------------------

n = point_order(G)
print(f"Порядок точки G: n = {n}\n")

if not (1 < d < n):
    print("Ошибка: закрытый ключ d должен удовлетворять 1 < d < n.")
    exit()

# ------------------ ФОРМИРОВАНИЕ КЛЮЧЕЙ ------------------

print("Формирование ключей:")
print(f"Закрытый ключ d = {d}")
Q = scalar_mult(d, G)
print(f"Открытый ключ Q = d * G = {Q}\n")

# ------------------ ХЭШ СООБЩЕНИЯ ------------------

h = sum(ord(c) for c in msg) % n
if h == 0:
    h = 1

print(f"Сообщение: \"{msg}\"")
print(f"Хэш сообщения h = сумма ASCII mod n = {h}\n")

# ------------------ ФОРМИРОВАНИЕ ПОДПИСИ ------------------

print("Формирование подписи:")

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

k = None
for cand in range(1, n):
    if gcd(cand, n) == 1:
        k = cand
        break

print(f"Выбираем k = {k} (взаимно просто с n)")

R = scalar_mult(k, G)
Rx, Ry = R
r = Rx % n

print(f"R = k * G = {R}")
print(f"r = x_R mod n = {Rx} mod {n} = {r}")

k_inv = mod_inv(k, n)
s = (k_inv * (h + d * r)) % n

print(f"k^(-1) mod n = {k_inv}")
print(f"s = k^(-1) * (h + d*r) mod n = {s}\n")

print(f"Подпись: (r, s) = ({r}, {s})\n")

# ------------------ ПРОВЕРКА ПОДПИСИ ------------------

print("Проверка подписи:")

w = mod_inv(s, n)
print(f"w = s^(-1) mod n = {w}")

u1 = (h * w) % n
u2 = (r * w) % n

print(f"u1 = h * w mod n = {u1}")
print(f"u2 = r * w mod n = {u2}")

P1 = scalar_mult(u1, G)
P2 = scalar_mult(u2, Q)

print(f"u1 * G = {P1}")
print(f"u2 * Q = {P2}")

X = point_add(P1, P2)
print(f"X = u1*G + u2*Q = {X}")

if X is O:
    print("X = точка бесконечности → подпись недействительна")
else:
    v = X[0] % n
    print(f"v = x_X mod n = {v}")
    print("Подпись корректна" if v == r else "Подпись неверна")
