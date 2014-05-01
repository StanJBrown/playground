# playground.gp.tree.tree_generator
During the Genetic Programming search process an initial random population is
needed, this module provides methods to produce the initial random population.

**Classes**:
- TreeGenerator(object)

## TreeGenerator(object)
`TreeGenerator` is responsible for creating an population of `Tree`s used in
the Genetic Programming process. It supports tree intialization using the:

- Full Method
- Grow Method
- Ramped Half and Half Method

For more information on these methods have a look at "_A Field Guide to
Genetic Programming_" by Riccard Poli, Bill Langdon and Nic McPhee.

**Attributes**:

    config (dict):
        configuration

    tree_parser (TreeParser):
        tree parser instance

    tree_evaluator (TreeEvaluator):
        tree evaluator instance


### full_method()
Initializes a single `Tree` using the full method

    Returns:

        A `Tree` object


### grow_method()
Initializes a single `Tree` using the grow method

    Returns:

        A `Tree` object


### generate_tree()
A general method that looks at `config` for which type of tree initialization
should be used. The `config` key expected is "tree_init_method".

    Returns:

        A `Tree` object


### init()
Initializes a population of trees. It looks at `config` for which type of tree
initialization should be used. The `config` key expected is "tree_init_method".

    Returns:

        A `Population` object full of initialized `Tree` objects



