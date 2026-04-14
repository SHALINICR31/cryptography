import numpy as np

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def matrix_mod_inv(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = mod_inverse(det % modulus, modulus)

    if det_inv is None:
        raise ValueError("Matrix is not invertible")

    matrix_modulus_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )
    return matrix_modulus_inv

def hill_encrypt(text, key_matrix):
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += "X"

    result = ""
    for i in range(0, len(text), 2):
        pair = text[i:i+2]
        vector = np.array([[ord(pair[0]) - 65],
                           [ord(pair[1]) - 65]])

        encrypted_vector = np.dot(key_matrix, vector) % 26
        result += chr(encrypted_vector[0][0] + 65)
        result += chr(encrypted_vector[1][0] + 65)

    return result

def hill_decrypt(cipher, key_matrix):
    inverse_matrix = matrix_mod_inv(key_matrix, 26)

    result = ""
    for i in range(0, len(cipher), 2):
        pair = cipher[i:i+2]
        vector = np.array([[ord(pair[0]) - 65],
                           [ord(pair[1]) - 65]])

        decrypted_vector = np.dot(inverse_matrix, vector) % 26
        result += chr(int(decrypted_vector[0][0]) + 65)
        result += chr(int(decrypted_vector[1][0]) + 65)

    return result

# Example
key_matrix = np.array([[3, 3],
                       [2, 5]])

text = "HELLO"

encrypted = hill_encrypt(text, key_matrix)
decrypted = hill_decrypt(encrypted, key_matrix)

print("Encrypted:", encrypted)
print("Decrypted:", decrypted)