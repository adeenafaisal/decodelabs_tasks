import math
import secrets
import string

MIN_LENGTH = 8    
RECOMMENDED_LENGTH = 15  
MAX_LENGTH = 64        
DEFAULT_LENGTH = 16

def get_length():
    """Phase 1: capture and validate the target password length."""
    while True:
        raw = input(f"Password length ({MIN_LENGTH}-{MAX_LENGTH}, "
                    f"Enter for {DEFAULT_LENGTH}): ").strip()

        if raw == "":
            return DEFAULT_LENGTH

        try:
            length = int(raw)
        except ValueError:
            print("  Invalid data: please enter a whole number.")
            continue

        if length < MIN_LENGTH or length > MAX_LENGTH:
            print(f"  Length must be between {MIN_LENGTH} and {MAX_LENGTH}.")
            continue

        if length < RECOMMENDED_LENGTH:
            print(f"  Note: NIST recommends at least {RECOMMENDED_LENGTH} "
                  "characters for high-security accounts.")
        return length


def get_use_symbols():
    """Ask whether to include special characters (@, #, $ ...)."""
    while True:
        answer = input("Include special characters? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Invalid data: please answer y or n.")

def build_pools(use_symbols):
    """Return the list of character pools to draw from."""
    pools = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if use_symbols:
        pools.append(string.punctuation)
    return pools


def generate_password(length, use_symbols=False):
    """Phase 2: the transformation engine (integer -> secure string)."""
    pools = build_pools(use_symbols)
    all_chars = "".join(pools)
    chars = [secrets.choice(pool) for pool in pools]
    chars += [secrets.choice(all_chars) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)

    return "".join(chars) 

def calculate_entropy(length, pool_size):
    """E = L * log2(R), in bits."""
    return length * math.log2(pool_size)


def rate_entropy(bits):
    if bits < 50:
        return "Weak"
    if bits < 80:
        return "Moderate"
    if bits < 100:
        return "Strong"
    return "Very strong"


def display(password, use_symbols):
    """Phase 3: present the result with its entropy score."""
    pool_size = len("".join(build_pools(use_symbols)))
    bits = calculate_entropy(len(password), pool_size)

    print("\n=== Generated Password ===")
    print(password)
    print(f"Length : {len(password)}")
    print(f"Pool   : {pool_size} characters")
    print(f"Entropy: {bits:.1f} bits ({rate_entropy(bits)})")

def main():
    print("=== Random Password Generator ===\n")
    length = get_length()
    use_symbols = get_use_symbols()
    password = generate_password(length, use_symbols)
    display(password, use_symbols)

if __name__ == "__main__":
    main()