# playground.symreg_test_funcs

**Functions**:
- write_test_data(fp, data)
- generate_random_matrix(bounds, points, decimal_places=2)
- generate_series_matrix(bounds, points, decimal_places=2)
- evaluate_test_function(equation, var_values)
- simple_test_functions(dest, pattern="simple_test_funcs", fext=".dat")
- arabas_et_al_test_functions(dest, pattern="arabas_et_al-f", fext=".dat")
- nguyen_et_al_test_functions(dest, pattern="nguyen_et_al-f", fext=".dat")


## write_test_data(fp, data)
Write test data `data` in csv format to destination `fp`.

    Args:

        fp (str):
            file path to write the data to

        data (list of rows of data):
            data


## generate_random_matrix(bounds, points, decimal_places=2)
Generate random data points.

    Args:

        bounds (list of float):
            boundary to which the random data are to be created

        points (int):
            number of data points to generate

        decimal_places (int)[default=2]:
            limit decimal places of the matrix

    Returns:

        multidimensional list


## generate_series_matrix(bounds, points, decimal_places=2)
Generate data points in series.

    Args:

        bounds (list of float):
            boundary to which the random data are to be created

        points (int):
            number of data points to generate

        decimal_places (int)[default=2]:
            limit decimal places of the matrix

    Returns:

        multidimensional list


## evaluate_test_function(equation, var_values)
Generates response data by evaluating the test function provided by `equation`
and `var_values`.

    Args:

        equation (str):
            equation in string format

        var_values (multidimensional list):
            input data points

    Returns:

        list of output data


## simple_test_functions(dest, pattern="simple_test_funcs", fext=".dat")
Gennerate simple test functions

    Args:

        dest (str):
            path to which the test function data files are outputted

        pattern (str)[default="simple_test_funcs"]:
            form of which the output file names will have

        fext (str)[default=".dat"]:
            file extension


## arabas_et_al_test_functions(dest, pattern="arabas_et_al-f", fext=".dat")
Gennerate test functions from:

> Arabas, J., Michalewicz, Z. & Mulawka, J., 1994. GAVaPS-a genetic algorithm
with varying population size. Proceedings of the First IEEE Conference on
Evolutionary Computation. IEEE World Congress on Computational Intelligence.

    Args:

        dest (str):
            path to which the test function data files are outputted

        pattern (str)[default="arabas_et_al-f"]:
            form of which the output file names will have

        fext (str)[default=".dat"]:
            file extension

## nguyen_et_al_test_functions(dest, pattern="nguyen_et_al-f", fext=".dat")
Gennerate test functions from:

> Uy, N.Q. et al., 2011. Semantically-based crossover in genetic
programming: application to real-valued symbolic regression. Genetic
Programming and Evolvable Machines, 12(2), p.91-119.

    Args:

        dest (str):
            path to which the test function data files are outputted

        pattern (str)[default="arabas_et_al-f"]:
            form of which the output file names will have

        fext (str)[default=".dat"]:
            file extension
