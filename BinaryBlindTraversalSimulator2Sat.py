# New Incremental 2-SAT version

from typing import List, Tuple
from collections import defaultdict

class BinaryBlindTraversalSimulator2Sat:

    # New Incremental 2-SAT version
    class Inc2SAT:
        def __init__(self):
            self.current_clauses = []
            self.graph = defaultdict(list)
            self.rev_graph = defaultdict(list)
            self.variables = set()
            self.raw_variables = set()
            # self.state = False
            
        def is_sat(self, clauses):
            # print("is_sat() clauses", clauses)
            # print("is_sat() self.current_clauses", self.current_clauses)
        
            def add_implication(u: int, v: int):
                self.graph[u].append(v)
                self.rev_graph[v].append(u)
            
            if len(clauses) == len(self.current_clauses) and all([clauses[i] == c for i, c in enumerate(self.current_clauses)]):
                # print("Identical", clauses)
                return True
                
            if len(clauses) == len(self.current_clauses) + 1 and all([clauses[i] == c for i, c in enumerate(self.current_clauses)]):
                # print("Hello 1", clauses)
                clause = clauses[-1]
                if len(clause) == 1:
                    a = clause[0]
                    a, b = a, a
                else:
                    a, b = clause
                return_false = True if abs(a) not in self.raw_variables or abs(b) not in self.raw_variables else False
                # print("return_false", return_false)
                add_implication(-a, b)
                add_implication(-b, a)
                self.variables.update([abs(a), abs(b)])
                self.raw_variables.add(abs(a))
                self.raw_variables.add(abs(b))
                self.current_clauses.append(clause)
                if return_false:
                    return True
            else:
                # print("Hello 2", clauses)
                self.current_clauses = [c for c in clauses]
                self.graph = defaultdict(list)
                self.rev_graph = defaultdict(list)
                self.variables = set()
    
        
            for clause in clauses:
                if len(clause) == 1:
                    a = clause[0]
                    a, b = a, a
                else:
                    a, b = clause
                add_implication(-a, b)
                add_implication(-b, a)
                self.variables.update([abs(a), abs(b)])
                self.raw_variables.add(abs(a))
                self.raw_variables.add(abs(b))
        
            visited = set()
            order = []
        
            def dfs(u):
                visited.add(u)
                for v in self.graph[u]:
                    if v not in visited:
                        dfs(v)
                order.append(u)
        
            for var in self.variables:
                for v in (var, -var):
                    if v not in visited:
                        dfs(v)
        
            component = {}
            def reverse_dfs(u, label):
                component[u] = label
                for v in self.rev_graph[u]:
                    if v not in component:
                        reverse_dfs(v, label)
        
            for u in reversed(order):
                if u not in component:
                    reverse_dfs(u, u)
        
            for var in self.variables:
                if component.get(var) == component.get(-var):
                    return False
            return True
    
    # def __init__(self, binary_info: List[List[Tuple[int, ...]]]):
    def __init__(self, three_sat):
        # self.bi = binary_info  # bi[i] = [left_clause, right_clause]
        binary_info = [[(a, b), (c,)] for a, b, c in three_sat]
        self.bi = binary_info  # bi[i] = [left_clause, right_clause]
        # print("binary_info", binary_info)
        self.depth = len(binary_info)
        self.skip_prefixes = set()

        self.inc2sat = BinaryBlindTraversalSimulator2Sat.Inc2SAT()
    
    # def simulate_check(self, path: List[Tuple[int, ...]]) -> bool:
    def simulate_check(self, path):
        # return BinaryBlindTraversalSimulator2Sat.is_2sat_satisfiable(path)
        return self.inc2sat.is_sat(path)

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
    # non-incremental 2-SAT
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


