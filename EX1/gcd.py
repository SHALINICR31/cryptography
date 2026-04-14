def gcd_recursive(a, b):
    if b == 0:
        return a
    return gcd_recursive(b, a % b)

# Example
print("GCD is:", gcd_recursive(48, 18))