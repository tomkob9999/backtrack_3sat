
**Title: A Space-Efficient 3-SAT Solver via 2-SAT Clause Conversion and Backtrack DFS**

**Overview:**
This article presents a novel approach to solving 3-SAT problems by reducing each 3-SAT clause into 2-SAT lines and using a depth-first search (DFS) traversal with early pruning and minimal space usage. The solver avoids full clause expansion or brute-force enumeration. Instead, it explores a binary path space while retaining only the currently active path, using just **O(2n)** space for $n$ clauses and skipping infeasible branches upon detecting unsatisfiability in partial assignments.

---

**1. Background and Motivation**
The 3-SAT problem is NP-complete, and brute-force exploration of all $2^n$ truth assignments is infeasible for large $n$. While many solvers focus on implication graphs or clause learning, our approach leverages:
- Local clause simplification (3-SAT to 2-SAT transformation per path)
- Dynamic pruning of the search tree when partial clauses become unsatisfiable
- Fast detection of satisfying paths without tracking full search state

This enables a clean and practical DFS traversal that uses only 2-dimensional linear data structures.

---

**2. Clause Transformation: 3-SAT to Binary Forks**
Each 3-SAT clause \((a \lor b \lor c)\) is converted into two options:
- A 2-literal clause \((a \lor b)\)
- A 1-literal fallback \((c)\)

This reflects the logical equivalence that if \((a \lor b)\) is false, then \(c\) must be true. Thus, for each 3-SAT clause, we define a **binary choice**:
```python
[(a, b), (c,)]
```
A full 3-SAT problem becomes a list of such binary forks, creating a binary decision tree with depth equal to the number of clauses.

---

**3. DFS Traversal of the Decision Tree**
The solver performs DFS over this binary structure:
- At each level, one of the two clause forms is appended to the current path
- The path is incrementally validated as a 2-SAT instance
- If the partial path becomes UNSAT, it is immediately pruned
- If a complete path is reached and it is SAT, the solver terminates

This enables early backtracking and drastically reduces the number of full paths explored.

---

**4. Space Complexity: Only O(2n)**
Instead of storing the full binary tree or all possible variable states, the solver only keeps:
- The active path of clause choices (depth $\leq n$)
- A simple 2-SAT clause list to validate each partial assignment

This yields a memory footprint of only $O(2n)$ in total: linear in clause count, not exponential.

---

**5. 2-SAT Checking and Short-Circuiting**
A key component is the ability to check 2-SAT satisfiability **incrementally**. We use a compact structure that supports:
- Initial evaluation of a base 2-SAT clause set
- Fast checking when adding a new clause
- Short-circuit return when a conflict is detected

This enables immediate skipping of invalid branches without needing to restart the solver or recalculate global state.

---

**6. Termination Conditions**
- The solver **terminates early** when it finds a full path that satisfies all clauses
- The solver **skips** any subtree rooted at an unsatisfiable partial path
- If no SAT path is found, the solver concludes the problem is UNSAT

---

**7. Conclusion**
This space-efficient 3-SAT solver combines local clause reduction with backtracking DFS and incremental 2-SAT checking. It avoids the complexity of full implication graphs or full state expansion, making it a practical tool for SAT evaluation in constrained environments.

> **The binary search tree of clause forks is never built explicitly — it is walked intelligently using DFS with structural awareness and bounded memory.**