# # SAT
print("  =============")
print("TEST SAT")
clauses_set =  [
    [(-4, 1, 3), (-4, -3, -2), (-4, -3, -1), (-4, -2, 3), (-4, -2, 3), (-3, 1, 4), (-3, -2, 4), (-3, 1, 2), (-4, 1, 2), (-3, -2, -1), (-4, 1, 2), (-2, 1, 4), (1, 3, 4), (-4, -1, 3), (-3, -1, 2), (1, 2, 4), (-2, -1, 4), (-2, 3, 4), (-3, -2, 4), (-3, 1, 2)],
    [(-4, -3, -2), (-4, 1, 3), (-1, 3, 4), (-3, 2, 4), (1, 2, 4), (-4, 1, 3), (-4, -3, -2), (-4, -3, -2), (1, 3, 4), (1, 2, 3), (-3, -2, -1), (-3, -2, 4), (-3, 1, 4), (-4, 1, 3), (-4, 2, 3), (-4, -2, -1), (-3, 2, 4), (-4, -3, -2), (-4, -3, -2), (-4, -2, 3)],
    [(-1, 2, 4), (-2, -1, 4), (-3, -2, -1), (-1, 2, 4), (-2, -1, 4), (2, 3, 4), (-3, 2, 4), (-3, -1, 2), (-3, 2, 4), (2, 3, 4), (-4, -2, -1), (-2, -1, 3), (-3, 2, 4), (-3, 1, 4), (-4, -2, -1), (2, 3, 4), (-3, -1, 2), (-4, -2, 3), (-3, -1, 4), (-1, 3, 4)],
    [(-4, -3, 2), (-1, 2, 3), (-3, -2, 1), (-2, 3, 4), (-4, -3, 2), (-2, 1, 4), (-4, -3, -2), (-2, 1, 3), (-2, -1, 4), (-4, -3, 2), (-3, -1, 2), (-4, -3, 1), (-4, 1, 3), (-2, -1, 3), (-3, -1, 2), (-4, -1, 2), (-2, 1, 4), (-3, -2, -1), (-1, 2, 3), (-4, -3, -1)],
    [(-4, -3, 2), (1, 2, 3), (-4, -3, 2), (-4, -2, -1), (-3, -2, 4), (-2, 1, 3), (-3, -2, -1), (-4, -1, 3), (-4, 1, 3), (-1, 2, 3), (-3, -1, 2), (-3, 2, 4), (1, 2, 3), (-2, 3, 4), (1, 3, 4), (-3, 1, 4), (-3, -2, -1), (1, 2, 4), (-4, 1, 2), (-4, -1, 2)],
    [(-3, 1, 2), (-2, 1, 3), (2, 3, 4), (-4, 1, 2), (-2, 1, 4), (-3, -1, 2), (1, 3, 4), (-4, 2, 3), (-4, -2, 3), (-4, -3, 2), (-3, 1, 2), (-4, -1, 2), (-4, -3, -2), (-2, -1, 3), (1, 2, 4), (-1, 2, 4), (-4, 2, 3), (-2, 1, 3), (-4, -2, -1), (-2, -1, 3)],
    [(2, 3, 4), (-3, -2, 1), (-3, 2, 4), (-4, -3, -1), (-2, 1, 3), (-2, -1, 3), (-3, -2, 1), (-2, -1, 4), (-3, 1, 4), (-4, -3, -2), (-1, 2, 3), (-1, 3, 4), (-2, -1, 3), (-3, -1, 4), (-4, -1, 2), (-3, 1, 2), (-2, 1, 4), (1, 2, 4), (-3, 1, 2), (1, 3, 4)],
    [(-4, -1, 3), (1, 3, 4), (-3, -1, 2), (-4, 1, 2), (-1, 2, 3), (2, 3, 4), (1, 3, 4), (-2, -1, 3), (-2, 1, 3), (-1, 3, 4), (-2, -1, 4), (-4, -3, 2), (-3, -2, 1), (-4, 1, 2), (-2, 1, 3), (-2, 3, 4), (-3, 2, 4), (-4, 1, 3), (-3, 1, 4), (-3, -1, 2)],
    [(-4, -3, -2), (1, 2, 3), (-3, -2, 1), (1, 3, 4), (-1, 2, 4), (-3, -1, 2), (1, 3, 4), (-3, 1, 2), (-2, -1, 4), (-4, -2, -1), (2, 3, 4), (-1, 3, 4), (2, 3, 4), (-4, -2, -1), (-3, 2, 4), (1, 3, 4), (-4, -3, 2), (-4, -3, -1), (-4, -3, 1), (-4, -3, -1)],
    [(-3, -1, 4), (-3, 1, 2), (-4, -2, 1), (1, 2, 3), (1, 2, 4), (1, 2, 4), (-2, 3, 4), (2, 3, 4), (-4, 1, 3), (1, 3, 4), (-4, -3, 2), (-4, 1, 3), (-4, 1, 2), (-3, -2, -1), (-3, -1, 4), (-2, -1, 3), (-3, -2, -1), (-4, 1, 2), (-4, -3, 2), (-3, -2, 4)],
    [(-3, -1, 2), (-4, 2, 3), (-4, -3, 1), (-3, -1, 2), (-3, -2, 4), (-4, 1, 2), (-3, -2, -1), (-4, -1, 2), (-4, -1, 3), (-3, -2, 4), (-2, 1, 3), (-3, -1, 2), (-3, -2, 1), (-4, -3, 2), (1, 2, 3), (-2, 1, 3), (-2, -1, 3), (-1, 2, 4), (-3, -2, 1), (-3, -1, 2)]
]


