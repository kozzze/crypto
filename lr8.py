import random
import time
from collections import Counter

# ==========================
# 1. ЛИНЕЙНЫЕ РЕГИСТРЫ СДВИГА (ЛРРС) С ПРИМИТИВНЫМИ МНОГОЧЛЕНАМИ
# ==========================

def lfsr_generator(initial_state, taps):
    """
    ЛРРС над GF(2).
    initial_state: список 0/1, начальное заполнение регистра.
    taps: индексы разрядов, участвующих в обратной связи (по модулю 2).
    Генератор выдаёт биты (0/1).
    """
    state = initial_state[:]
    k = len(state)
    while True:
        out = state[-1]
        feedback = 0
        for t in taps:
            feedback ^= state[t]
        state = [feedback] + state[:-1]
        yield out


def lfsr_10():
    """
    Регистр сдвига с примитивным многочленом 10 степени.
    Пример: x^10 + x^3 + 1.
    """
    k = 10
    initial = [1] * k
    taps = [0, 7]  # x^10 и x^3
    return lfsr_generator(initial, taps)


def lfsr_9():
    """
    Регистр сдвига с примитивным многочленом 9 степени.
    Пример: x^9 + x^4 + 1.
    """
    k = 9
    initial = [1] * k
    taps = [0, 5]  # x^9 и x^4
    return lfsr_generator(initial, taps)


def lfsr_11():
    """
    Регистр сдвига с примитивным многочленом 11 степени.
    Пример: x^11 + x^2 + 1.
    """
    k = 11
    initial = [1] * k
    taps = [0, 9]  # x^11 и x^2
    return lfsr_generator(initial, taps)


# ==========================
# 2. НЕЛИНЕЙНЫЙ УСЛОЖНИТЕЛЬ ДЛЯ 3 АРГУМЕНТОВ
# ==========================

def nonlinear_combiner(a, b, c):
    """
    Нелинейный усложнитель для трёх аргументов.
    Пример булевой функции: f(a,b,c) = ab ⊕ bc ⊕ ca.
    """
    return (a & b) ^ (b & c) ^ (c & a)


def nonlinear_generator():
    """
    Генератор ПСП на основе трёх ЛРРС и нелинейного усложнителя.
    """
    g1 = lfsr_9()
    g2 = lfsr_10()
    g3 = lfsr_11()
    while True:
        a = next(g1)
        b = next(g2)
        c = next(g3)
        yield nonlinear_combiner(a, b, c)


# ==========================
# 3. ВИХРЬ МЕРСЕННА (MERSENNE TWISTER)
# ==========================

def mersenne_generator(seed=None):
    """
    Генератор ПСП на основе вихря Мерсена (MT19937).
    Выдаёт биты (0/1).
    """
    rnd = random.Random(seed)
    while True:
        x = rnd.getrandbits(1)
        yield x


# ==========================
# 4. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================

def bits_to_int(bits):
    v = 0
    for b in bits:
        v = (v << 1) | b
    return v


def generate_sequence(gen, length):
    return [next(gen) for _ in range(length)]


# ==========================
# 5. ТЕСТЫ: ДНИ РОЖДЕНИЯ, ПЕРЕСЕКАЮЩИЕСЯ ПЕРЕСТАНОВКИ, РАНГИ МАТРИЦ
# ==========================

def birthday_test(bits, block_size=16, space_size=2**16):
    """
    Тест Дней Рождения.
    Разбиваем последовательность на блоки по block_size бит,
    интерпретируем как числа в диапазоне [0, space_size),
    считаем количество совпадений (коллизий).
    """
    values = []
    for i in range(0, len(bits) - block_size + 1, block_size):
        block = bits[i:i + block_size]
        v = bits_to_int(block) % space_size
        values.append(v)
    cnt = Counter(values)
    collisions = sum(c - 1 for c in cnt.values() if c > 1)
    return {
        "blocks": len(values),
        "collisions": collisions
    }


