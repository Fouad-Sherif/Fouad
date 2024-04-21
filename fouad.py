import random
import math
import time

def is_prime(num):
    """Check if a number is prime."""
    if num <= 1:
        return False
    elif num <= 3:
        return True
    elif num % 2 == 0 or num % 3 == 0:
        return False
    # Check divisibility by all numbers of the form 6k ± 1 up to sqrt(n)
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_large_prime(bits):
    """Generate a large prime number with the specified number of bits."""
    while True:
        # Generate a random number in the specified range
        prime_candidate = random.randint(2**(bits-1), 2**bits)
        # Check if the number is prime
        if is_prime(prime_candidate):
            return prime_candidate

def calculate_gcd(a, b):
    """Calculate the greatest common divisor of two numbers using the Euclidean algorithm."""
    while b != 0:
        a, b = b, a % b
    return a

def extended_euclidean_algorithm(a, b):
    """Calculate the extended Euclidean algorithm to find the modular inverse."""
    if a == 0:
        return b, 0, 1
    else:
        # Recursively call the extended Euclidean algorithm
        gcd_value, x, y = extended_euclidean_algorithm(b % a, a)
        return (gcd_value, y - (b // a) * x, x)

def factorize_modulus(modulus):
    """Factorize the modulus into its prime factors."""
    for i in range(2, int(math.sqrt(modulus)) + 1):
        if modulus % i == 0:
            return i, modulus // i

def calculate_private_exponent(public_exponent, prime_p, prime_q):
    """Calculate the private exponent given the public exponent and prime factors."""
    phi = (prime_p - 1) * (prime_q - 1)
    # Calculate the modular inverse using the extended Euclidean algorithm
    gcd_value, private_exponent, _ = extended_euclidean_algorithm(public_exponent, phi)
    private_exponent %= phi
    if private_exponent < 0:
        private_exponent += phi
    return private_exponent

def brute_force_private_exponent(public_exponent, phi):
    """Attempt to brute force the private exponent."""
    private_exponent = 2
    while True:
        # Check if the current value of the private exponent satisfies the condition (e * d) % phi == 1
        if (public_exponent * private_exponent) % phi == 1:
            return private_exponent
        # Increment the private exponent for the next iteration
        private_exponent += 1

def main():
    print("RSA Security Analysis: Runtime Comparison\n")
    # Prompt the user to choose the key size
    key_size = int(input("Enter the key size (8 or 16 bits): "))
    # Validate the input key size
    if key_size not in [8, 16]:
        print("Invalid key size. Please choose either 8 or 16 bits.")
        return
    
    # Generate RSA keys
    bits = key_size
    print("\nGenerating RSA keys...")
    start_time = time.perf_counter()
    prime_p = generate_large_prime(bits)
    prime_q = generate_large_prime(bits)
    modulus = prime_p * prime_q
    public_exponent = 65537
    end_time = time.perf_counter()
    print("RSA keys generated successfully.")
    print("Public Key (modulus, public exponent):", (modulus, public_exponent))
    print("Key Generation Time: {:.6f} milliseconds".format((end_time - start_time) * 1000))

    # Factorize the modulus to obtain prime factors
    print("\nFactoring modulus...")
    start_time = time.perf_counter()
    prime_p, prime_q = factorize_modulus(modulus)
    end_time = time.perf_counter()
    print("Modulus factored successfully.")
    print("Prime Factors (prime_p, prime_q):", (prime_p, prime_q))
    print("Factorization Time: {:.6f} milliseconds".format((end_time - start_time) * 1000))
    
    # Calculate phi(N)
    phi = (prime_p - 1) * (prime_q - 1)
    # Calculate the private exponent d
    print("\nCalculating private exponent...")
    start_time = time.perf_counter()
    private_exponent = calculate_private_exponent(public_exponent, prime_p, prime_q)
    end_time = time.perf_counter()
    print("Private exponent calculated successfully.")
    print("Private Exponent:", private_exponent)
    print("Private Exponent Calculation Time: {:.6f} milliseconds".format((end_time - start_time) * 1000))
    
    # Attempt brute force for 8-bit keys
    if key_size == 8:
        print("\nAttempting brute force for 8-bit keys...")
        start_time = time.perf_counter()
        brute_force_d = brute_force_private_exponent(public_exponent, phi)
        end_time = time.perf_counter()
        print("Brute force completed.")
        print("Brute Force Private Exponent:", brute_force_d)
        print("Brute Force Time: {:.6f} milliseconds".format((end_time - start_time) * 1000))
    
    # Optionally attempt brute force for 16-bit keys
    if key_size == 16:
        print("\nBrute force for 16-bit keys is computationally intensive and may take a long time.")
        choice = input("Do you want to attempt brute force for 16-bit keys? (yes/no): ").lower()
        if choice == "yes":
            print("\nAttempting brute force for 16-bit keys...")
            start_time = time.perf_counter()
            brute_force_d = brute_force_private_exponent(public_exponent, phi)
            end_time = time.perf_counter()
            print("Brute force completed.")
            print("Brute Force Private Exponent:", brute_force_d)
            print("Brute Force Time: {:.6f} milliseconds".format((end_time - start_time) * 1000))
        else:
            print("Brute force for 16-bit keys was not attempted.")

if __name__ == "__main__":
    main()