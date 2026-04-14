def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def vigenere_encrypt(text, key):
    key = generate_key(text, key)
    result = ""

    for i in range(len(text)):
        if text[i].isalpha():
            x = (ord(text[i].upper()) + ord(key[i].upper())) % 26
            x += ord('A')
            result += chr(x)
        else:
            result += text[i]

    return result

def vigenere_decrypt(cipher, key):
    key = generate_key(cipher, key)
    result = ""

    for i in range(len(cipher)):
        if cipher[i].isalpha():
            x = (ord(cipher[i].upper()) - ord(key[i].upper()) + 26) % 26
            x += ord('A')
            result += chr(x)
        else:
            result += cipher[i]

    return result

# Example
text = "HELLO"
key = "KEY"

encrypted = vigenere_encrypt(text, key)
decrypted = vigenere_decrypt(encrypted, key)

print("Encrypted:", encrypted)
print("Decrypted:", decrypted)