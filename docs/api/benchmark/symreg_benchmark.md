# playground.symreg_benchmark

**Functions**:
- gp_benchmark_loop(config)


## gp_benchmark_loop(config)
Genetic Programming benchmark loop.

    Args:

        config (dict):

            config["random_seed"] (int):
                random seed

            config["call_path"] (str):
                path from which the script is executing from

            config["max_population"] (int):
                max population

            # SELECTION
            config["selection"]["method"] (str)

            # CROSSOVER
            config["crossover"]["method"] (str)
            config["crossover"]["probability"] (float)

            # MUTATION
            config["mutation"]["method"] (str)
            config["mutation"]["probability"] (float)

            # MISC
            config["log_path"] (str)[default=False]


    Returns:

        original config
