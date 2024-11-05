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

def is_generator(g, p):
    if g <= 1 or g >= p:
        return False
    factors = prime_factors(p - 1)
    for factor in factors:
        if pow(g, (p - 1) // factor, p) == 1:
            return False
    return True

def prime_factors(n):
    i = 2
    factors = set()
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.add(i)
    if n > 1:
        factors.add(n)
    return factors

def generate_keys(p):
    while True:
        g = random.randint(2, p - 2)
        if is_generator(g, p):
            break
    private_key = random.randint(2, p - 2)
    public_key = pow(g, private_key, p)
    return private_key, public_key, g

def encrypt(message, public_key, g, p):
    k = random.randint(2, p - 2)
    c1 = pow(g, k, p)
    c2 = (message * pow(public_key, k, p)) % p
    return c1, c2

def decrypt(c1, c2, private_key, p):
    s = pow(c1, private_key, p)
    message = (c2 * pow(s, p - 2, p)) % p
    return message

def main():
    # Запрос размерности ключа в битах
    bits = int(input("Введите размерность ключа в битах (кратно степени 2): "))
    if bits % 8 != 0:
        print("Размерность ключа должна быть кратна 8.")
        sys.exit(1)

    p = generate_prime(bits)
    print(f"Сгенерировано простое число p: {p}")

    alice_private_key, alice_public_key, g = generate_keys(p)
    print(f"Закрытый ключ Алисы: {alice_private_key}")
    print(f"Открытый ключ Алисы: {alice_public_key}")
    print(f"Генератор g: {g}")

    bob_private_key, bob_public_key, _ = generate_keys(p)
    print(f"Закрытый ключ Боба: {bob_private_key}")
    print(f"Открытый ключ Боба: {bob_public_key}")

    response = 24 
    print(f"Исходное сообщение Боба: {response}")

    c1, c2 = encrypt(response, alice_public_key, g, p)
    print(f"Зашифрованный ответ Боба (c1, c2): ({c1}, {c2})")

    print("Боб отправляет зашифрованный ответ Алисе.")

    decrypted_response = decrypt(c1, c2, alice_private_key, p)
    print(f"Расшифрованный ответ Алисы: {decrypted_response}")

if __name__ == "__main__":
    main()