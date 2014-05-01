# playground.climbing.climbers
This module contains hill climbing algorithms, current it features:

- Hill Climbing
- Steepest Ascent Hill Climbing

**Module contents**:
- hill_climbing(config)
- steepest_ascent_hill_climbing(config)


## hill_climbing(config)

    Args:

        config (dict):

            config is a dictionary containing elements needed for the algorithm

            config["tweak_function"] (function):


            config["eval_function"] (function):


            config["stop_function"] (function):


            config["max_iteration"] (int):



    Returns:

        Tuple containing the best solution and fitness score

        (solution, fitness score)


## steepest_ascent_hill_climbing(config)
