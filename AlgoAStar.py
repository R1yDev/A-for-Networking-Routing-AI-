import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import math
import heapq

class Router:
    """Représente un routeur dans le réseau."""
    #on utiliser "self pour appeler l’objet courant de la classe  
    def __init__(self, id, label, x, y):
        self.id = id # le numéro unique d'un routeur pour stocker/chercher rapidement les coûts 
        self.label = label #(A,B,C ...):
        self.x = x
        self.y = y
        self.neighbors = []  # Liste de tuples (Routeur, bandwidth/débit, couts)

class SimulationAStar:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation A* - Routage Réseau")
        self.root.geometry("1100x750")

        # Variables de données
        self.nodes = [] #les routeurs
        self.edges = [] #liste de toutes les liaisons (liens)
        self.path = [] #les chemains
        
        self.setup_ui()

    def setup_ui(self):
        """Initialise l'interface utilisateur."""
        # --- Barre supérieure (Contrôles) ---
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(top_frame, text="Nombre de routeurs (6-25) :").pack(side=tk.LEFT, padx=5)
        self.entry_count = tk.Entry(top_frame, width=5) 
        self.entry_count.insert(0, "10")
        self.entry_count.pack(side=tk.LEFT, padx=5)

        tk.Button(top_frame, text="Générer le réseau", command=self.generate_network, bg="#2c3e50", fg="white").pack(side=tk.LEFT, padx=10)

        # --- Zone principale (Canvas + Logs) ---
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # Canvas pour le dessin
        self.canvas = tk.Canvas(main_frame, width=800, height=600, bg="white", relief=tk.SUNKEN, border=2)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Zone de log
        log_frame = tk.Frame(main_frame)
        log_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        tk.Label(log_frame, text="Journal de l'algorithme :", font=("Arial", 10, "bold")).pack()
        self.log_area = scrolledtext.ScrolledText(log_frame, width=35, height=35, font=("Courier New", 9), bg="#1e272e", fg="#d2dae2")
        self.log_area.pack()

        # --- Barre inférieure (Simulation) ---
        bottom_frame = tk.Frame(self.root, pady=10)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(bottom_frame, text="SIMULER A*", command=self.run_astar, bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=20).pack(side=tk.LEFT, padx=50)
        tk.Button(bottom_frame, text="ANNULER", command=self.reset_highlight, bg="#95a5a6", fg="white", width=20).pack(side=tk.RIGHT, padx=50)

        self.info_label = tk.Label(bottom_frame, text="Générez un réseau pour commencer.", font=("Arial", 10, "italic"))
        self.info_label.pack(pady=5)


    def generate_network(self):
        """Génère aléatoirement un graphe de routeurs."""
        try:
            count = int(self.entry_count.get())
            if not (6 <= count <= 25):
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez saisir un entier entre 6 et 25.")
            return

        self.nodes = []
        self.edges = []
        self.path = []
        self.log_area.delete('1.0', tk.END)
        self.log("Génération d'un nouveau réseau...")

        # 1. Création des nœuds (Positions aléatoires)
        for i in range(count):
            label = chr(65 + i)
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            self.nodes.append(Router(i, label, x, y))

        # 2. Garantie de connectivité (Lier chaque nouveau nœud au plus proche déjà existant)
        for i in range(1, count):
            best_dist = float('inf') # on va init la maill dist avec un nombre inf 
            target = 0  # on va init la distination 
            for j in range(i):
                d = self.get_dist(self.nodes[i], self.nodes[j])
                if d < best_dist:
                    best_dist = d
                    target = j
            self.add_edge(self.nodes[i], self.nodes[target])

        # 3. Ajout de liens supplémentaires pour la complexité
        for i in range(count):
            if random.random() > 0.6:
                target = random.randint(0, count - 1)
                if target != i and not self.are_linked(self.nodes[i], self.nodes[target]):
                    self.add_edge(self.nodes[i], self.nodes[target])

        self.draw_network()
        self.info_label.config(text=f"Réseau prêt. Départ: A, Arrivée: {self.nodes[-1].label}")
    #ajouter des liaisons entre les routeurs (pour chaque routeur possede au moin une liaison).
    def add_edge(self, n1, n2):
        """Crée une liaison/connectivity avec un débit aléatoire."""
        bandwidth = random.randint(10, 1000)
        cost = round(1000 / bandwidth, 2)
        n1.neighbors.append((n2, bandwidth, cost))
        n2.neighbors.append((n1, bandwidth, cost))
        self.edges.append({'n1': n1, 'n2': n2, 'bw': bandwidth, 'cost': cost})

    def are_linked(self, n1, n2):
        return any(nb[0] == n2 for nb in n1.neighbors)


    def get_dist(self, n1, n2):
        return math.sqrt((n2.x - n1.x)**2 + (n2.y - n1.y)**2)

    # ALGORITHME A*

    def heuristic(self, current, goal):
        """
        Calcul de l'heuristique h(n).
        ADMISSIBILITÉ : h(n) <= coût réel.
        Le coût réel minimum d'un lien est 1 (pour 1000 Mbps).
        Ici h(n) = distance / 1000. Comme la distance max est d'environ 1000 pixels,
        h(n) sera toujours <= 1. Elle ne surestime donc jamais le coût d'un saut.
        """
        return self.get_dist(current, goal) / 1000

    def run_astar(self):
        if not self.nodes: return
        self.reset_highlight()
        
        start = self.nodes[0]
        goal = self.nodes[-1]
        
        self.log("--- Lancement de A* ---")
        
        # open_set stocke des tuples (f_score, router_id, router_object)
        # On utilise router_id pour départager les égalités de f_score
        open_set = []
        heapq.heappush(open_set, (0, start.id, start)) # init heapq avec le routeur A (f(n),(id, obj routeur))
        
        came_from = {} #on va stocker les chemains pour faire la presedence 
        g_score = {node.id: float('inf') for node in self.nodes} #on va calculer pour chaque routeur leur g(n) depuis le point de dep et point actuelle
        g_score[start.id] = 0 #point initial
        
        f_score = {node.id: float('inf') for node in self.nodes} #f(n)
        f_score[start.id] = self.heuristic(start, goal)

        closed_set = set()

        while open_set:
            # Récupérer le nœud avec le f_score le plus bas
            current_f, _, current = heapq.heappop(open_set) # recuperer f(n) et le routeur

            if current == goal:
                self.reconstruct_path(came_from, current)
                return

            closed_set.add(current.id)
            self.log(f"Exploration de {current.label} (f={current_f:.2f})")

            for neighbor, bw, cost in current.neighbors: 
                if neighbor.id in closed_set: # skip 
                    continue

                tentative_g = g_score[current.id] + cost
                
                if tentative_g < g_score[neighbor.id]:
                    # Ce chemin est meilleur !
                    came_from[neighbor.id] = current
                    g_score[neighbor.id] = tentative_g
                    h = self.heuristic(neighbor, goal)
                    f = tentative_g + h
                    f_score[neighbor.id] = f
                    
                    if not any(item[1] == neighbor.id for item in open_set):
                        heapq.heappush(open_set, (f, neighbor.id, neighbor))
                    
                    self.log(f" -> Maj {neighbor.label}: g={tentative_g:.1f}, h={h:.1f}, f={f:.1f}")

        messagebox.showinfo("Résultat", "Aucun chemin trouvé.")

    def reconstruct_path(self, came_from, current):
        self.path = [current]
        total_cost = 0
        while current.id in came_from:
            prev = came_from[current.id]
            # Trouver le coût du lien
            for nb, bw, cost in prev.neighbors:
                if nb == current:
                    total_cost += cost
                    break
            current = prev
            self.path.append(current)
        self.path.reverse()
        
        path_str = " -> ".join([n.label for n in self.path])
        self.log(f"CHEMIN TROUVÉ : {path_str}")
        self.log(f"COÛT TOTAL : {total_cost:.2f}")
        self.info_label.config(text=f"Succès ! Coût : {total_cost:.2f}", fg="#27ae60")
        self.draw_network()


    # DESSIN ET IHM


    def draw_network(self):
        self.canvas.delete("all")
        
        # 1. Dessiner les arêtes
        for edge in self.edges:
            n1, n2 = edge['n1'], edge['n2']
            is_in_path = self.is_edge_in_path(n1, n2)
            
            color = "#e74c3c" if is_in_path else "#bdc3c7"
            width = 4 if is_in_path else 1
            
            self.canvas.create_line(n1.x, n1.y, n2.x, n2.y, fill=color, width=width)
            
            # Label débit
            mid_x, mid_y = (n1.x + n2.x)/2, (n1.y + n2.y)/2
            self.canvas.create_text(mid_x, mid_y - 10, text=f"{edge['bw']}Mbps", font=("Arial", 8), fill="#34495e")

        # 2. Dessiner les nœuds
        for i, node in enumerate(self.nodes):
            color = "white"
            if i == 0: color = "#3498db" # Départ
            elif i == len(self.nodes) - 1: color = "#2ecc71" # Arrivée
            
            # Cercle
            r = 15
            self.canvas.create_oval(node.x-r, node.y-r, node.x+r, node.y+r, fill=color, outline="#2c3e50", width=2)
            
            # Croix à l'intérieur
            offset = 6
            self.canvas.create_line(node.x-offset, node.y-offset, node.x+offset, node.y+offset, fill="#2c3e50")
            self.canvas.create_line(node.x+offset, node.y-offset, node.x-offset, node.y+offset, fill="#2c3e50")
            
            # Label texte
            self.canvas.create_text(node.x, node.y - 25, text=node.label, font=("Arial", 10, "bold"))

    def is_edge_in_path(self, n1, n2):
        if not self.path: return False
        for i in range(len(self.path) - 1):
            p1, p2 = self.path[i], self.path[i+1]
            if (p1 == n1 and p2 == n2) or (p1 == n2 and p2 == n1):
                return True
        return False

    def log(self, message):
        self.log_area.insert(tk.END, "> " + message + "\n")
        self.log_area.see(tk.END)

    def reset_highlight(self):
        self.path = []
        self.info_label.config(text="Simulation réinitialisée.", fg="black")
        self.draw_network()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationAStar(root)
    root.mainloop()
