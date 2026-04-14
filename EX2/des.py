# Simple DES-like (Feistel structure)

def xor(a, b):
    return ''.join(str(int(i) ^ int(j)) for i, j in zip(a, b))

def swap(left, right):
    return right, left

def f_function(right, key):
    # simple XOR with key (real DES uses expansion + S-box)
    return xor(right, key)

def encrypt(plaintext, key):
    # assume 8-bit plaintext and key
    left = plaintext[:4]
    right = plaintext[4:]

    for i in range(2):  # 2 rounds (DES uses 16)
        temp = right
        right = xor(left, f_function(right, key))
        left = temp

    return left + right

def decrypt(ciphertext, key):
    left = ciphertext[:4]
    right = ciphertext[4:]

    for i in range(2):
        temp = left
        left = xor(right, f_function(left, key))
        right = temp

    return left + right

# Example
pt = "10101010"
key = "11001100"

ct = encrypt(pt, key)
print("Encrypted:", ct)

dt = decrypt(ct, key)
print("Decrypted:", dt)