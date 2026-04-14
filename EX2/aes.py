# Simplified AES (16 bytes block)

# Simple S-box (partial for demo)
sbox = {
    0x0: 0x6, 0x1: 0x4, 0x2: 0xC, 0x3: 0x5,
    0x4: 0x0, 0x5: 0x7, 0x6: 0x2, 0x7: 0xE,
    0x8: 0x1, 0x9: 0xF, 0xA: 0x3, 0xB: 0xD,
    0xC: 0x8, 0xD: 0xA, 0xE: 0x9, 0xF: 0xB
}

def sub_bytes(state):
    return [sbox[b] for b in state]

def shift_rows(state):
    return [
        state[0], state[1], state[2], state[3],
        state[5], state[6], state[7], state[4],
        state[10], state[11], state[8], state[9],
        state[15], state[12], state[13], state[14]
    ]

def add_round_key(state, key):
    return [s ^ k for s, k in zip(state, key)]

def aes_encrypt(plaintext, key):
    state = plaintext[:]

    # Round 1
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key)

    # Round 2
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key)

    return state

# Example (values in hex form)
plaintext = [0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8,
             0x9,0xA,0xB,0xC,0xD,0xE,0xF,0x0]

key = [0x0]*16

cipher = aes_encrypt(plaintext, key)
print("Encrypted:", cipher)