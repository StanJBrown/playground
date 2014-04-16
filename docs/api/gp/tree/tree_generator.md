## TreeGenerator(object)
`TreeGenerator` is responsible for creating an population of `Tree`s used in
the Genetic Programming process. It supports tree intialization using the:

- Full Method
- Grow Method


    Attributes:

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



