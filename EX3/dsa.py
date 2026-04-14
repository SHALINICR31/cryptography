import random

# Simple modular inverse
def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

# Parameters (small values for demo)
p = 23
q = 11
g = 2

# Private key
x = random.randint(1, q-1)

# Public key
y = (g ** x) % p

print("Private key:", x)
print("Public key:", y)

# Signing
def sign(message):
    k = random.randint(1, q-1)
    r = ((g ** k) % p) % q
    k_inv = mod_inverse(k, q)
    s = (k_inv * (message + x * r)) % q
    return (r, s)

# Verification
def verify(message, r, s):
    w = mod_inverse(s, q)
    u1 = (message * w) % q
    u2 = (r * w) % q
    v = (((g ** u1) * (y ** u2)) % p) % q
    return v == r

# Example
msg = 5

r, s = sign(msg)
print("Signature:", (r, s))

valid = verify(msg, r, s)
print("Valid Signature:", valid)