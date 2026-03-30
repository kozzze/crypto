import os
import json
from pathlib import Path
from enum import Enum

from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives import padding as sym_padding

from gostcrypto import gostcipher


class CipherType(Enum):
    DES = "DES"
    MAGMA = "MAGMA"


class Encoding(Enum):
    UTF8 = "utf-8"
    CP1251 = "cp1251"


BLOCK_SIZE = 8  # 64 бит для обоих шифров
KEY_SIZE_DES = 8  # 64 бит
KEY_SIZE_MAGMA = 32  # 256 бит


def generate_key(cipher_type: CipherType) -> bytes:
    """Генерирует случайный ключ для указанного шифра."""
    size = KEY_SIZE_DES if cipher_type == CipherType.DES else KEY_SIZE_MAGMA
    key = os.urandom(size)
    print(f"Сгенерирован ключ {cipher_type.value} ({size * 8} бит): {key.hex()}")
    return key


def save_key(key: bytes, cipher_type: CipherType, keys_file: str = "keys.json"):
    """Сохраняет ключ в файл с ключами."""
    path = Path(keys_file)
    if path.exists():
        with open(path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append({"cipher": cipher_type.value, "key_hex": key.hex()})

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Ключ сохранён в {keys_file} (запись #{len(data)})")
    return len(data) - 1


def load_keys(keys_file: str = "keys.json") -> list[dict]:
    """Загружает все ключи из файла."""
    path = Path(keys_file)
    if not path.exists():
        return []
    with open(path, "r") as f:
        return json.load(f)


def _pad(data: bytes) -> bytes:
    """PKCS7 паддинг (64-битный блок)."""
    padder = sym_padding.PKCS7(BLOCK_SIZE * 8).padder()
    padded = padder.update(data) + padder.finalize()
    print(f"  Паддинг: {len(data)} -> {len(padded)} байт")
    return padded


def _unpad(data: bytes) -> bytes:
    """Снятие PKCS7 паддинга."""
    unpadder = sym_padding.PKCS7(BLOCK_SIZE * 8).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def _split_blocks(data: bytes) -> list[bytes]:
    """Разбивает данные на блоки по BLOCK_SIZE байт."""
    return [data[i:i + BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]


def encrypt_des(plaintext: bytes, key: bytes) -> bytes:
    """Шифрует данные алгоритмом DES (ECB)."""
    print(f"\n--- DES шифрование ---")
    print(f"  Ключ: {key.hex()}")
    print(f"  Размер открытого текста: {len(plaintext)} байт")

    padded = _pad(plaintext)
    cipher = Cipher(TripleDES(key), modes.ECB())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    blocks_in = _split_blocks(padded)
    blocks_out = _split_blocks(ciphertext)
    print(f"  Количество блоков: {len(blocks_in)}")
    for i, (bi, bo) in enumerate(zip(blocks_in, blocks_out)):
        print(f"  Блок {i + 1}: {bi.hex()} -> {bo.hex()}")

    return ciphertext


def decrypt_des(ciphertext: bytes, key: bytes) -> bytes:
    """Расшифровывает данные алгоритмом DES (ECB)."""
    print(f"\n--- DES расшифрование ---")
    print(f"  Ключ: {key.hex()}")
    print(f"  Размер шифртекста: {len(ciphertext)} байт")

    cipher = Cipher(TripleDES(key), modes.ECB())
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    blocks_in = _split_blocks(ciphertext)
    blocks_out = _split_blocks(padded)
    print(f"  Количество блоков: {len(blocks_in)}")
    for i, (bi, bo) in enumerate(zip(blocks_in, blocks_out)):
        print(f"  Блок {i + 1}: {bi.hex()} -> {bo.hex()}")

    return _unpad(padded)


def encrypt_magma(plaintext: bytes, key: bytes) -> bytes:
    """Шифрует данные алгоритмом МАГМА (ГОСТ Р 34.12-2015, ECB)."""
    print(f"\n--- МАГМА шифрование ---")
    print(f"  Ключ: {key.hex()}")
    print(f"  Размер открытого текста: {len(plaintext)} байт")

    padded = _pad(plaintext)
    magma_cipher = gostcipher.new('magma', key, gostcipher.MODE_ECB)
    ciphertext = bytes(magma_cipher.encrypt(padded))

    blocks_in = _split_blocks(padded)
    blocks_out = _split_blocks(ciphertext)
    print(f"  Количество блоков: {len(blocks_in)}")
    for i, (bi, bo) in enumerate(zip(blocks_in, blocks_out)):
        print(f"  Блок {i + 1}: {bi.hex()} -> {bo.hex()}")

    return ciphertext


def decrypt_magma(ciphertext: bytes, key: bytes) -> bytes:
    """Расшифровывает данные алгоритмом МАГМА (ГОСТ Р 34.12-2015, ECB)."""
    print(f"\n--- МАГМА расшифрование ---")
    print(f"  Ключ: {key.hex()}")
    print(f"  Размер шифртекста: {len(ciphertext)} байт")

    magma_cipher = gostcipher.new('magma', key, gostcipher.MODE_ECB)
    padded = bytes(magma_cipher.decrypt(ciphertext))

    blocks_in = _split_blocks(ciphertext)
    blocks_out = _split_blocks(padded)
    print(f"  Количество блоков: {len(blocks_in)}")
    for i, (bi, bo) in enumerate(zip(blocks_in, blocks_out)):
        print(f"  Блок {i + 1}: {bi.hex()} -> {bo.hex()}")

    return _unpad(padded)


def encrypt(plaintext: str, key: bytes, cipher_type: CipherType,
            encoding: Encoding) -> bytes:
    """Шифрует текстовое сообщение выбранным шифром и кодировкой."""
    print(f"\nКодировка текста: {encoding.value}")
    data = plaintext.encode(encoding.value)
    print(f"Текст в байтах ({encoding.value}): {data.hex()}")

    if cipher_type == CipherType.DES:
        return encrypt_des(data, key)
    else:
        return encrypt_magma(data, key)


def decrypt(ciphertext: bytes, key: bytes, cipher_type: CipherType,
            encoding: Encoding) -> str:
    """Расшифровывает сообщение и декодирует в строку."""
    if cipher_type == CipherType.DES:
        data = decrypt_des(ciphertext, key)
    else:
        data = decrypt_magma(ciphertext, key)

    result = data.decode(encoding.value)
    print(f"Декодирование из {encoding.value}: '{result}'")
    return result


def get_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  Пожалуйста, введите целое число.")


def main():


    print("\nВыберите шифр:")
    print("  1) DES")
    print("  2) МАГМА (ГОСТ Р 34.12-2015)")
    choice = get_int("Ваш выбор: ")
    cipher_type = CipherType.DES if choice == 1 else CipherType.MAGMA

    print("\nВыберите кодировку:")
    print("  1) UTF-8")
    print("  2) CP1251 (Windows-1251)")
    enc_choice = get_int("Ваш выбор: ")
    encoding = Encoding.UTF8 if enc_choice == 1 else Encoding.CP1251

    print("\nКлюч:")
    print("  1) Сгенерировать новый")
    print("  2) Загрузить из файла")
    key_choice = get_int("Ваш выбор: ")

    if key_choice == 2:
        keys = load_keys()
        if not keys:
            print("Файл ключей пуст, генерирую новый ключ.")
            key = generate_key(cipher_type)
            save_key(key, cipher_type)
        else:
            print("Доступные ключи:")
            for i, k in enumerate(keys):
                print(f"  {i + 1}) {k['cipher']}: {k['key_hex'][:16]}...")
            idx = get_int("Номер ключа: ") - 1
            key = bytes.fromhex(keys[idx]["key_hex"])
            print(f"Загружен ключ: {key.hex()}")
    else:
        key = generate_key(cipher_type)
        save_key(key, cipher_type)

    print("\nДействие:")
    print("  1) Шифровать")
    print("  2) Расшифровать")
    action = get_int("Ваш выбор: ")

    print("\nИсточник данных:")
    print("  1) Ввод с клавиатуры")
    print("  2) Чтение из файла")
    src = get_int("Ваш выбор: ")

    if action == 1:
        if src == 1:
            text = input("Введите текст: ")
        else:
            path = input("Путь к файлу: ")
            with open(path, "r", encoding=encoding.value) as f:
                text = f.read()
            print(f"Прочитано из файла: {len(text)} символов")

        ciphertext = encrypt(text, key, cipher_type, encoding)

        print("\nВывод результата:")
        print("  1) На экран")
        print("  2) В файл")
        out = get_int("Ваш выбор: ")
        if out == 1:
            print(f"\nШифртекст (hex): {ciphertext.hex()}")
        else:
            path = input("Путь к файлу: ")
            with open(path, "wb") as f:
                f.write(ciphertext)
            print(f"Записано в {path}")
    else:
        if src == 1:
            hex_str = input("Введите шифртекст (hex): ")
            ciphertext = bytes.fromhex(hex_str)
        else:
            path = input("Путь к файлу: ")
            with open(path, "rb") as f:
                ciphertext = f.read()
            print(f"Прочитано из файла: {len(ciphertext)} байт")

        plaintext = decrypt(ciphertext, key, cipher_type, encoding)

        print("\nВывод результата:")
        print("  1) На экран")
        print("  2) В файл")
        out = get_int("Ваш выбор: ")
        if out == 1:
            print(f"\nОткрытый текст: {plaintext}")
        else:
            path = input("Путь к файлу: ")
            with open(path, "w", encoding=encoding.value) as f:
                f.write(plaintext)
            print(f"Записано в {path}")


if __name__ == "__main__":
    main()