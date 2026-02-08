def diophantine(a, b, c):
    print(f"Решаем уравнение: {a}*x + {b}*y = {c}\n")

    # Инициализация
    r1, r2 = a, b
    s1, t1 = 1, 0
    s2, t2 = 0, 1

    steps = []
    while r2 != 0:
        q = r1 // r2
        r = r1 % r2
        s = s1 - q * s2
        t = t1 - q * t2
        steps.append(f"q={q}, r={r}, s={s}, t={t}")
        r1, r2 = r2, r
        s1, t1, s2, t2 = s2, t2, s, t

    d = r1
    s, t = s1, t1
    print("Промежуточные шаги:")
    for st in steps:
        print(st)

    print(f"\nНОД(a,b) = d = {d}, найдено: s={s}, t={t}")
    if c % d != 0:
        print(f"Решений нет, так как {c} не делится на {d}")
        return None

    # Частное решение
    x0 = s * (c // d)
    y0 = t * (c // d)
    print(f"\nЧастное решение: x0={x0}, y0={y0}")

    # Общее решение
    print(f"Общее решение:")
    print(f"x = {x0} + ({b}//{d})*k")
    print(f"y = {y0} - ({a}//{d})*k,   k ∈ Z")

    return x0, y0, d


# Пример
a, b, c =21, 14, 35
diophantine(a, b, c)
