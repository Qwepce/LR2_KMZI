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

def generate_keys(bits):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randint(3, phi - 1)
        if extended_gcd(e, phi)[0] == 1:
            break

    d = mod_inverse(e, phi)

    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    return pow(message, e, n)

def decrypt(ciphertext, private_key):
    d, n = private_key
    return pow(ciphertext, d, n)

def main():
    bits = int(input("Введите размерность ключа в битах (кратно степени 2): "))
    if bits % 8 != 0:
        print("Размерность ключа должна быть кратна 8.")
        sys.exit(1)

    alice_public_key, alice_private_key = generate_keys(bits)
    print(f"Открытый ключ Алисы: {alice_public_key}")
    print(f"Закрытый ключ Алисы: {alice_private_key}")

    bob_public_key, bob_private_key = generate_keys(bits)
    print(f"Открытый ключ Боба: {bob_public_key}")
    print(f"Закрытый ключ Боба: {bob_private_key}")

    message = 42
    print(f"Исходное сообщение Алисы: {message}")

    encrypted_message = encrypt(message, bob_public_key)
    print(f"Зашифрованное сообщение Алисы: {encrypted_message}")

    print("Алиса отправляет зашифрованное сообщение Бобу.")

    decrypted_message = decrypt(encrypted_message, bob_private_key)
    print(f"Расшифрованное сообщение Боба: {decrypted_message}")

    response = 24
    print(f"Исходное сообщение Боба: {response}")

    encrypted_response = encrypt(response, alice_public_key)
    print(f"Зашифрованный ответ Боба: {encrypted_response}")

    print("Боб отправляет зашифрованный ответ Алисе.")

    decrypted_response = decrypt(encrypted_response, alice_private_key)
    print(f"Расшифрованный ответ Алисы: {decrypted_response}")

if __name__ == "__main__":
    main()