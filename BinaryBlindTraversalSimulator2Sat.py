# Valid Function version

from typing import List, Tuple
from collections import defaultdict

class BinaryBlindTraversalSimulator2Sat:
    # def __init__(self, binary_info: List[List[Tuple[int, ...]]]):
    def __init__(self, three_sat):
        # self.bi = binary_info  # bi[i] = [left_clause, right_clause]
        binary_info = [[(a, b), (c,)] for a, b, c in three_sat]
        self.bi = binary_info  # bi[i] = [left_clause, right_clause]
        self.depth = len(binary_info)
        self.skip_prefixes = set()

    # def simulate_check(self, path: List[Tuple[int, ...]]) -> bool:
    def simulate_check(self, path):
        return BinaryBlindTraversalSimulator2Sat.is_2sat_satisfiable(path)

    def traverse(self) -> bool:
        total = 1 << self.depth  # 2^depth
        i = 0
        while i < total:
            skip = False
            current_path = []
            literal_set = set()
            jump_prefix = None
            for d in range(1, self.depth + 1):
                prefix = i >> (self.depth - d)
                if (d, prefix) in self.skip_prefixes:
                    skip = True
                    break

                bit = (i >> (self.depth - d)) & 1
                clause = self.bi[d - 1][bit]
                current_path.append(clause)
                # print("current_path", current_path)

                # if not self.simulate_check(current_path):
                if (len(clause) == 1 and -clause[0] in literal_set) or not self.simulate_check(current_path):
                    if len(current_path) < self.depth:
                        # print("pruned", current_path)
                        self.skip_prefixes.add((d, prefix))
                        jump_prefix = prefix + 1
                        i = jump_prefix << (self.depth - d)
                    skip = True
                    break
                
                if len(clause) == 1:
                    literal_set.add(clause[0])

            if not skip:
                print(f"✅ Found satisfying full path: {current_path}")
                return True

            if jump_prefix is None:
                i += 1

        print("❌ No satisfying path found.")
        return False

    # def is_2sat_satisfiable(clauses: List[Tuple[int, ...]]) -> bool:
    def is_2sat_satisfiable(clauses):
        graph = defaultdict(list)
        rev_graph = defaultdict(list)
        variables = set()
    
        def add_implication(u: int, v: int):
            graph[u].append(v)
            rev_graph[v].append(u)
    
        for clause in clauses:
            if len(clause) == 1:
                a = clause[0]
                a, b = a, a
            else:
                a, b = clause
            add_implication(-a, b)
            add_implication(-b, a)
            variables.update([abs(a), abs(b)])
    
        visited = set()
        order = []
    
        def dfs(u):
            visited.add(u)
            for v in graph[u]:
                if v not in visited:
                    dfs(v)
            order.append(u)
    
        for var in variables:
            for v in (var, -var):
                if v not in visited:
                    dfs(v)
    
        component = {}
        def reverse_dfs(u, label):
            component[u] = label
            for v in rev_graph[u]:
                if v not in component:
                    reverse_dfs(v, label)
    
        for u in reversed(order):
            if u not in component:
                reverse_dfs(u, u)
    
        for var in variables:
            if component.get(var) == component.get(-var):
                return False
        return True

# Reusing the Incremental2SAT class from previous cell
# Now testing this new integrated traversal class

# Convert 3-SAT to binary form
clauses_3sat = [
    (1, 2, 3),
    (-1, -2, 4),
    (-3, -4, -1),
    (2, 4, 5),
    (-5, -4, -3)
]

# Run traversal with 2-SAT integration
simulator = BinaryBlindTraversalSimulator2Sat(clauses_3sat)
simulator.traverse()