# functions
`functions` contains function ingredients that a Genetic Programming requires.

    Functions:
        - add_function(left, right)
        - sub_function(left, right)
        - mul_function(left, right)
        - div_function(left, right)
        - pow_function(left, right)

        - cos_function(value)
        - sin_function(value)
        - rad_function(value)
        - ln_function(value)
        - fact_function(value)

    Class:
        - EvaluationError
        - GPFunctionRegistry


## GPFunctionRegistry(object)
`GPFunctionRegistry` acts as an interface to register and obtain functions for
Genetic Programming.

    Attributes:

        functions (dict):
            Dictionary of functions with the function name as key, and the
            reference to the function as the value.

    Constructor Arguments:

        override_defaults (bool):
            By default the `GPFunctionRegistry` class adds a set of default
            functions to be added into the registry, namely:

            - add_function(left, right)
            - sub_function(left, right)
            - mul_function(left, right)
            - div_function(left, right)
            - pow_function(left, right)

            - cos_function(value)
            - sin_function(value)
            - rad_function(value)
            - ln_function(value)
            - fact_function(value)


### register(function_name, function)
Register function and its name into the function registry.

    Args:

        function_name (str):
            Name of the function to be added

        function (function):
            Function to be added


### unregister(function_name)
Unregister function from the function registry.

    Args:

        function_name (str):
            Name of the function to be removed

        function (function):
            Function to be removed


### get_function(function_name)
Obtain function from function registry with the given name in `function_name`.

    Args:

        function_name (str):
            Name of the function to be obtained
