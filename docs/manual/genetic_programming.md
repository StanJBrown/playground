# Genetic Programming
Genetic Programming (GP) is a general combinatorial search, like Genetic
Algorithms (GA) through the evolutionary process, the best solution to the
problem is hoped to have evolved and converge into a desirable optimal
solution.

In GP while the process is similar to GA, GP operates on a different data
structure, instead of a 1 dimensional bit string it operates on a tree
structure. (See image below for an example)

![A tree representing a mathematical equation](images/gp_tree.png)

Playground current supports the current GP genetic operators:
- Selection
    - Roulette wheel selection
    - Tournament selection
- Crossover
    - One point crossover
- Mutation
    - Point mutation
    - Hoist mutation
    - Sub-tree mutation
    - Shrink mutation
    - Expand mutation

# Example

- [Symbolic Regression](../examples/gp-symbolic_regression.md)



