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

        population (class):
            `population` is an instance of Population class, it contains all
            the individuals of a population. It is assumed that current number
            of individuals in `population` is less than `max_population`.

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



## play(population, selection, crossover, mutation, config)
`play` encapsulates the complete executional loop of a genetic programming
process.  The needed ingredient are an individual initializer, genetic
operatros such as selection, crossover and mutation, and finally the
configuration for the whole genetic process.

`play` assumes that `config` must contain a key-value of "max_generation" to
indicate the max number of generations to run.


    Args:

        population (class):
            `population` is an instance of Population class, it contains all
            the individuals of a population.

        selection (class):
            `selection` assumes a selection class be it `playground`'s own
            built-in or a custom one. The only requirement is that `selection`
            must contain a method called `select()` that returns a `Population`
            class of selected individuals.

        crossover (class):
            `crossover` assumes a crossover class be it `playground`'s own
            built-in or a custom one. The only requirement is that `crossover`
            must contain a method called `crossover(child_1, child_2)`
            accepting two arguments `child_1` and `child_2` as individuals,
            crossing over the two individuals **in-place**.

        mutation (class):
            `mutation` assumes a mutation class be it `playground`'s own
            built-in or a custom one. The only requirement is that `mutation`
            must contain a method called `mutate(child)`, accepting 1
            individual, and mutating the individual **in-place**.

        config (dict):
            Configuration for the whole process.



## play_multicore(population, functions, evaluator, selection, crossover, mutation, config)
`play_multicore` encapsulates the complete executional loop of a genetic
programming process.  The needed ingredient are an individual initializer,
genetic operatros such as selection, crossover and mutation, and finally the
configuration for the whole genetic process.

`play_multicore` is essentially the same as `play` except the evaluation phase
spawnes multiple processes utilizing multiple cpus the machine may have.

`play_multicore` assumes that `config` must contain a key-value of
"max_generation" to indicate the max number of generations to run.


    Args:

        population (class):
            `population` is an instance of Population class, it contains all
            the individuals of a population.

        selection (class):
            `selection` assumes a selection class be it `playground`'s own
            built-in or a custom one. The only requirement is that `selection`
            must contain a method called `select()` that returns a `Population`
            class of selected individuals.

        crossover (class):
            `crossover` assumes a crossover class be it `playground`'s own
            built-in or a custom one. The only requirement is that `crossover`
            must contain a method called `crossover(child_1, child_2)`
            accepting two arguments `child_1` and `child_2` as individuals,
            crossing over the two individuals **in-place**.

        mutation (class):
            `mutation` assumes a mutation class be it `playground`'s own
            built-in or a custom one. The only requirement is that `mutation`
            must contain a method called `mutate(child)`, accepting 1
            individual, and mutating the individual **in-place**.

        config (dict):
            Configuration for the whole process.
