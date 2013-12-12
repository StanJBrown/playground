# selection
`selection` contains selection operators that form part of the Genetic
Programming process. It can currently perform the following selection methods.

    - Roulette Wheel Selection
    - Tournament Selection


    Class:
        - Selection



## Selection(object)
`Selection` class contains selection methods for Genetic Programming.

    Attributes:

        config (dict):
            Configuration for the whole process.

        recorder (object):
            Object that records the search process.

        method (str):
            Selection method being used for select.

        selected (int):
            Resultant individuals selected.

        new_population (Population):
            Newly selected population of individuals.


    Constructor Arguments:

        config (dict):
            Configuration for the whole process.

        **kwargs:

            recorder (object):
                Object that records the search process.



### roulette_wheel_selection(population)
Performs roulette wheel selection on `population`.

    Args:

        population (Population):
            Population to be selected from.

    Returns:

        Newly selected population of individuals.


### tournament_selection(population)
Performs tournament selection on `population`. By default the tournament size
is 2, else if `Selection.config["selection"]["tournament_size"]` is set, that
value will be used for the tournament size instead.

    Args:

        population (Population):
            Population to be selected from.

    Returns:

        Newly selected population of individuals.


### select(population)
General select method that performs a selection method based on the settings in
`Selection.config["selection"]["method"]`.

    Args:

        population (Population):
            Population to be selected from.

    Returns:

        Newly selected population of individuals.

    Raises:

        RuntimeError if `Selection.config["selection"]["method"]` is unimplemented.
