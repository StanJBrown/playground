# population
`population` contains the `Population` class that encapusulates the notion of a
population during an Evolutionary Computational process.

    Classes:
        - Population


## Population(object)
`Population` encapsultes the notion of a population during an Evolutionary
Computational process. It contains attributes such as generation number, best
individuals, as well as the individuals itself in a generation of population.


### Attributes

    config (dict): configuration for the population
    evaluator (class): evaluator class to evaluate population/individuals
    generation (int): integer representing the generation number of the population
    best_top (int): best top individuals to keep
    best_individuals (array of objects): array of best individual objects
    individuals (array of objects): array of individuals in a population


### Constructor Arguments

    config (dict):
        Configuration for population

    evaluator (class):
        Evaluator for the population, can be `playground`'s built-in evaluator
        or a custom one. The only requirement is that it must contain a method
        called `evaluate(individual)` accepting 1 argument for an individual,
        the method should set the `individual`'s own score attrubute in-place
        (i.e.  `individual.score = 0.1`)


### sort_individuals()
Simply sorts the individuals according to the `individual`'s score. By default
it sorts by acending order. The top `Population.best_top` is recorded into
`Population.best_individuals`.


### evaluate_population()
Evaluates the population's individuals (i.e. `Population.individuals`) one by
one using `Population.evaluator`. If an `EvaluationError` exception is detected
the individual will be removed from `Population.individuals`.


### evaluate_individual()
Evaluates an individual using `Population.evaluator`. If an `EvaluationError`
exception is detected the individual will be removed from
`Population.individuals`.
