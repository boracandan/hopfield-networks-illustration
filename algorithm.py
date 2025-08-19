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

def converge_network(weights: np.ndarray, outputs: np.ndarray) -> np.ndarray:
    """
    Run Hopfield network until convergence (energy change ≤ e) or max_steps reached.
    """
    max_steps = 1000000
    e = 1e-6

    # Calculate the initial energy
    energy = calculate_energy(weights, outputs)

    # Iterative Updates
    step = 0
    while step < max_steps:
        step += 1
        
        rand_neuron = randint(0, len(outputs) - 1)

        # Compute Neuron's Input
        neuron_input = sum([weights[rand_neuron][j] * outputs[j] for j in range(len(outputs)) if j != rand_neuron])
        neuron_input_sign = -1 if neuron_input <= 0 else 1

        # Compute Suggested New State 
        if neuron_input_sign == outputs[rand_neuron]:
            continue
        outputs[rand_neuron] = neuron_input_sign
        new_energy = calculate_energy(weights, outputs)
        delta_energy = energy - new_energy

        if delta_energy <= e:
            break
        energy = new_energy


    return outputs

