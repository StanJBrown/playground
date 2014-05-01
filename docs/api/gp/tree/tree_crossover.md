# playground.gp.tree.tree_crossover
`crossover` contains crossover operators that form part of the Genetic
Programming process. It can currently perform the following crossover methods
on a Tree.

- One point crossover

**Classes**:
- GPTreeCrossover



## TreeCrossover(object)
`GPTreeCrossover` class contains crossover methods for Genetic Programming.

    Attributes:

        config (dict):
            Configuration for the whole process.

        recorder (object):
            Object that records the search process.

        method (str):
            Crossover method being used for crossover.

        index (int):
            Crossover index point.

        crossover_probability (float):
            Crossover probability threshold to perform crossover.

        random_probability (float):
            Random probability.

        crossovered (bool):
            Boolean to denote if trees have been crossovered.


    Constructor Arguments:

        config (dict):
            Configuration for the whole process.

        **kwargs:

            recorder (object):
                Object that records the search process.



### one_point_crossover(tree_1, tree_2, crossover_index=None)
Performs one point crossover in-place on both trees, `tree_1`, `tree_2`. By
default the crossover point is chosen at a random common region, the index is
uniform on both trees.

    Args:

        tree_1 (Tree):
            Tree 1 to be crossovered.

        tree_2 (Tree):
            Tree 2 to be crossovered.

        crossover_index (int):
            Optional argument to set the crossover pivot point.


### crossover(tree_1, tree_2)
General crossover method that performs a crossover method based on the settings in
`GPTreeCrossover.config["crossover"]["method"]`.

    Args:

        tree_1 (Tree):
            Tree 1 to be crossovered.

        tree_2 (Tree):
            Tree 2 to be crossovered.

    Raises:

        RuntimeError if `GPTreeCrossover.config["crossover"]["method"]` is
        unimplemented.
