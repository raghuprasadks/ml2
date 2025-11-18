import random
from typing import List

def generate_uniform_random(count: int = 1) -> float or List[float]:
    """
    Generates one or more uniformly distributed random floating-point numbers
    in the interval [0.0, 1.0).

    This function utilizes Python's built-in 'random.random()', which is
    based on the Mersenne Twister algorithm (a high-quality pseudo-random
    number generator).

    Args:
        count (int): The number of random numbers to generate.
                     If count is 1, a single float is returned.
                     If count > 1, a list of floats is returned.

    Returns:
        float or List[float]: A single random number or a list of random numbers.
    """
    if count < 1:
        # Handle invalid count
        return []

    if count == 1:
        # random.random() returns a float x such that 0.0 <= x < 1.0
        return random.random()
    else:
        # Generate a list of 'count' random numbers
        return [random.random() for _ in range(count)]

def evaluate_function(x: float) -> float:
    """
    The function to be integrated: f(x) = x^2 + 2x
    
    Args:
        x (float): The input value (a random sample).

    Returns:
        float: The result of f(x).
    """
    return x**2 + 2*x

# --- Example Usage ---

# 1. Generate a single random number (Original example)
single_number = generate_uniform_random()
print(f"Single uniform random number: {single_number:.4f}")

# 2. Generate 10 random samples and evaluate f(x) for each one
SAMPLE_COUNT = 10
random_samples = generate_uniform_random(count=SAMPLE_COUNT)
sum_of_fx = 0.0  # Initialize sum for Monte Carlo estimation

print(f"\n--- Evaluation of f(x) = x^2 + 2x for {SAMPLE_COUNT} Random Samples ---")
print("{:<10} {:<10}".format("Sample (x)", "Result (f(x))"))
print("-" * 21)

for i, x in enumerate(random_samples):
    f_x = evaluate_function(x)
    sum_of_fx += f_x
    print(f"{x:.6f} | {f_x:.6f}")

# 3. Monte Carlo Integration Estimate
# The integral I over [0, 1] is approximately (b - a) * (1/N) * sum(f(x_i))
# Since (b - a) = (1 - 0) = 1, I is the average of f(x_i).
monte_carlo_estimate = sum_of_fx / SAMPLE_COUNT

print("\n--- Monte Carlo Integral Estimation ---")
print(f"Total sum of f(x) values: {sum_of_fx:.6f}")
print(f"Number of samples (N): {SAMPLE_COUNT}")
print(f"Monte Carlo Estimate of Integral I: {monte_carlo_estimate:.6f}")

# Analytical integral for comparison: Integral(x^2 + 2x) dx from 0 to 1 = [x^3/3 + x^2] from 0 to 1 = 1/3 + 1 = 4/3
EXACT_INTEGRAL_VALUE = 4.0 / 3.0
print(f"Exact Analytical Integral Value: {EXACT_INTEGRAL_VALUE:.6f}")

# 4. Generating a number within a custom range [a, b) (Original example)
A = 10
B = 20
custom_range_number = A + (B - A) * generate_uniform_random()
print(f"\nRandom number in [{A}, {B}): {custom_range_number:.4f}")