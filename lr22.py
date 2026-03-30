def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


def solve_square_congruence(a, m):

    print(f"\nРЕШЕНИЕ СРАВНЕНИЯ x^2 ≡ {a} (mod {m})")
    print("=" * 60)

    # Проверка модуля
    print("\n1) Проверка модуля")
    if m <= 1:
        print("  Модуль должен быть ≥ 2.")
        return
    print(f"  Модуль корректен: m = {m}")

    # Приведение a по модулю
    print("\n2) Приведение a по модулю m")
    a_mod = a % m
    print(f"  {a} mod {m} = {a_mod}")

    # Символ Лежандра
    print("\n3) Символ Лежандра")
    if m % 2 == 1:
        ls = legendre_symbol(a_mod, m)
        print(f"  (a / m) = ({a_mod} / {m}) = {ls}")

        if ls == -1:
            print("  => a является квадратичным невычетом. Решений быть не может.")
        elif ls == 0:
            print("  => a ≡ 0 (mod m). Единственное решение: x ≡ 0.")
        else:
            print("  => a является квадратичным вычетом. Решения должны существовать.")
    else:
        print("  Символ Лежандра не определён, так как m не нечётное простое.")

    # Перебор всех x
    print("\n4) Перебор всех x от 0 до m-1")
    solutions = []
    for x in range(m):
        x2 = x * x
        r = x2 % m
        print(f"  x = {x:2d}: x^2 = {x2:3d} => {x2} mod {m} = {r}")
        if r == a_mod:
            print("    => подходит")
            solutions.append(x)
        else:
            print("    => не подходит")

    # Итог
    print("\n5) Итог")
    if not solutions:
        print("  Решений нет.")
    else:
        print(f"  Найдены решения: {solutions}")
        print(f"  То есть x ≡ {solutions} (mod {m})")


# Запуск
a = int(input("Введите число a: "))
m = int(input("Введите модуль m: "))

solve_square_congruence(a, m)
