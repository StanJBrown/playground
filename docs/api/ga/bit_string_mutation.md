# playground.ga.bit_string.mutation

**Classes**:
- BitStringMutation(object)


## BitStringMutation(object)

    Attributes:

        config (dict):
            configuration

        recorder (JSONStore)[default=None]:
            object that stores mutation statistics

        generator (BitStringGenerator):
            bit string generator


        # MUTATION STATISTIC ATTRIBUTES
        method (string):
            mutation method

        index (int):
            mutation index

        mutation_probability (float):
            mutation probability

        random_probability (float):
            generated pseudo random probability

        mutationed (bool):
            boolean to denote whether mutation is successful or not

        before_mutation (str):
            string representation of both `BitString` parents before mutation

        after_mutation (str):
            string representation of both `BitString` parents before mutation


    Constructor:

        BitStringMutation(config, **kwargs)



**Methods**:
- point_mutation(bstr_1, bstr_2, index=None)
- mutate(bstr_1, bstr_2)
- to_dict()



### point_mutation(bstr_1, bstr_2, index=None)
Performs a one point mutation between parents, the **result is both parents
are modified in-place**.

    Args:

        bstr_1 (BitString):
            bit string parent 1

        bstr_2 (BitString):
            bit string parent 2

        index (int)[default=None]:
            mutation index


### mutate(bstr_1, bstr_2)
Performs a mutation method defined in `config["mutation"]["method"]`,
additionally mutation probability is defined in
`config["mutation"]["probability"]`.

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
            - mutation_probability
            - random_probability
            - mutationed
            - before_mutation
            - after_mutation
