import numpy as np
from random import randint

def calculate_energy(weights: np.ndarray, outputs: np.ndarray) -> float:
    """
    Calculate Hopfield network energy, excluding self-connections.
    """
    energy = 0
    for i in range(len(outputs)):
        for j in range(len(outputs)):
            if i != j:
                energy += weights[i][j] * outputs[i] * outputs[j]
    energy *= -1/2
    
    return energy

def calculate_weight_matrix(memories: list[dict[str, list[int]]]) -> np.ndarray:
    """
    Calculate Hopfield weight matrix using the pseudo-inverse rule.
    Memories should be stored as ±1 vectors.
    """
    # Convert memories to a list of numpy arrays
    memory_arrays = [np.array(next(iter(memory.values())), dtype=int) for memory in memories]
    
    # Stack memories into a matrix X of shape (N, m)
    X = np.column_stack(memory_arrays)  # N x m
    
    # Compute pseudo-inverse weight matrix
    W = X @ np.linalg.pinv(X.T @ X) @ X.T
    
    # Remove self-connections
    np.fill_diagonal(W, 0)
    
    return W

def converge_network(weights: np.ndarray, outputs: np.ndarray) -> np.ndarray:
    """
    Run Hopfield network until convergence (energy change ≤ e) or max_steps reached.
    """
    max_steps = 30000
    e = 1e-12

    # Iterative Updates
    step = 0
    while step < max_steps:
        step += 1
        changed = False

        indicies = np.random.permutation(len(outputs))

        for rand_neuron in indicies:
            # Compute Neuron's Input
            neuron_input = sum([weights[rand_neuron][j] * outputs[j] for j in range(len(outputs)) if j != rand_neuron])
            neuron_input_sign = 1 if neuron_input > 0 else -1

            # Compute Suggested New State 
            if neuron_input_sign == outputs[rand_neuron]:
                continue
            outputs[rand_neuron] = neuron_input_sign
            changed = True
        
        if not changed:
            break

    return outputs