def overlapping_permutations_test(bits, t=5):
    """
    Тест пересекающихся перестановок.
    Берём t чисел из [0,1), полученных из блоков бит,
    смотрим частоты перестановок.
    Здесь упрощённый вариант: считаем количество различных перестановок.
    """
    block_size = 16
    floats = []
    for i in range(0, len(bits) - block_size + 1, block_size):
        block = bits[i:i + block_size]
        v = bits_to_int(block) / (2**block_size)
        floats.append(v)

    perms = []
    for i in range(0, len(floats) - t + 1):
        window = floats[i:i + t]
        order = tuple(sorted(range(t), key=lambda j: window[j]))
        perms.append(order)

    cnt = Counter(perms)
    return {
        "windows": len(perms),
        "distinct_perms": len(cnt),
        "max_freq": max(cnt.values()) if cnt else 0
    }


def gf2_rank(matrix):
    """
    Ранг бинарной матрицы над GF(2) методом Гаусса.
    matrix — список списков 0/1.
    """
    m = [row[:] for row in matrix]
    rows = len(m)
    cols = len(m[0]) if rows > 0 else 0
    rank = 0
    col = 0
    for r in range(rows):
        while col < cols and all(m[i][col] == 0 for i in range(r, rows)):
            col += 1
        if col == cols:
            break
        pivot = None
        for i in range(r, rows):
            if m[i][col] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r:
            m[r], m[pivot] = m[pivot], m[r]
        for i in range(rows):
            if i != r and m[i][col] == 1:
                for j in range(col, cols):
                    m[i][j] ^= m[r][j]
        rank += 1
        col += 1
    return rank


def matrix_rank_test(bits, rows=32, cols=32):
    """
    Тест рангов матриц.
    Формируем бинарные матрицы размера rows x cols из последовательности бит,
    считаем распределение рангов.
    """
    block_size = rows * cols
    ranks = []
    for i in range(0, len(bits) - block_size + 1, block_size):
        block = bits[i:i + block_size]
        matrix = []
        for r in range(rows):
            row = block[r * cols:(r + 1) * cols]
            matrix.append(row)
        rnk = gf2_rank(matrix)
        ranks.append(rnk)
    cnt = Counter(ranks)
    return {
        "matrices": len(ranks),
        "rank_distribution": dict(sorted(cnt.items()))
    }


# ==========================
# 6. ЗАПУСК ЭКСПЕРИМЕНТОВ
# ==========================

def run_tests_for_generator(name, gen_factory, lengths=(100, 1000, 10000)):
    results = []
    for L in lengths:
        gen = gen_factory()
        bits = generate_sequence(gen, L)

        t0 = time.time()
        bres = birthday_test(bits)
        t1 = time.time()
        ores = overlapping_permutations_test(bits)
        t2 = time.time()
        mres = matrix_rank_test(bits)
        t3 = time.time()

        results.append({
            "generator": name,
            "length": L,
            "birthday": bres,
            "birthday_time": t1 - t0,
            "perm": ores,
            "perm_time": t2 - t1,
            "rank": mres,
            "rank_time": t3 - t2
        })
    return results


def main():
    generators = [
        ("LFSR_10", lfsr_10),
        ("LFSR_9", lfsr_9),
        ("LFSR_11", lfsr_11),
        ("Nonlinear", nonlinear_generator),
        ("Mersenne", lambda: mersenne_generator(seed=12345)),
    ]

    all_results = []
    for name, factory in generators:
        res = run_tests_for_generator(name, factory)
        all_results.extend(res)

    print("\nИТОГОВАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ:")
    print("Генератор | Длина | Birthday(collisions) | Perm(distinct) | Rank(max_rank,count)")
    for r in all_results:
        gen = r["generator"]
        L = r["length"]
        bc = r["birthday"]["collisions"]
        pd = r["perm"]["distinct_perms"]
        rank_dist = r["rank"]["rank_distribution"]
        max_rank = max(rank_dist.keys()) if rank_dist else 0
        max_rank_count = rank_dist.get(max_rank, 0)
        print(f"{gen:9s} | {L:5d} | {bc:18d} | {pd:13d} | {max_rank:4d}, {max_rank_count:4d}")


if __name__ == "__main__":
    main()
