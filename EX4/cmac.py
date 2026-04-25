from typing import List 
def to_hex(arr): 
    return ''.join(f'{x:02x}' for x in arr) 
def xor(a, b): 
    return [x ^ y for x, y in zip(a, b)] 
# Dummy AES block (same as your JS logic) 
def aes_block(block, key, log): 
    log("\n--- ENTERING AES BLOCK ---") 
    log("Input: " + to_hex(block)) 
    state = xor(block, key) 
    log("Initial XOR with Key (AddRoundKey): " + to_hex(state)) 
    # Simplified rounds 
    for i in range(3): 
        state = [(x ^ 0x63) & 0xFF for x in state] 
        log(f"Round {i+1} Output: " + to_hex(state)) 
    return state 
def left_shift(arr): 
    res = [0]*16 
    carry = 0 
    for i in range(15, -1, -1): 
        res[i] = ((arr[i] << 1) & 0xFF) | carry 
        carry = (arr[i] >> 7) & 1 
    return res 
def cmac_no_padding(message: str, key_str: str): 
    steps = [] 
    def log(msg): 
        steps.append(msg) 
    # Convert message and key 
    data = list(message.encode()) 
    key = list(key_str.encode())[:16] 
 
    while len(key) < 16: 
        key.append(0) 
    log("Message Hex: " + to_hex(data)) 
    log("Key Hex: " + to_hex(key)) 
    # --- STEP 1: SUBKEY GENERATION --- 
    log("\n[STEP 1] Generating Subkeys") 
    zero_block = [0]*16 
    L = aes_block(zero_block, key, log) 
    log("L (AES encryption of zero): " + to_hex(L)) 
    K1 = left_shift(L) 
    if L[0] & 0x80: 
        K1[15] ^= 0x87 
        log("MSB of L was 1, XORed shifted L with 0x87") 
    log("K1: " + to_hex(K1)) 
    # --- STEP 2: BLOCK PREPARATION --- 
    if len(data) == 0: 
        data = [0]*16 
    while len(data) % 16 != 0: 
        data.append(0) 
    blocks = [data[i:i+16] for i in range(0, len(data), 16)] 
    log(f"\n[STEP 2] Message divided into {len(blocks)} block(s).") 
    # --- STEP 3: PROCESSING --- 
    X = [0]*16 
    for i in range(len(blocks) - 1): 
        log(f"\nProcessing Block {i}: " + to_hex(blocks[i])) 
        X = aes_block(xor(X, blocks[i]), key, log) 
        log("Current Intermediate State (X): " + to_hex(X)) 
    # --- STEP 4: FINAL BLOCK --- 
    log("\n[STEP 3] Final Block Processing (Always using K1)") 
    last_block = blocks[-1] 
log("Last Block Content: " + to_hex(last_block)) 
M_last = xor(xor(X, last_block), K1) 
log("Final XOR result (X ^ LastBlock ^ K1): " + to_hex(M_last)) 
T = aes_block(M_last, key, log) 
log("\n==============================") 
log("FINAL CMAC TAG: " + to_hex(T)) 
log("==============================") 
return T, steps 
# ---- RUN ---- 
if __name__ == "__main__": 
msg = input("Enter message: ") 
key = input("Enter key (16 bytes): ") 
tag, steps = cmac_no_padding(msg, key) 
print("\n--- INTERMEDIATE STEPS ---") 
for s in steps: 
print(s) 
print("\nFinal CMAC Tag:", to_hex(tag)) 