def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_primes(max_n):
    return [n for n in range(2, max_n + 1) if is_prime(n)]
