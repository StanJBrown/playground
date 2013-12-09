# play
`play` contains general methods to run a Genetic Programming process.

    Functions:
        - reproduce(population, crossover, mutation, config)
        - play(intializer, selection, crossover, mutation, config)


## reproduce(population, crossover, mutation, config)
`reproduce` is the mating phase of a generation. It is assuemd that the
indivduals chosen to be mated together are already selected in population with
space available for the children to be inputted.

During the reproduction phase two other genetic operators are used, namely the
crossover and mutation operators.

    Args:

        selection (class):
            Similar to intializer, `selection` assumes a selection class be it
            `playground`'s own built-in or a custom one. The only requirement
            is that `selection` must contain a method called `select()` that
            returns a `Population` class of selected individuals.

        crossover (class):
            Similar to intializer, `crossover` assumes a crossover class be it
            `playground`'s own built-in or a custom one. The only requirement
            is that `crossover` must contain a method called
            `crossover(child_1, child_2)` accepting two arguments `child_1` and
            `child_2` as individuals, crossing over the two individuals
            **in-place**.

        mutation (class):
            Similar to intializer, `mutation` assumes a mutation class be it
            `playground`'s own built-in or a custom one. The only requirement
            is that `mutation` must contain a method called `mutate(child)`,
            accepting 1 individual, and mutating the individual **in-place**.

        config (dict): Configuration for the whole process.



## play(initializer, selection, crossover, mutation, config)
`play` encapsulates the complete executional loop of a genetic programming
process.  The needed ingredient are an individual initializer, genetic
operatros such as selection, crossover and mutation, and finally the
configuration for the whole genetic process.

`play` assumes that `config` must contain a key-value of "max_generation" to
indicate the max number of generations to run.


    Args:

        intializer (class):
            Individual initializer class, can be playground's built-in
            initializer class, or a custom one. The only requirement is that it
            must contain a method called `init()` that returns a `Population`
            class full of individuals to be selected, crossed and mutated.

        selection (class):
            Similar to intializer, `selection` assumes a selection class be it
            `playground`'s own built-in or a custom one. The only requirement
            is that `selection` must contain a method called `select()` that
            returns a `Population` class of selected individuals.

        crossover (class):
            Similar to intializer, `crossover` assumes a crossover class be it
            `playground`'s own built-in or a custom one. The only requirement
            is that `crossover` must contain a method called
            `crossover(child_1, child_2)` accepting two arguments `child_1` and
            `child_2` as individuals, crossing over the two individuals
            **in-place**.

        mutation (class):
            Similar to intializer, `mutation` assumes a mutation class be it
            `playground`'s own built-in or a custom one. The only requirement
            is that `mutation` must contain a method called `mutate(child)`,
            accepting 1 individual, and mutating the individual **in-place**.

        config (dict):
            Configuration for the whole process.
