# mutation
`mutation` contains mutation operators that form part of the Genetic
Programming process. It can currently perform the following mutation methods
on a Tree.

    - Point mutation
    - Hoist mutation
    - Subtree mutation
    - Shrink mutation
    - Expand mutation


    Class:
        - GPTreeMutation



## GPTreeMutation(object)
`GPTreeMutation` class contains mutation methods for Genetic Programming.

    Attributes:

        config (dict):
            Configuration for the whole process.

        recorder (object):
            Object that records the search process.

        tree_generator (TreeInitializer):
            Tree generator

        method (str):
            Mutation method being used for mutation.

        index (int):
            Mutation index point.

        mutation_probability (float):
            Mutation probability threshold to perform mutation.

        random_probability (float):
            Random probability.

        mutated (bool):
            Boolean to denote if trees have been mutated.


    Constructor Arguments:

        config (dict):
            Configuration for the whole process.

        **kwargs:

            recorder (object):
                Object that records the search process.



### point_mutation(tree, mutation_index=None)
Performs point mutation in-place.

    Args:

        tree (Tree):
            Tree to be mutated.

        mutation_index (int):
            Optional argument to set the mutation pivot point.


### hoist_mutation(tree, mutation_index=None)
Performs hoist mutation in-place.

    Args:

        tree (Tree):
            Tree to be mutated.

        mutation_index (int):
            Optional argument to set the mutation pivot point.


### subtree_mutation(tree, mutation_index=None)
Performs subtree mutation in-place.

    Args:

        tree (Tree):
            Tree to be mutated.

        mutation_index (int):
            Optional argument to set the mutation pivot point.


### shrink_mutation(tree, mutation_index=None)
Performs shrink mutation in-place.

    Args:

        tree (Tree):
            Tree to be mutated.

        mutation_index (int):
            Optional argument to set the mutation pivot point.


### expand_mutation(tree, mutation_index=None)
Performs expand mutation in-place.

    Args:

        tree (Tree):
            Tree to be mutated.

        mutation_index (int):
            Optional argument to set the mutation pivot point.


### mutation(tree)
General mutation method that performs a mutation method based on the settings
in `GPTreeMutation.config["mutation"]["method"]`.

    Args:

        tree (Tree):
            Tree to be mutated.

    Raises:

        RuntimeError if `GPTreeMutation.config["mutation"]["method"]` is
        unimplemented.
