#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import random
import time

KEYS_FILE = "keys.jsonl"

# ==========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("Обратного элемента не существует")
    return x % m

def is_probable_prime(n, k=10):
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False
    # Миллер–Рабин
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=16):
    while True:
        n = random.getrandbits(bits)
        n |= 1
        if is_probable_prime(n):
            return n

def save_key_record(record):
    with open(KEYS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def load_text_from_keyboard():
    print("Введите текст (одна строка):")
    return input()

def load_text_from_file():
    path = input("Введите путь к файлу: ").strip()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_text_to_file(text):
    path = input("Введите путь для сохранения файла: ").strip()
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Результат сохранён в файл: {path}")

def choose_encoding():
    print("Выберите кодировку текста:")
    print("1) utf-8")
    print("2) cp1251")
    while True:
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            return "utf-8"
        if choice == "2":
            return "cp1251"
        print("Неверный выбор, попробуйте ещё раз.")

def encode_text(text, encoding):
    return text.encode(encoding)

def decode_text(b, encoding):
    return b.decode(encoding, errors="replace")

# ==========================
# RSA
# ==========================

def generate_rsa_keys():
    # Учебный вариант: маленькие ключи, НЕ для реальной безопасности
    p = generate_prime(16)
    q = generate_prime(16)
    while q == p:
        q = generate_prime(16)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if phi % e == 0:
        # подстраховка
        e = 3
        while egcd(e, phi)[0] != 1:
            e += 2
    d = modinv(e, phi)
    return {"n": n, "e": e}, {"n": n, "d": d}

def rsa_encrypt_bytes(data, pub):
    n, e = pub["n"], pub["e"]
    # шифруем каждый байт отдельно
    return [pow(b, e, n) for b in data]

def rsa_decrypt_bytes(cipher_list, priv):
    n, d = priv["n"], priv["d"]
    plain_bytes = bytes([pow(c, d, n) for c in cipher_list])
    return plain_bytes

# ==========================
# ElGamal
# ==========================

def find_primitive_root(p):
    # простой поиск примитивного корня (учебный, p маленькое)
    factors = set()
    phi = p - 1
    n = phi
    f = 2
    while f * f <= n:
        if n % f == 0:
            factors.add(f)
            while n % f == 0:
                n //= f
        f += 1
    if n > 1:
        factors.add(n)
    for g in range(2, p - 1):
        ok = True
        for q in factors:
            if pow(g, phi // q, p) == 1:
                ok = False
                break
        if ok:
            return g
    raise ValueError("Не найден примитивный корень")

def generate_elgamal_keys():
    # Учебный вариант: маленькое p
    p = generate_prime(16)
    g = find_primitive_root(p)
    x = random.randrange(2, p - 2)  # приватный
    y = pow(g, x, p)               # публичный
    pub = {"p": p, "g": g, "y": y}
    priv = {"p": p, "g": g, "x": x}
    return pub, priv

def elgamal_encrypt_bytes(data, pub):
    p, g, y = pub["p"], pub["g"], pub["y"]
    cipher = []
    for m in data:
        k = random.randrange(2, p - 2)
        a = pow(g, k, p)
        b = (m * pow(y, k, p)) % p
        cipher.append([a, b])
    return cipher

def elgamal_decrypt_bytes(cipher_list, priv):
    p, x = priv["p"], priv["x"]
    plain = []
    for a, b in cipher_list:
        s = pow(a, x, p)
        s_inv = modinv(s, p)
        m = (b * s_inv) % p
        plain.append(m)
    return bytes(plain)

# ==========================
# ШИФРОВАНИЕ / РАСШИФРОВАНИЕ
# ==========================

def choose_algorithm():
    print("Выберите криптосистему:")
    print("1) RSA")
    print("2) ElGamal")
    while True:
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            return "RSA"
        if choice == "2":
            return "ElGamal"
        print("Неверный выбор, попробуйте ещё раз.")

def choose_input_source():
    print("Источник текста:")
    print("1) Ввод с клавиатуры")
    print("2) Чтение из файла")
    while True:
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            return "keyboard"
        if choice == "2":
            return "file"
        print("Неверный выбор, попробуйте ещё раз.")

def choose_output_target():
    print("Куда выводить результат:")
    print("1) На экран")
    print("2) В файл")
    while True:
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            return "screen"
        if choice == "2":
            return "file"
        print("Неверный выбор, попробуйте ещё раз.")

def encrypt_flow():
    algo = choose_algorithm()
    encoding = choose_encoding()
    src = choose_input_source()
    if src == "keyboard":
        plain_text = load_text_from_keyboard()
    else:
        plain_text = load_text_from_file()

    data = encode_text(plain_text, encoding)

    if algo == "RSA":
        pub, priv = generate_rsa_keys()
        cipher_data = rsa_encrypt_bytes(data, pub)
    else:
        pub, priv = generate_elgamal_keys()
        cipher_data = elgamal_encrypt_bytes(data, pub)

    session_id = f"{algo}_{int(time.time())}_{random.randint(1000,9999)}"
    key_record = {
        "session_id": session_id,
        "algorithm": algo,
        "public_key": pub,
        "private_key": priv,
        "created_at": int(time.time())
    }
    save_key_record(key_record)
    print(f"Ключи сессии сохранены в {KEYS_FILE} под идентификатором: {session_id}")

    cipher_obj = {
        "algorithm": algo,
        "encoding": encoding,
        "session_id": session_id,
        "cipher": cipher_data
    }
    cipher_json = json.dumps(cipher_obj, ensure_ascii=False)

    target = choose_output_target()
    if target == "screen":
        print("Шифртекст (JSON):")
        print(cipher_json)
    else:
        path = input("Введите путь для сохранения шифртекста: ").strip()
        with open(path, "w", encoding="utf-8") as f:
            f.write(cipher_json)
        print(f"Шифртекст сохранён в файл: {path}")

def load_key_by_session_id(session_id):
    if not os.path.exists(KEYS_FILE):
        raise ValueError("Файл с ключами не найден.")
    with open(KEYS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("session_id") == session_id:
                return rec
    raise ValueError("Ключи для указанной сессии не найдены.")

def decrypt_flow():
    print("Источник шифртекста:")
    print("1) Ввод JSON с клавиатуры")
    print("2) Чтение JSON из файла")
    while True:
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            print("Вставьте JSON шифртекста одной строкой:")
            cipher_json = input()
            break
        elif choice == "2":
            path = input("Введите путь к файлу с шифртекстом: ").strip()
            with open(path, "r", encoding="utf-8") as f:
                cipher_json = f.read()
            break
        else:
            print("Неверный выбор, попробуйте ещё раз.")

    cipher_obj = json.loads(cipher_json)
    algo = cipher_obj["algorithm"]
    encoding = cipher_obj["encoding"]
    session_id = cipher_obj["session_id"]
    cipher_data = cipher_obj["cipher"]

    key_record = load_key_by_session_id(session_id)
    if key_record["algorithm"] != algo:
        raise ValueError("Алгоритм в шифртексте и ключах не совпадает.")

    priv = key_record["private_key"]

    if algo == "RSA":
        plain_bytes = rsa_decrypt_bytes(cipher_data, priv)
    else:
        plain_bytes = elgamal_decrypt_bytes(cipher_data, priv)

    plain_text = decode_text(plain_bytes, encoding)

    target = choose_output_target()
    if target == "screen":
        print("Расшифрованный текст:")
        print(plain_text)
    else:
        save_text_to_file(plain_text)

# ==========================
# ГЛАВНОЕ МЕНЮ
# ==========================

def main():
    while True:
        print("\nМеню:")
        print("1) Зашифровать сообщение")
        print("2) Расшифровать сообщение")
        print("3) Выход")
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            encrypt_flow()
        elif choice == "2":
            try:
                decrypt_flow()
            except Exception as e:
                print(f"Ошибка при расшифровании: {e}")
        elif choice == "3":
            print("Выход.")
            break
        else:
            print("Неверный выбор, попробуйте ещё раз.")

if __name__ == "__main__":
    main()
