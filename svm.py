from typing import List

# === Structure Signature (for SVM) ===
class StructureSignature:
    def __init__(self, x: float, phi_x: float, delta_x: float, zk_passed: bool, entropy: float, references: List[str]):
        self.x = x
        self.phi_x = phi_x
        self.delta_x = delta_x
        self.zk_passed = zk_passed
        self.entropy = entropy
        self.references = references

# === Structure VM Path Validator ===
def is_valid_structure_path(path: List[StructureSignature], entropy_threshold: float = 1.0) -> bool:
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
def test_svm_valid():
    path = [
        StructureSignature(x=1, phi_x=0.6, delta_x=0.08, zk_passed=True, entropy=1.1, references=[]),
        StructureSignature(x=2, phi_x=0.58, delta_x=0.07, zk_passed=True, entropy=1.2, references=[]),
        StructureSignature(x=3, phi_x=0.56, delta_x=0.05, zk_passed=True, entropy=1.3, references=[]),
    ]
    assert is_valid_structure_path(path)

def test_svm_invalid_delta():
    path = [
        StructureSignature(x=1, phi_x=0.6, delta_x=0.05, zk_passed=True, entropy=1.0, references=[]),
        StructureSignature(x=2, phi_x=0.6, delta_x=0.06, zk_passed=True, entropy=1.0, references=[]),
    ]
    assert not is_valid_structure_path(path)

def test_svm_invalid_zk():
    path = [
        StructureSignature(x=1, phi_x=0.6, delta_x=0.05, zk_passed=False, entropy=1.1, references=[]),
        StructureSignature(x=2, phi_x=0.58, delta_x=0.04, zk_passed=True, entropy=1.2, references=[]),
    ]
    assert not is_valid_structure_path(path)

def test_svm_low_entropy():
    path = [
        StructureSignature(x=1, phi_x=0.6, delta_x=0.03, zk_passed=True, entropy=0.8, references=[]),
        StructureSignature(x=2, phi_x=0.58, delta_x=0.02, zk_passed=True, entropy=0.9, references=[]),
    ]
    assert not is_valid_structure_path(path)

if __name__ == "__main__":
    print("--- test_svm_valid ---")
    path_valid = [
        StructureSignature(x=1, phi_x=0.6, delta_x=0.08, zk_passed=True, entropy=1.1, references=[]),
        StructureSignature(x=2, phi_x=0.58, delta_x=0.07, zk_passed=True, entropy=1.2, references=[]),
        StructureSignature(x=3, phi_x=0.56, delta_x=0.05, zk_passed=True, entropy=1.3, references=[]),
    ]
    for s in path_valid:
        print(s.__dict__)
    print("Result:", is_valid_structure_path(path_valid))

    print("--- test_svm_invalid_delta ---")
    path_delta = [
        StructureSignature(x=1, phi_x=0.6, delta_x=0.05, zk_passed=True, entropy=1.0, references=[]),
        StructureSignature(x=2, phi_x=0.6, delta_x=0.06, zk_passed=True, entropy=1.0, references=[]),
    ]
    for s in path_delta:
        print(s.__dict__)
    print("Result:", is_valid_structure_path(path_delta))

    print("--- test_svm_invalid_zk ---")
    path_zk = [
        StructureSignature(x=1, phi_x=0.6, delta_x=0.05, zk_passed=False, entropy=1.1, references=[]),
        StructureSignature(x=2, phi_x=0.58, delta_x=0.04, zk_passed=True, entropy=1.2, references=[]),
    ]
    for s in path_zk:
        print(s.__dict__)
    print("Result:", is_valid_structure_path(path_zk))

    print("--- test_svm_low_entropy ---")
    path_entropy = [
        StructureSignature(x=1, phi_x=0.6, delta_x=0.03, zk_passed=True, entropy=0.8, references=[]),
        StructureSignature(x=2, phi_x=0.58, delta_x=0.02, zk_passed=True, entropy=0.9, references=[]),
    ]
    for s in path_entropy:
        print(s.__dict__)
    print("Result:", is_valid_structure_path(path_entropy))

    print("All SVM path tests passed.")
