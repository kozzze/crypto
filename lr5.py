def universal_step_by_step_solver(a, m):
    print(f"=== ПОЛНЫЙ АНАЛИЗ СРАВНЕНИЯ: x² ≡ {a} (mod {m}) ===")

    # ШАГ 1: Классификация модуля
    print(f"\n[Шаг 1: Анализ модуля m = {m}]")
    if m % 2 == 0:
        print(f"  - Модуль четный. Классический символ Лежандра напрямую не применим.")
    else:
        print(f"  - Модуль нечетный.")

    # Проверка на простоту
    d = 2
    is_prime = True if m > 1 else False
    while d * d <= m:
        if m % d == 0:
            is_prime = False
            break
        d += 1
    print(f"  - Число {m} является {'ПРОСТЫМ' if is_prime else 'СОСТАВНЫМ'}.")

    # ШАГ 2: Генерация множества квадратов (Вычетов)
    print(f"\n[Шаг 2: Нахождение множества вычетов Q]")
    print(f"  Используем свойство: x² ≡ (m-x)² (mod m). Проверяем x от 0 до {m // 2}:")

    residues_dict = {}
    for x in range(0, (m // 2) + 1):
        res = (x ** 2) % m
        if res not in residues_dict:
            residues_dict[res] = []
        residues_dict[res].append(x)
        if x < 10:  # Ограничим вывод для больших модулей
            print(f"    {x}² = {x ** 2} ≡ {res} (mod {m})")

    Q = sorted(list(residues_dict.keys()))
    print(f"  Множество всех вычетов Q = {Q}")

    # ШАГ 3: Нахождение невычетов
    print(f"\n[Шаг 3: Нахождение множества невычетов N]")
    all_possible = set(range(0, m))
    N = sorted(list(all_possible - set(Q)))
    print(f"  Числа, которые не могут быть остатками квадратов: N = {N}")

    # ШАГ 4: Решение конкретной задачи
    print(f"\n[Шаг 4: Итоговый вердикт для a = {a}]")
    target = a % m
    if target in residues_dict:
        # Для полноты найдем все корни, включая те, что > m/2
        all_roots = []
        for x in range(m):
            if (x ** 2) % m == target:
                all_roots.append(x)
        print(f"  Число {a} является квадратичным ВЫЧЕТОМ по модулю {m}.")
        print(f"  Сравнение x² ≡ {a} (mod {m}) ИМЕЕТ решения: x ≡ {all_roots}")
    else:
        print(f"  Число {a} является квадратичным НЕВЫЧЕТОМ по модулю {m}.")
        print(f"  Сравнение x² ≡ {a} (mod {m}) НЕ ИМЕЕТ решений.")


universal_step_by_step_solver(5, 11)