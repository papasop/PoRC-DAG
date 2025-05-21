import math
import random
from typing import List, Tuple

# === Structure Function ===
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

# === Structure VM Path Checker ===
class SVMNode:
    def __init__(self, x: float, phi_x: float, delta_x: float, zk_passed: bool, entropy: float):
        self.x = x
        self.phi_x = phi_x
        self.delta_x = delta_x
        self.zk_passed = zk_passed
        self.entropy = entropy

def is_valid_structure_path(path: List[SVMNode], entropy_threshold: float = 1.0) -> bool:
    """
    Validate a structure path by ensuring:
    - delta_x decreases or stays constant
    - all zk_passed are True
    - average entropy ≥ threshold
    """
    prev_delta = float('inf')
    entropy_sum = 0
    for node in path:
        if not node.zk_passed or node.delta_x > prev_delta:
            return False
        prev_delta = node.delta_x
        entropy_sum += node.entropy
    avg_entropy = entropy_sum / len(path)
    return avg_entropy >= entropy_threshold

# === Tests ===
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

def test_svm_path_valid():
    path = [
        SVMNode(x=1, phi_x=0.6, delta_x=0.1, zk_passed=True, entropy=1.2),
        SVMNode(x=2, phi_x=0.55, delta_x=0.08, zk_passed=True, entropy=1.1),
        SVMNode(x=3, phi_x=0.52, delta_x=0.05, zk_passed=True, entropy=1.0),
    ]
    assert is_valid_structure_path(path, entropy_threshold=1.0)

def test_svm_path_invalid():
    path = [
        SVMNode(x=1, phi_x=0.6, delta_x=0.1, zk_passed=True, entropy=0.9),
        SVMNode(x=2, phi_x=0.65, delta_x=0.15, zk_passed=True, entropy=0.8),  # delta increased
    ]
    assert not is_valid_structure_path(path, entropy_threshold=1.0)

if __name__ == "__main__":
    test_phi_basic()
    test_delta_positive()
    test_phi_input_validation()
    test_svm_path_valid()
    test_svm_path_invalid()
    print("All tests passed.")
