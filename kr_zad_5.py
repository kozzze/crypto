# Универсальный демонстрационный код El-Gamal
# Меняешь только p и phrase — получаешь готовое решение "как в тетрадь"

# ================== НАСТРОЙКИ ==================
p = 31                 # простое число p > 26
phrase = "Iron Man"    # фраза для шифрования
# ===============================================

# --- Вспомогательные функции ---

def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def factorize(n):
    factors = []
    d = 2
    m = n
    while d * d <= m:
        if m % d == 0:
            factors.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        factors.append(m)
    return factors

def mod_pow(base, exp, mod):
    result = 1
    b = base % mod
    e = exp
    while e > 0:
        if e % 2 == 1:
            result = (result * b) % mod
        b = (b * b) % mod
        e //= 2
    return result

def mod_inv(x, mod):
    # расширенный алгоритм Евклида
    old_r, r = x, mod
    old_s, s_ = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s_ = s_, old_s - q * s_
    return old_s % mod

def find_primitive_root(p):
    # ищем первообразный корень g по модулю p
    phi = p - 1
    factors = factorize(phi)
    for g in range(2, p):
        ok = True
        for q in factors:
            if mod_pow(g, phi // q, p) == 1:
                ok = False
                break
        if ok:
            return g
    return None

# --- Проверка p и построение параметров ---

print("Построение шифра El-Gamal")
print(f"Задан модуль p = {p}")

if not is_prime(p):
    print("Число p не является простым. Алгоритм El-Gamal в таком виде некорректен.")
    exit()

print("p является простым числом.")
print()

g = find_primitive_root(p)
print(f"Находим первообразный корень g по модулю p.")
print(f"Выбираем g = {g}")
print()

# Секретный ключ a (для наглядности фиксируем)
a = 7
if a >= p:
    a = 3  # на случай маленьких p
print(f"Секретный ключ a = {a}")

y = mod_pow(g, a, p)
print(f"Открытый ключ y = g^a mod p = {g}^{a} mod {p} = {y}")
print()

# --- Кодирование фразы ---

print(f"Исходная фраза: \"{phrase}\"")
phrase_up = phrase.upper()

# A=1..Z=26, пробел=0
char_to_num = {' ': 0}
num_to_char = {0: ' '}

for i in range(26):
    ch = chr(ord('A') + i)
    char_to_num[ch] = i + 1
    num_to_char[i + 1] = ch

print("\nСхема кодирования символов:")
print("Пробел -> 0")
print("A -> 1, B -> 2, ..., Z -> 26")
print()

nums = []
print("Преобразование фразы в числа:")
for ch in phrase_up:
    if ch not in char_to_num:
        print(f"Символ '{ch}' не поддерживается (только A-Z и пробел).")
        exit()
    n = char_to_num[ch]
    if n >= p:
        print(f"Ошибка: код символа {n} не меньше p = {p}. Нужно взять большее p.")
        exit()
    nums.append(n)
    print(f"Символ '{ch}' -> {n}")
print()

# --- Выбор одноразового параметра k и шифрование ---

k = 5
print(f"Выбираем одноразовый секретный параметр k = {k}")

c1 = mod_pow(g, k, p)
print(f"c1 = g^k mod p = {g}^{k} mod {p} = {c1}")

yk = mod_pow(y, k, p)
print(f"y^k mod p = {y}^{k} mod {p} = {yk}")
print()

print("Шифрование каждого числового символа m:")
cipher_pairs = []

for i, m in enumerate(nums):
    c2 = (m * yk) % p
    cipher_pairs.append((c1, c2))
    print(f"Символ {i+1}: m = {m}")
    print(f"c2 = m * y^k mod p = {m} * {yk} mod {p} = {c2}")
    print(f"Пара шифртекста: (c1, c2) = ({c1}, {c2})")
    print()

print("Итоговый шифртекст (для каждого символа):")
for i, (c1_i, c2_i) in enumerate(cipher_pairs):
    print(f"Символ {i+1}: (c1, c2) = ({c1_i}, {c2_i})")
print()

# --- Расшифровка ---

print("=== Расшифровка ===")
print("Получаем пары (c1, c2) и восстанавливаем m.")

s = mod_pow(c1, a, p)
print(f"s = c1^a mod p = {c1}^{a} mod {p} = {s}")

s_inv = mod_inv(s, p)
print(f"Обратный элемент s^(-1) по модулю {p}: s^(-1) = {s_inv}")
print()

print("Восстановление каждого m из пары (c1, c2):")
decrypted_nums = []
for i, (c1_i, c2_i) in enumerate(cipher_pairs):
    print(f"Символ {i+1}: (c1, c2) = ({c1_i}, {c2_i})")
    print(f"m = c2 * s^(-1) mod p = {c2_i} * {s_inv} mod {p}")
    m_rec = (c2_i * s_inv) % p
    decrypted_nums.append(m_rec)
    print(f"m = {m_rec}")
    print()

print("Преобразуем числа обратно в символы:")
decrypted_chars = []
for n in decrypted_nums:
    ch = num_to_char[n]
    decrypted_chars.append(ch)
    print(f"{n} -> '{ch}'")

decrypted_phrase = "".join(decrypted_chars)
print()
print(f"Расшифрованная фраза: \"{decrypted_phrase}\"")
