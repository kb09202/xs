from qiskit import QuantumCircuit, transpile, assemble
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram

# Créer un circuit quantique avec un qubit et un bit classique
qc = QuantumCircuit(1, 1)

# Appliquer une porte Hadamard pour mettre le qubit en superposition
qc.h(0)

# Mesurer le qubit et stocker le résultat dans le bit classique
qc.measure(0, 0)

# Visualiser le circuit
print(qc)

# Simuler le circuit
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
qobj = assemble(compiled_circuit)
result = simulator.run(qobj, shots=1024).result()

# Obtenir les résultats de la simulation
counts = result.get_counts()

# Afficher les résultats
print("\nTotal count for 0 and 1 are:", counts)
plot_histogram(counts).show()
