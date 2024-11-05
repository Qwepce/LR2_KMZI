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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"{a} не имеет обратного элемента по модулю {m}")
    return x % m

def generate_keys(p):
    while True:
        private_key = random.randint(2, p - 2)
        try:
            public_key = mod_inverse(private_key, p - 1)
            return private_key, public_key
        except ValueError:
            continue

def encrypt(message, public_key, p):
    return pow(message, public_key, p)

def decrypt(ciphertext, private_key, p):
    return pow(ciphertext, private_key, p)

def main():
    bits = int(input("Введите размерность ключа в битах (кратно степени 2): "))
    if bits % 8 != 0:
        print("Размерность ключа должна быть кратна 8.")
        sys.exit(1)

    p = generate_prime(bits)
    print(f"Сгенерировано простое число p: {p}")

    alice_private_key, alice_public_key = generate_keys(p)
    print(f"Закрытый ключ Алисы: {alice_private_key}")
    print(f"Открытый ключ Алисы: {alice_public_key}")

    bob_private_key, bob_public_key = generate_keys(p)
    print(f"Закрытый ключ Боба: {bob_private_key}")
    print(f"Открытый ключ Боба: {bob_public_key}")

    message = 42  
    print(f"Исходное сообщение Алисы: {message}")

    encrypted_message = encrypt(message, bob_public_key, p)
    print(f"Зашифрованное сообщение Алисы: {encrypted_message}")

    print("Алиса отправляет зашифрованное сообщение Бобу.")

    decrypted_message = decrypt(encrypted_message, bob_private_key, p)
    print(f"Расшифрованное сообщение Боба: {decrypted_message}")

    response = 24  
    print(f"Исходное сообщение Боба: {response}")

    encrypted_response = encrypt(response, alice_public_key, p)
    print(f"Зашифрованный ответ Боба: {encrypted_response}")

    print("Боб отправляет зашифрованный ответ Алисе.")

    decrypted_response = decrypt(encrypted_response, alice_private_key, p)
    print(f"Расшифрованный ответ Алисы: {decrypted_response}")

if __name__ == "__main__":
    main()