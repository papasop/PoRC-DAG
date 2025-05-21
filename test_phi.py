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

def test_phi_basic():
    A, t, theta = generate_structure_params("test_seed", 5)
    val = phi(10, A, t, theta)
    assert isinstance(val, float)

def test_delta_positive():
    assert abs(delta(0.6, 0.5) - 0.1) < 1e-9
    assert abs(delta(-1.0, 1.0) - 2.0) < 1e-9

def test_phi_input_validation():
    try:
        phi(-2, [1], [1], [0])
    except ValueError as e:
        assert "log operation" in str(e)

    try:
        phi(10, [1], [1], [0, 0])
    except ValueError as e:
        assert "same length" in str(e)

if __name__ == "__main__":
    test_phi_basic()
    test_delta_positive()
    test_phi_input_validation()
    print("All tests passed.")
