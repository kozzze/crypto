def legendre_symbol(a, p):
    """Символ Лежандра (a/p) для нечётного простого p."""
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


def solve_quadratic_congruence(a, b, c, m):
    print(f"РЕШЕНИЕ СРАВНЕНИЯ:")
    print(f"  {a} * x^2 + {b} * x + {c} ≡ 0 (mod {m})")

    # 1. Проверка модуля
    print("\n[1] Проверка модуля m")
    if m == 0:
        print("  m = 0 => сравнение по модулю 0 не имеет смысла.")
        print("  Останавливаемся.")
        return
    if m < 0:
        print(f"  m отрицательный => заменяем на |m| = {abs(m)}")
        m = abs(m)
    else:
        print(f"  m положительный, оставляем как есть: m = {m}")

    # 2. Исходные коэффициенты
    print("\n[2] Исходные коэффициенты")
    print(f"  a = {a}")
    print(f"  b = {b}")
    print(f"  c = {c}")

    # 3. Приведение коэффициентов
    print("\n[3] Приведение коэффициентов по модулю m")
    a_mod = a % m
    b_mod = b % m
    c_mod = c % m
    print(f"  a mod {m} = {a_mod}")
    print(f"  b mod {m} = {b_mod}")
    print(f"  c mod {m} = {c_mod}")

    # 4. Проверка квадратичности
    print("\n[4] Проверка наличия квадратичного члена")
    if a_mod == 0:
        print("  a ≡ 0 (mod m) => уравнение линейное:")
        print(f"    {b_mod} * x + {c_mod} ≡ 0 (mod {m})")

        print("\n  Перебор всех x от 0 до m-1:")
        solutions = []
        for x in range(m):
            left = b_mod * x + c_mod
            value = left % m
            print(f"    x = {x:2d}: {b_mod}*{x} + {c_mod} = {left} → {left} mod {m} = {value}")
            if value == 0:
                solutions.append(x)

        print("\n[5] Итог для линейного случая")
        if not solutions:
            print("  Подходящих x нет => решений нет.")
        else:
            print(f"  Найдено решений: {len(solutions)}")
            print(f"  x ≡ {solutions} (mod {m})")
        return
    else:
        print("  a != 0 (mod m) => уравнение действительно квадратичное.")

    # --- ДОБАВЛЕНО: дискриминант и символ Лежандра ---
    print("\n[4.1] Дискриминант и символ Лежандра")
    D = (b_mod * b_mod - 4 * a_mod * c_mod) % m
    print(f"  D = b^2 - 4ac mod {m} = {D}")

    if m % 2 == 1:
        ls = legendre_symbol(D, m)
        print(f"  Символ Лежандра (D / {m}) = {ls}")
        if ls == -1:
            print("  => D не является квадратичным вычетом. Корней может не быть.")
        elif ls == 0:
            print("  => D ≡ 0 (mod m). Корень один (кратный).")
        else:
            print("  => D — квадратичный вычет. Корни должны существовать.")
    else:
        print("  Символ Лежандра не определён (m не нечётное простое).")

    # 5. Перебор всех x
    print("\n[5] Перебор всех x от 0 до m-1 для квадратичного случая")
    solutions = []
    for x in range(m):
        x2 = x * x
        term1 = a_mod * x2
        term2 = b_mod * x
        sum_raw = term1 + term2 + c_mod
        value = sum_raw % m

        print(f"  x = {x:2d}:")
        print(f"    x^2 = {x2}")
        print(f"    a * x^2 = {term1}")
        print(f"    b * x   = {term2}")
        print(f"    a*x^2 + b*x + c = {sum_raw}")
        print(f"    {sum_raw} mod {m} = {value}")
        if value == 0:
            print("    => это значение даёт 0 по модулю => x подходит.")
            solutions.append(x)
        else:
            print("    => не 0 по модулю => x не подходит.")

    # 6. Итог
    print("\n[6] Итог для квадратичного случая")
    if not solutions:
        print("  Ни один x от 0 до m-1 не дал 0 по модулю.")
        print("  => решений нет.")
    else:
        print(f"  Найдено решений: {len(solutions)}")
        print(f"  x ≡ {solutions} (mod {m})")


# Пример вызова
solve_quadratic_congruence(3, -5, 10, 11)
