def quadratic_residues_app(m):
    print(f"ОПРЕДЕЛЕНИЕ КВАДРАТИЧНЫХ ВЫЧЕТОВ ПО МОДУЛЮ {m}")

    # 1. Проверка корректности модуля
    print("\n1) Проверка модуля")
    if m <= 1:
        print("  Модуль должен быть ≥ 2.")
        return
    print(f"  Модуль корректен: m = {m}")

    # 2. Перебор всех x и вычисление x^2 mod m
    print("\n2) Перебор всех x от 0 до m-1 и вычисление x^2 mod m")
    residues = set()
    steps = []

    for x in range(m):
        x2 = x * x
        r = x2 % m
        steps.append((x, x2, r))
        print(f"  x = {x:2d}: x^2 = {x2:4d} → {x2} mod {m} = {r}")
        residues.add(r)

    # 3. Формирование множества всех возможных значений
    print("\n3) Формирование множеств вычетов и невычетов")
    all_values = set(range(m))
    non_residues = sorted(all_values - residues)
    residues = sorted(residues)

    print(f"  Все значения по модулю m: {list(all_values)}")
    print(f"  Квадратичные вычеты:      {residues}")
    print(f"  Квадратичные невычеты:    {non_residues}")

    # 4. Итог
    print("\n4) Итог")
    print(f"  Количество квадратичных вычетов:   {len(residues)}")
    print(f"  Количество квадратичных невычетов: {len(non_residues)}")

    print("\nГотово.")


quadratic_residues_app(11)
