#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Хэш-функция на основе схемы Матиса–Мейера–Осеаса (MMO)
поверх блочного шифра AES (ECB, 128 бит).

Разрешено:
- использовать готовую библиотеку блочного шифра (AES из pycryptodome)

Запрещено:
- использовать готовые хэш-функции (hashlib и т.п.)
"""

import os
from typing import Tuple

try:
    from Crypto.Cipher import AES
except ImportError:
    raise SystemExit("Требуется установить pycryptodome: pip install pycryptodome")


# ==========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================

BLOCK_SIZE = 16  # 128 бит


def pkcs7_pad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return data + bytes([pad_len]) * pad_len


def pkcs7_unpad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    if not data or len(data) % block_size != 0:
        raise ValueError("Некорректная длина данных для PKCS#7")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Некорректная длина паддинга")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Некорректный паддинг")
    return data[:-pad_len]


def bytes_xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def to_hex(b: bytes) -> str:
    return b.hex()


def from_hex(s: str) -> bytes:
    return bytes.fromhex(s)


# ==========================
# MMO НА ОСНОВЕ AES-128
# ==========================

def aes_encrypt_block(key: bytes, block: bytes) -> bytes:
    """
    Блочное шифрование AES-128 (ECB) одного блока.
    key: 16 байт
    block: 16 байт
    """
    if len(key) != BLOCK_SIZE or len(block) != BLOCK_SIZE:
        raise ValueError("Ключ и блок должны быть длиной 16 байт")
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(block)


def mmo_hash(message: bytes) -> bytes:
    """
    Хэш-функция по схеме Матиса–Мейера–Осеаса:
    H_0 = 0^n
    H_i = E_{M_i}(H_{i-1}) XOR H_{i-1}

    Здесь:
    - блочный шифр: AES-128
    - размер блока: 128 бит (16 байт)
    - ключ шифра: M_i (i-й блок сообщения)
    - вход шифра: H_{i-1}
    """
    # Паддинг сообщения до кратности 16 байтам
    m_padded = pkcs7_pad(message, BLOCK_SIZE)

    # Разбиение на блоки
    blocks = [m_padded[i:i + BLOCK_SIZE] for i in range(0, len(m_padded), BLOCK_SIZE)]

    # Начальное значение H0 = 0^128
    h = bytes(BLOCK_SIZE)

    for m_i in blocks:
        # E_{M_i}(H_{i-1})
        e = aes_encrypt_block(key=m_i, block=h)
        # H_i = E_{M_i}(H_{i-1}) XOR H_{i-1}
        h = bytes_xor(e, h)

    return h


# ==========================
# ВВОД / ВЫВОД
# ==========================

def load_text_from_keyboard() -> str:
    print("Введите сообщение (одна строка):")
    return input()


def load_text_from_file() -> str:
    path = input("Введите путь к файлу с сообщением: ").strip()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_hash_to_file(hash_hex: str) -> None:
    path = input("Введите путь для сохранения хэша: ").strip()
    with open(path, "w", encoding="utf-8") as f:
        f.write(hash_hex)
    print(f"Хэш сохранён в файл: {path}")


def choose_input_source() -> str:
    print("Источник сообщения:")
    print("1) Ввод с клавиатуры")
    print("2) Чтение из файла")
    while True:
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            return "keyboard"
        if choice == "2":
            return "file"
        print("Неверный выбор, попробуйте ещё раз.")


def choose_output_target() -> str:
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


def choose_encoding() -> str:
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


# ==========================
# ОСНОВНОЙ ПОТОК
# ==========================

def hash_flow() -> None:
    src = choose_input_source()
    encoding = choose_encoding()

    if src == "keyboard":
        text = load_text_from_keyboard()
    else:
        text = load_text_from_file()

    data = text.encode(encoding)

    h = mmo_hash(data)
    h_hex = to_hex(h)

    target = choose_output_target()
    if target == "screen":
        print("Хэш сообщения (MMO-AES-128):")
        print(h_hex)
    else:
        save_hash_to_file(h_hex)


def main() -> None:
    while True:
        print("\nМеню:")
        print("1) Вычислить хэш сообщения (MMO на AES-128)")
        print("2) Выход")
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            try:
                hash_flow()
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "2":
            print("Выход.")
            break
        else:
            print("Неверный выбор, попробуйте ещё раз.")


if __name__ == "__main__":
    main()
