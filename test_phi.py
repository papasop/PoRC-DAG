import math
import random
from typing import List, Tuple

def generate_structure_params(seed: str, k: int = 10) -> Tuple[List[float], List[float], List[float]]:
    random.seed(seed)
    A = [random.uniform(0.5, 1.5) for _ in range(k)]
    t = [random.uniform(1.0, 5.0) for _ in range(k)]
    theta = [random.uniform(0, 2 * math.pi) for _ in range(k)]
    return A, t, theta

def phi(x: float, A: List[float], t: List[float], theta: List[float]) -> float:
    if x + 1 <= 0:
        raise ValueError("x + 1 must be positive for log operation")
    if not (len(A) == len(t) == len(theta)):
        raise ValueError("A, t, and theta must have the same length")
    return sum(Ai * math.cos(ti * math.log(x + 1) + thetai)
               for Ai, ti, thetai in zip(A, t, theta))

def delta(phi_x: float, tau: float) -> float:
    return abs(phi_x - tau)

def test_phi_output():
    A, t, theta = generate_structure_params("demo-seed", 5)
    tau = 0.5
    for x in range(1, 6):
        phi_val = phi(x, A, t, theta)
        delta_val = delta(phi_val, tau)
        print(f"x={x}, φ(x)={phi_val:.6f}, δ(x)={delta_val:.6f}")

if __name__ == "__main__":
    print("--- φ(x) and δ(x) Output Test ---")
    test_phi_output()
