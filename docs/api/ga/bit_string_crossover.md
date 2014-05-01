# playground.ga.bit_string_crossover

**Classes**:
- BitStringCrossover(object)


## BitStringCrossover(object)

    Attributes:

        config (dict):
            configuration

        recorder (JSONStore)[default=None]:
            object that stores crossover statistics


        # CROSSOVER STATISTIC ATTRIBUTES
        index (int):
            crossover index

        crossover_probability (float):
            crossover probability

        random_probability (float):
            generated pseudo random probability

        crossovered (bool):
            boolean to denote whether crossover is successful or not

        before_crossover (str):
            string representation of both `BitString` parents before crossover

        after_crossover (str):
            string representation of both `BitString` parents before crossover


    Constructor:

        BitStringCrossover(config, **kwargs)



**Methods**:
- uniform_random_index(bstr_1, bstr_2)
- one_point_crossover(bstr_1, bstr_2, index=None)
- crossover(bstr_1, bstr_2)
- to_dict()


### uniform_random_index(bstr_1, bstr_2)
Selects a random index that are shared by both bit string parents.

    Args:

        bstr_1 (BitString):
            bit string parent 1

        bstr_2 (BitString):
            bit string parent 2


    Returns:

        Random index shared by both parents



### one_point_crossover(bstr_1, bstr_2, index=None)
Performs a one point crossover between parents, the **result is both parents
are modified in-place**.

    Args:

        bstr_1 (BitString):
            bit string parent 1

        bstr_2 (BitString):
            bit string parent 2

        index (int)[default=None]:
            crossover index


### crossover(bstr_1, bstr_2)
Performs a crossover method defined in `config["crossover"]["method"]`,
additionally crossover probability is defined in
`config["crossover"]["probability"]`.

    Args:

        bstr_1 (BitString):
            bit string parent 1

        bstr_2 (BitString):
            bit string parent 2



### to_dict()
Converts the `BitStringCrossoer` statistics to dictionary for recording

    Returns:

        Dictionary containing:
            - method
            - index
            - crossover_probability
            - random_probability
            - crossovered
            - before_crossover
            - after_crossover
