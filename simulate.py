import random
import uuid
from collections import defaultdict
from phi import generate_structure_params, phi, delta

class DAGNode:
    def __init__(self, x, phi_x, delta_x, zk_passed, references):
        self.id = str(uuid.uuid4())
        self.x = x
        self.phi_x = phi_x
        self.delta_x = delta_x
        self.zk_passed = zk_passed
        self.references = references
        self.weight = 0
        self.entropy = 0

class DAG:
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(list)

    def add_node(self, node: DAGNode):
        self.nodes[node.id] = node
        for ref in node.references:
            self.edges[ref].append(node.id)

def simulate_zkp(delta_val: float, epsilon: float) -> bool:
    return delta_val < epsilon

def compute_weight(node, alpha=1.0, beta=1.0, gamma=1.0):
    reference_count = len(node.references)
    residual_term = 1.0 - (node.delta_x / 0.1)
    entropy_term = node.entropy
    node.weight = alpha * reference_count + beta * residual_term + gamma * entropy_term
    return node.weight

# ====== Run Simulation ======
if __name__ == "__main__":
    seed = "node_01"
    k = 10
    A, t, theta = generate_structure_params(seed, k)
    dag = DAG()

    tau = 0.5
    epsilon = 0.1

    for i in range(20):
        x = i + 1
        phi_x = phi(x, A, t, theta)
        delta_x = delta(phi_x, tau)
        zk = simulate_zkp(delta_x, epsilon)
        references = list(dag.nodes.keys())[-3:]
        node = DAGNode(x, phi_x, delta_x, zk, references)
        node.entropy = random.uniform(0.5, 2.0)
        compute_weight(node)
        dag.add_node(node)

    print(f"DAG size: {len(dag.nodes)} nodes")
