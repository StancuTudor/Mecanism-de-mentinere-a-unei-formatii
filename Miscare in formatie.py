import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
import random as rnd


def d(A, B):
    return np.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)

agents = [
    [np.random.random() * 10, np.random.random() * 10, "red"],
    [np.random.random() * 10, np.random.random() * 10, "orange"],
    [np.random.random() * 10, np.random.random() * 10, "yellow"],
    [np.random.random() * 10, np.random.random() * 10, "green"],
    [np.random.random() * 10, np.random.random() * 10, "blue"],
    [np.random.random() * 10, np.random.random() * 10, "purple"]
]
vAgents = [
    [np.random.random() * 2 - 1, np.random.random() * 2 - 1],
    [np.random.random() * 2 - 1, np.random.random() * 2 - 1],
    [np.random.random() * 2 - 1, np.random.random() * 2 - 1],
    [np.random.random() * 2 - 1, np.random.random() * 2 - 1],
    [np.random.random() * 2 - 1, np.random.random() * 2 - 1],
    [np.random.random() * 2 - 1, np.random.random() * 2 - 1]
]

def ShowAgents(text):
    for a in agents:
        plt.plot(a[0], a[1], 'o', color=a[2])
    plt.suptitle(text)
    plt.show()

def DrawLinesAgents(A, B):
    x_values = [A[0], B[0]]
    y_values = [A[1], B[1]]
    plt.plot(x_values, y_values, 'bo', linestyle="--")
    mid = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2]
    # plt.text(mid[0] + 0.02, mid[1] + 0.02, ("%.2f" % d(A, B)))

goal = [
    [0, 1, 1, 2, 0, 2],
    [1, 0, 1, 1, 1, 0],
    [1, 1, 0, 0, 1, 1],
    [2, 1, 0, 0, 1, 2],
    [0, 1, 1, 1, 0, 1],
    [2, 0, 1, 2, 1, 0]
]
ShowAgents("Pozitia initiala")

# Simulare gradient
steps = range(1000)
positions = [[] for a in agents]
distance_error = [[[0, 0, 0, 0, 0, 0] for a in agents] for s in steps]
velocity_error = [[[np.array([0,0]), np.array([0,0]), np.array([0,0]), np.array([0,0]), np.array([0,0]), np.array([0,0])] for a in agents] for s in steps]
T = 0.1
kp = 0.1
kv = 0.1
B = 0

for step in steps:
    # Calcul distanta
    for i in range(len(agents)):
        for j in range(len(agents)):
            distance_error[step][i][j] = abs(d(agents[i], agents[j]) - goal[i][j])
            velocity_error[step][i][j] = abs(np.array(vAgents[i]) - np.array(vAgents[j]))
    # Simulare step
    rand_agent = rnd.randint(0, len(agents) - 1)
    for i in range(len(agents)):
        positions[i].append(agents[i])
        u = 0
        v = 0
        a = np.array(agents[i][:-1])
        va = np.array(vAgents[i])
        for j in [rand_agent]:
            b = np.array(agents[j][:-1])
            vb = np.array(vAgents[j])
            if goal[i][j] > 0:
                u =  u + (1-B) * (a - b + 2 * (d(a, b) - goal[i][j]) / d(a, b) * (a - b)) * goal[i][j]
                if d(va, vb) == 0:
                    v = v
                else:
                    v =  v + (1-B) * 2 * (d(va, vb)) / d(va, vb) * (va - vb) * goal[i][j]
        comanda = - kp * u - kv * v
        # Aplicare comanda
        agents[i] = list((np.array(agents[i][:-1]) + T * np.array(vAgents[i]))) + [agents[i][2]]
        vAgents[i] = list(np.array(vAgents[i]) + T * comanda)

# Afisare traseu
for i in range(len(positions)):
    pos = positions[i]
    x_poz = [p[0] for p in pos]
    y_poz = [p[1] for p in pos]
    plt.plot(x_poz, y_poz, color = agents[i][2])
plt.suptitle("Traseu agenti")
plt.show()

# Afisare pozitie finala
for i in range(len(agents)):
    for j in range(len(agents)):
        if goal[i][j] > 0:
            DrawLinesAgents(agents[i], agents[j])
ShowAgents("Pozitia finala")

