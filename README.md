# 🧭 A* Algorithm Explained (Network and Routing Simulation) + (GUI) [Full Guid]

This document explains how the `AlgoAStar.py` script works.

---

## 1️⃣ Data Structures
- **`Router` class** — Represents a node in the network. Each router has a position `(x, y)`, a name (A, B, C...), and a list of neighbors.
- **Link cost** — The cost isn't simple physical distance; it's inversely proportional to bandwidth (`1000 / throughput`). The higher the throughput (random value), the lower the cost — this biases the algorithm toward choosing the fastest links.

## 📂 File structure
| File | Role |
|---|---|
| `AlgoAStar.py` | Tkinter GUI application that generates a random network of routers and runs the A* algorithm to find the lowest-cost path. |
| `README.md` | Explanation/documentation of the algorithm and simulation behavior (heuristic, data structures, and visualization). |
| `class1.png` | Optional image asset (not required for running the program). |

---

## 2️⃣ The A* Algorithm (Core Logic)
A* searches for the optimal path using an evaluation function:

```text
f(n) = g(n) + h(n)
```

| Term | Meaning |
|---|---|
| **g(n)** | Real accumulated cost from the start node to the current node `n` |
| **h(n)** *(heuristic)* | Estimated remaining cost to reach the destination — the code uses Euclidean distance divided by 1000 |
| **f(n)** | The algorithm prioritizes exploring nodes where this sum is lowest |

```text
Place the initial node in a priority queue (sorted according to f(n) = g(n) + h(n)).
While the queue is not empty Do :
    Remove the node with the smallest f(n) value (the lowest total cost).
    If it is the target then:
        Success
    Else :
        For each neighbor: calculate the traveled cost g(n) and the remaining estimate h(n), then insert them into the priority queue according to their sum of f(n).
```

---

## 3️⃣ How the Simulation Works

### 🏗️ Generation — `generate_network()`
- Places routers randomly.
- Guarantees connectivity (every node is linked to at least one other).
- Adds redundant links to increase complexity.

### ▶️ Execution — `run_astar()`
- Uses a priority queue (`heapq`) for efficient search.
- Updates paths whenever a cheaper route is found.

### 🎨 Visualization — `draw_network()`
- 🔵 **Blue** — Starting point (Node A)
- 🟢 **Green** — Destination (last node)
- 🔴 **Red** — Optimal path found by A*

## ▶️ How to run the program
1. Make sure you have **Python 3** installed.
2. Install nothing else: the script uses **standard libraries** only (`tkinter`, `heapq`, `math`, `random`).
3. Run the script:
   - In a terminal/VSCode terminal, execute:
     ```bash
     python AlgoAStar.py
     ```
   - If your system uses `python3`, try:
     ```bash
     python3 AlgoAStar.py
     ```
4. The window opens:
   - Enter the number of routers (allowed range: **6 to 25**).
   - Click **“Générer le réseau”**.
   - Click **“SIMULER A*”** to compute the path.

### Recommended environment / frameworks
- **Python + Tkinter** (already used in `AlgoAStar.py`) for the GUI.
- A code editor like **VSCode** with the **Python** extension.

### Notes
- On some setups, `tkinter` might not be installed by default (especially on minimal Python installs). If you get an error related to `tkinter`, install the Tk/Tkinter package for your Python distribution.

---
## 4️⃣ class diagram 

![image alt](https://github.com/R1yDev/A-for-Networking-Routing-AI-/blob/725bbf1b062a64bc79767491b49f65f5430e5e2c/class1.png)
[View the Project Report](presentation.pdf)
---

## 5️⃣ Why This Approach Works
A* is ideal for routing because it combines the **correctness of Dijkstra's algorithm** (real link cost) with the **efficiency of a heuristic-guided search** (position-based estimate) — finding the fastest path while limiting the number of nodes explored.
