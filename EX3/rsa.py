# GCD
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Modular inverse (Extended Euclidean)
def mod_inverse(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    return None

# RSA Key Generation
p = 17
q = 11

n = p * q
phi = (p - 1) * (q - 1)

e = 7  # choose e such that gcd(e, phi)=1
d = mod_inverse(e, phi)

print("Public Key:", (e, n))
print("Private Key:", (d, n))

# Encryption
def encrypt(msg, e, n):
    return (msg ** e) % n

# Decryption
def decrypt(cipher, d, n):
    return (cipher ** d) % n

# Example
message = 9

cipher = encrypt(message, e, n)
print("Encrypted:", cipher)

original = decrypt(cipher, d, n)
print("Decrypted:", original)