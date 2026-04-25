import struct 
import math 
# Left rotate function 
def left_rotate(x, c): 
return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF 
# MD5 functions 
def F(x, y, z): return (x & y) | (~x & z) 
def G(x, y, z): return (x & z) | (y & ~z) 
def H(x, y, z): return x ^ y ^ z 
def I(x, y, z): return y ^ (x | ~z) 
# Constants 
s = [ 
    7,12,17,22, 7,12,17,22, 7,12,17,22, 7,12,17,22, 
    5,9,14,20, 5,9,14,20, 5,9,14,20, 5,9,14,20, 
    4,11,16,23, 4,11,16,23, 4,11,16,23, 4,11,16,23, 
    6,10,15,21, 6,10,15,21, 6,10,15,21, 6,10,15,21 
] 
K = [int(abs(math.sin(i + 1)) * (2**32)) & 0xFFFFFFFF for i in range(64)] 
def md5(message): 
    steps = [] 
    # Step 1: Convert to bytes 
    msg = bytearray(message, 'utf-8') 
    orig_len_bits = (8 * len(msg)) & 0xffffffffffffffff 
    steps.append(f"Step 1: Input = '{message}', Length = {len(msg)} bytes") 
    # Step 2: Padding 
    msg.append(0x80) 
    while (len(msg) * 8) % 512 != 448: 
        msg.append(0) 
    msg += struct.pack('<Q', orig_len_bits) 
    steps.append(f"Step 2: After padding length = {len(msg)} bytes" 
    # Step 3: Initialize variables 
    A = 0x67452301 
    B = 0xefcdab89 
    C = 0x98badcfe 
    D = 0x10325476 
    steps.append(f"Step 3: Initial Values:\nA={hex(A)}, B={hex(B)}, C={hex(C)}, D={hex(D)}") 
    # Step 4: Process 512-bit chunks 
    for chunk_offset in range(0, len(msg), 64): 
        chunk = msg[chunk_offset:chunk_offset+64] 
        M = list(struct.unpack('<16I', chunk)) 
        a, b, c, d = A, B, C, D 
        steps.append(f"\nProcessing Chunk {chunk_offset//64}") 
        for i in range(64): 
            if 0 <= i <= 15: 
                f = F(b, c, d) 
                g = i 
            elif 16 <= i <= 31: 
                f = G(b, c, d) 
                g = (5*i + 1) % 16 
            elif 32 <= i <= 47: 
                f = H(b, c, d) 
                g = (3*i + 5) % 16 
            else: 
                f = I(b, c, d) 
                g = (7*i) % 16 
            temp = d 
            d = c 
            c = b 
            b = (b + left_rotate((a + f + K[i] + M[g]) & 0xFFFFFFFF, s[i])) & 0xFFFFFFFF 
            a = temp 
            # Log few steps (not all 64 to keep readable) 
            if i % 16 == 0: 
                steps.append(f"Round {i//16 + 1} step {i}: A={hex(a)}, B={hex(b)}, C={hex(c)}, D={hex(d)}") 
        # Add to result 
        A = (A + a) & 0xFFFFFFFF 
        B = (B + b) & 0xFFFFFFFF 
        C = (C + c) & 0xFFFFFFFF 
        D = (D + d) & 0xFFFFFFFF 
        steps.append(f"After Chunk: A={hex(A)}, B={hex(B)}, C={hex(C)}, D={hex(D)}") 
    # Step 5: Output 
    result = ''.join(f'{x:02x}' for x in struct.pack('<4I', A, B, C, D)) 
 
steps.append(f"\nFinal MD5 Hash: {result}") 
return result, step 
# ---- Run Program ---- 
if __name__ == "__main__": 
text = input("Enter text: ") 
hash_value, steps = md5(text) 
print("\n--- INTERMEDIATE STEPS ---") 
for step in steps: 
print(step) 
print("\nFinal MD5 Hash:", hash_value) 