# # UNSAT
# clauses_set = [
# [(-6, -3, -1), (1, 3, 6), (-3, 1, 2), (-3, 2, 5), (-4, -2, 1), (-6, -3, 5), (-4, 3, 6), (-6, -2, 3), (-4, 1, 2), (-1, 2, 3), (-4, -2, 6), (-1, 3, 5), (-3, 1, 5), (-2, 1, 4), (-6, -5, 4), (-3, -1, 6), (-5, -3, 1), (2, 4, 5), (-5, -4, 3), (-1, 3, 6)],
# [(-1, 5, 6), (-6, -1, 5), (3, 4, 5), (-2, 4, 6), (-4, 1, 3), (-4, -3, 5), (-6, -5, -4), (-5, 2, 6), (-5, -4, -2), (-3, -2, 4), (-4, 1, 3), (-5, -3, 4), (-6, -5, 3), (-1, 4, 6), (-2, 3, 4), (4, 5, 6), (-6, 2, 3), (-4, 1, 3), (-6, -3, 2), (-3, 1, 4)] ,
# [(-6, -4, 2), (-3, -1, 4), (-3, 1, 4), (3, 5, 6), (-2, 4, 6), (-5, 2, 3), (-6, -1, 4), (-6, -3, -2), (-1, 2, 5), (-6, 1, 5), (-2, 1, 3), (2, 5, 6), (2, 3, 4), (-4, -3, 5), (-3, 5, 6), (-5, 1, 6), (-1, 2, 4), (-5, -4, -1), (-6, -1, 5), (-5, 2, 3)] ,
# [(-4, 2, 6), (2, 4, 5), (-4, -2, 5), (-6, -4, 2), (-5, -2, 6), (-2, 1, 3), (-5, 2, 4), (-3, -2, 1), (-5, 2, 4), (-3, 1, 6), (-2, -1, 3), (-6, -4, -3), (-3, 4, 5), (-5, -4, -3), (-3, 1, 4), (-4, -1, 6), (-6, -5, -1), (-3, 2, 6), (-1, 5, 6), (-3, 5, 6)] ,
# [(-5, -4, -2), (-5, -1, 4), (-5, 2, 6), (-4, -2, 6), (-3, -2, -1), (-6, -1, 3), (1, 3, 5), (-5, -2, -1), (-2, -1, 6), (-5, 1, 3), (-1, 3, 6), (-5, -4, -2), (-6, -4, 5), (-3, 2, 6), (-6, -5, 3), (-3, -2, 4), (-6, -3, 2), (-6, 1, 2), (-2, 1, 5), (-5, -4, 2)] ,
# [(-5, -1, 4), (-6, -4, -1), (-3, 1, 4), (-2, 5, 6), (-4, -3, 1), (-4, -3, -1), (-2, -1, 4), (-6, -3, 2), (-4, -2, 5), (-5, -2, 4), (-5, -4, 3), (-4, 2, 3), (1, 4, 5), (-6, -4, 1), (-5, -3, -1), (-5, 1, 4), (-2, 1, 3), (-1, 5, 6), (-6, -1, 4), (-3, 2, 5)] ,
# [(-3, 2, 4), (-2, 5, 6), (-5, -4, 1), (-5, -3, -1), (-4, 2, 6), (-6, -2, 5), (-6, -2, 3), (-1, 2, 4), (-6, -4, 5), (-1, 3, 6), (-5, -3, -2), (-3, 2, 6), (-6, -1, 3), (4, 5, 6), (1, 4, 6), (-5, 2, 3), (-4, 3, 6), (1, 2, 3), (-6, -4, 5), (-5, -2, 6)] ,
# [(-6, -1, 3), (-6, 4, 5), (-4, 5, 6), (-4, -3, -2), (-2, 1, 3), (-4, 1, 6), (-3, -2, 5), (1, 2, 4), (-6, 1, 2), (2, 3, 6), (-5, 2, 3), (-1, 2, 3), (-4, -3, -1), (-1, 3, 6), (-5, -2, 4), (-2, 3, 4), (-2, 3, 6), (-1, 2, 6), (-4, -3, -1), (-5, -3, -1)] ,
# [(-6, 1, 2), (-3, -2, -1), (-4, 1, 2), (-1, 2, 6), (-1, 3, 5), (-5, 1, 3), (-4, -3, 2), (1, 4, 5), (-3, -1, 2), (-6, -5, 1), (-3, 1, 2), (-5, -2, 3), (1, 2, 4), (1, 4, 5), (-6, -5, 3), (-3, 1, 6), (-6, 3, 5), (-5, -4, 2), (-2, 4, 5), (-4, -2, 1)] ,
# [(-5, -4, 6), (-6, 4, 5), (-4, 3, 5), (-2, -1, 6), (-4, -3, 5), (-4, -3, 1), (-3, 5, 6), (1, 3, 5), (-2, -1, 3), (-5, -3, 4), (-5, -1, 2), (-6, -3, -2), (-5, 1, 3), (-5, -4, -1), (-4, 3, 6), (-5, 1, 6), (-1, 4, 5), (-3, -1, 4), (-1, 2, 6), (-1, 3, 5)] ,
# [(-4, 1, 6), (-2, 1, 3), (-1, 3, 6), (-6, -3, -2), (-4, 3, 5), (-3, 4, 6), (-4, 1, 2), (-1, 3, 4), (-4, 1, 2), (-3, 1, 4), (-6, 2, 3), (-4, -3, -2), (-6, -5, -1), (-4, -3, -1), (1, 2, 4), (-3, 5, 6), (2, 4, 5), (-6, -3, -2), (-6, -2, 3), (1, 4, 6)] ,
# ]

for clauses in clauses_set:
    simulator = BinaryBlindTraversalSimulator2Sat(clauses)
    simulator.traverse()