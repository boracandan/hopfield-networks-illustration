import numpy as np
from random import randint
from scipy.special import logsumexp

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
    Run Classical Hopfield network until convergence (energy change ≤ e) or max_steps reached.
    """
    max_steps = 30000

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

def converge_network_modern(patterns: np.ndarray, state: np.ndarray, max_steps: int = 30000) -> np.ndarray:
    """
    Run Discrete Modern Hopfield Network (Demircigil et al.) until convergence.
    
    patterns: (m, n) matrix of stored patterns (each column is one stored pattern)
    state: (m,) initial state vector (values in {-1, +1})
    max_steps: maximum number of update iterations
    """
    state = state.copy().astype(int).reshape(-1)  # ensure 1D array of ints
    print(state.shape, patterns.shape)
    m = len(state)

    def calculate_energy_modern(patterns, state):
        x = patterns.T @ state
        return -logsumexp(x)   # stable computation of sum(exp(x))

    for step in range(max_steps):
        changed = False
        indices = np.random.permutation(m)

        for i in indices:
            # Flip ith neuron to +1 or -1
            state_pos = state.copy()
            state_pos[i] = 1
            state_neg = state.copy()
            state_neg[i] = -1

            # Compute energy difference
            diff = -calculate_energy_modern(patterns, state_pos) + calculate_energy_modern(patterns, state_neg)

            new_val = np.sign(diff)
            if new_val == 0:  # resolve tie
                new_val = -1

            if new_val != state[i]:
                state[i] = new_val
                changed = True

        if not changed:
            break

    return state


