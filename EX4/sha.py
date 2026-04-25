import struct 
import math 
MASK = 0xFFFFFFFF 
def rotr(x, n): 
return ((x >> n) | (x << (32 - n))) & MASK 
def hex8(x): 
return format(x & MASK, '08x') 
# Generate K constants (instead of hardcoding) 
def generate_K(): 
return [int((abs(math.sin(i + 1)) * (2**32))) & MASK for i in range(64)] 
# Generate initial hash values (from square roots of primes) 
def generate_H(): 
primes = [2,3,5,7,11,13,17,19] 
return [int((math.sqrt(p) % 1) * (2**32)) & MASK for p in primes] 
def sha256_simple(msg): 
steps = [] 
log = lambda x: steps.append(x) 
K = generate_K() 
h = generate_H() 
data = bytearray(msg.encode()) 
bit_len = len(data) * 8 
# Padding 
data.append(0x80) 
while len(data) % 64 != 56: 
data.append(0) 
data += struct.pack(">Q", bit_len) 
log("PADDING DONE") 
# Process block 
for chunk in range(0, len(data), 64): 
w = [0]*64 
        for i in range(16): 
            w[i] = struct.unpack(">I", data[chunk+i*4:chunk+i*4+4])[0] 
        for i in range(16, 64): 
            s0 = rotr(w[i-15],7) ^ rotr(w[i-15],18) ^ (w[i-15] >> 3) 
            s1 = rotr(w[i-2],17) ^ rotr(w[i-2],19) ^ (w[i-2] >> 10) 
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & MASK 
        a,b,c,d,e,f,g,hh = h 
        log("PROCESSING 64 ROUNDS") 
        for i in range(64): 
            S1 = rotr(e,6) ^ rotr(e,11) ^ rotr(e,25) 
            ch = (e & f) ^ (~e & g) 
            temp1 = (hh + S1 + ch + K[i] + w[i]) & MASK 
            S0 = rotr(a,2) ^ rotr(a,13) ^ rotr(a,22) 
            maj = (a & b) ^ (a & c) ^ (b & c) 
            temp2 = (S0 + maj) & MASK 
            hh,g,f,e,d,c,b,a = g,f,e,(d + temp1)&MASK,c,b,a,(temp1 + temp2)&MASK 
            if i % 16 == 0:  # log only important rounds 
                log(f"Round {i}: {hex8(a)} {hex8(b)} {hex8(c)} {hex8(d)}") 
        # Add back 
        h = [(x+y)&MASK for x,y in zip(h,[a,b,c,d,e,f,g,hh])] 
        log("BLOCK DONE") 
    final_hash = ''.join(hex8(x) for x in h) 
    log("FINAL HASH: " + final_hash) 
    return final_hash, steps 
# RUN 
if __name__ == "__main__": 
    text = input("Enter text: ") 
    h, steps = sha256_simple(text) 
    print("\n--- STEPS ---") 
    for s in steps: 
        print(s) 
print("\nSHA-256:", h) 