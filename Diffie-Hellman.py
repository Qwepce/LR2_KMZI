import random
import sys

def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if p % 2 == 0:
            p += 1
        if is_prime(p):
            return p

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False

    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        if not check(a, s, d, n):
            return False
    return True

def generate_keys(p, g):
    private_key = random.randint(2, p - 2)
    public_key = pow(g, private_key, p)
    return private_key, public_key

def generate_session_key(private_key, other_public_key, p):
    return pow(other_public_key, private_key, p)

def xor_encrypt_decrypt(text, key):
    key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
    key_length = len(key_bytes)
    encrypted_text = bytearray()
    for i, char in enumerate(text):
        encrypted_text.append(char ^ key_bytes[i % key_length])
    return encrypted_text

def main():
    # Запрос размерности ключа в битах
    bits = int(input("Введите размерность ключа в битах (кратно степени 2): "))
    if bits % 8 != 0:
        print("Размерность ключа должна быть кратна 8.")
        sys.exit(1)

    p = generate_prime(bits)
    g = random.randint(2, p - 2)
    print(f"Сгенерировано простое число p: {p}")
    print(f"Сгенерирован генератор g: {g}")

    alice_private_key, alice_public_key = generate_keys(p, g)
    print(f"Закрытый ключ Алисы: {alice_private_key}")
    print(f"Открытый ключ Алисы: {alice_public_key}")

    bob_private_key, bob_public_key = generate_keys(p, g)
    print(f"Закрытый ключ Боба: {bob_private_key}")
    print(f"Открытый ключ Боба: {bob_public_key}")

    print("Алиса и Боб обмениваются открытыми ключами.")

    alice_session_key = generate_session_key(alice_private_key, bob_public_key, p)
    print(f"Сеансовый ключ Алисы: {alice_session_key}")

    bob_session_key = generate_session_key(bob_private_key, alice_public_key, p)
    print(f"Сеансовый ключ Боба: {bob_session_key}")

    if alice_session_key == bob_session_key:
        print("Сеансовые ключи совпадают.")
    else:
        print("Ошибка: сеансовые ключи не совпадают.")
        sys.exit(1)

    text = "Привет, это секретное сообщение!"
    print(f"Исходный текст: {text}")

    encrypted_text = xor_encrypt_decrypt(text.encode(), alice_session_key)
    print(f"Зашифрованный текст: {encrypted_text.hex()}")

    decrypted_text = xor_encrypt_decrypt(encrypted_text, alice_session_key).decode()
    print(f"Расшифрованный текст: {decrypted_text}")

if __name__ == "__main__":
    main()