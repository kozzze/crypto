# ============================================================
# Универсальный LFSR по многочлену, например 1000011 → x^6 + x + 1
# Формат шага:
# (s1,s2,s3,s4,s5,s6) -> (s_new,s1,s2,s3,s4,s5)
# Выходной бит = последний бит (s6)
# ============================================================

# ------------------ ВХОДНЫЕ ДАННЫЕ ------------------
poly = "1000011"          # ТУТ МЕНЯТЬ многочлен, например 1000011
initial_state = [1,0,0,0,0,0]   # начальное состояние (не все нули)
# ----------------------------------------------------

print(f"Многочлен: {poly}")

# Разбор многочлена
bits = [int(b) for b in poly]
degree = len(bits) - 1
print(f"Степень многочлена = {degree}")

# Находим степени, где коэффициент = 1
exponents = []
for i, b in enumerate(bits):
    if b == 1:
        exp = degree - i
        exponents.append(exp)

print("Ненулевые коэффициенты при степенях:", exponents)

# taps — все степени кроме старшей
taps = [e for e in exponents if e != degree]
print("Точки обратной связи (taps):", taps, "\n")

# ------------------ ФУНКЦИЯ ОДНОГО ШАГА ------------------

def lfsr_step(state, taps):
    """
    state = [s1, s2, ..., s6]
    taps = степени, например [1,0]
    feedback = XOR по state[k]
    выходной бит = последний элемент state[-1]
    """
    output = state[-1]

    # feedback = XOR по tap-разрядам
    feedback = 0
    for t in taps:
        feedback ^= state[t]

    # сдвиг
    new_state = [feedback] + state[:-1]

    return output, new_state, feedback


# ------------------ ПЕРВЫЕ 20 ЧЛЕНОВ ------------------

print("Первые 20 шагов LFSR:\n")

state = initial_state[:]
sequence = []

for step in range(1, 21):
    out, new_state, fb = lfsr_step(state, taps)

    print(f"{step}) состояние {state} -> новое {new_state}, "
          f"feedback={fb}, выходной бит={out}")

    sequence.append(out)
    state = new_state

print("\nПервые 20 членов последовательности:")
print(sequence, "\n")

# ------------------ ПОИСК ПЕРИОДА ------------------

print("Поиск периода...")

state = initial_state[:]
seen = {}
step = 0

while True:
    key = tuple(state)
    if key in seen:
        period = step - seen[key]
        print(f"Состояние повторилось: {state}")
        print(f"Период = {period}")
        break
    seen[key] = step
    out, new_state, fb = lfsr_step(state, taps)
    state = new_state
    step += 1
