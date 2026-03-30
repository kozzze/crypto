# Реализовать проверку многочлена на неприводимость и примитивность.

# ПРОВЕРКА МНОГОЧЛЕНА НА НЕПРИВОДИМОСТЬ И ПРИМИТИВНОСТЬ
# Работаем в поле GF(p) - числа от 0 до p-1, все операции по модулю p

def int_gcd(a, b):
    """НОД для целых чисел (нужен для разложения на множители)"""
    while b:
        a, b = b, a % b
    return abs(a)


# ОПЕРАЦИИ С МНОГОЧЛЕНАМИ В GF(p)

def poly_mod(a, b, p):
    """Остаток от деления многочлена a на b в GF(p)"""
    a = a[:]
    while len(a) >= len(b):
        # Коэффициент частного = старший коэф a / старший коэф b в поле GF(p)
        coef = a[-1] * pow(b[-1], -1, p) % p
        shift = len(a) - len(b)
        # Вычитаем b * coef * x^shift
        for i in range(len(b)):
            a[i + shift] = (a[i + shift] - coef * b[i]) % p
        # Убираем нулевые старшие коэффициенты
        while a and a[-1] == 0:
            a.pop()
    return a


def poly_mul(a, b, p):
    """Умножение многочленов в GF(p)"""
    res = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            res[i + j] = (res[i + j] + a[i] * b[j]) % p
    return res


def poly_pow_mod(base, exp, mod, p):
    """Быстрое возведение многочлена в степень по модулю (бинарный метод)"""
    result = [1]
    while exp > 0:
        if exp & 1:
            result = poly_mod(poly_mul(result, base, p), mod, p)
        base = poly_mod(poly_mul(base, base, p), mod, p)
        exp >>= 1
    return result


def poly_gcd(a, b, p):
    """НОД многочленов в GF(p) через алгоритм Евклида"""
    while b:
        a, b = b, poly_mod(a, b, p)
    return a


# 1. ПРОВЕРКА НЕПРИВОДИМОСТИ
# Многочлен неприводим, если его нельзя разложить на множители
def is_irreducible(f, p):
    n = len(f) - 1  # степень многочлена
    x = [0, 1]  # многочлен x

    power = x
    for k in range(1, n):
        # Вычисляем x^(p^k) mod f
        power = poly_pow_mod(power, p, f, p)
        # Считаем x^(p^k) - x
        diff = []
        for i in range(max(len(power), len(x))):
            val = (power[i] if i < len(power) else 0) - (x[i] if i < len(x) else 0)
            val %= p
            if val:
                while len(diff) <= i:
                    diff.append(0)
                diff[i] = val
        # Если НОД(f, diff) не равен 1, значит есть общий делитель
        if len(poly_gcd(f[:], diff, p)) > 1:
            return False
    return True


# 2. ПРОВЕРКА ПРИМИТИВНОСТИ
# Примитивный многочлен - его корни порождают всё поле GF(p^n)
def prime_factors(n):
    """Разложение числа на простые множители"""
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


def is_primitive(f, p):
    if not is_irreducible(f, p):
        return False

    n = len(f) - 1
    order = p ** n - 1  # порядок мультипликативной группы поля
    factors = prime_factors(order)

    x = [0, 1]

    # Проверяем для каждого простого делителя order
    for q in factors:
        exp = order // q
        # Если x^(order/q) = 1, то порядок x меньше максимального
        if poly_pow_mod(x, exp, f, p) == [1]:
            return False
    return True


# ПРИМЕР
if __name__ == "__main__":
    # x^3 + x + 1 над GF(2)
    f = [0, 1, 1]  # коэффициенты: x^0, x^1, x^2, x^3
    p = 2

    print(f"Многочлен: {f} над GF({p})")
    print(f"Неприводим? {is_irreducible(f, p)}")
    print(f"Примитивен? {is_primitive(f, p)}")