# playground.benchmark.analyzer

**Module contents**:
- parse_log(path)
- sort_records_by(attribute, log_jsons, reverse=False)
- parse_general_stats(log_jsons)
- plot_matrix(log_jsons, **kwargs)
- scatterplot_matrix(data, names=[], **kwargs)


## parse_log(path)
Parses the log file assumed to be a JSON file.

    Args:

        path (str):
            full path to log file

    Returns:

        list of JSON objects


## sort_records_by(attribute, log_jsons, reverse=False)
Sort wrapper. It essentially sorts the list of log JSON objects after they
have been parsed via `parse_log(path)`, accordding to the JSON object
attribute.

    Args:

        attribute (str):
            attribute of the JSON object to be sorted

        log_jsons (list of JSONS):
            list of JSON objects from `parse_log(path)`

    Returns:

        sorted list of JSON objects


## parse_general_stats(log_jsons)
Summarize general statistics from list of log JSON objects. It loops through
every log JSON object in `log_jsons` and summarizes:

- best individual
- best score
- run time

    Args:

        log_jsons (list of JSONS):
            list of JSON objects from `parse_log(path)`

    Returns:

        dictionary:
            - best_individuals (list of str)
            - best_scores (list of float)
            - runtimes (list of float)


## plot_matrix(log_jsons, **kwargs)
Wrapper function that performs a pairs plot, or a matrix plot of:

- population size
- crossover probability
- mutation probability
- best score
- runtime

This wrapper prepares and summarizes the above data fields in order for the
matrix plot to be performed.

    Args:

        log_jsons (list of JSONS):
            list of JSON objects from `parse_log(path)`

        **kwargs:

            kwargs["show_plot"] (bool)[default=False]:
                show plot via GUI

            kwargs["save_plot"] (bool)[default=False]:
                save plot

            kwargs["save_path"] (str):
                path to save plot, compulsary if `save_plot` is True

            kwargs["save_format"] (str)[default="png"]:
                image format to be saved


## scatterplot_matrix(data, names=[], **kwargs)
The actual matrix/ pairs plotting function using `matplotlib`.


    Args:

        data (2D list of floats):
            data to be plotted

        names (list of str):
            name or field of data to be plotted, used to label axises


        **kwargs:

            kwargs["figsize"] (tuple)[default=(8, 8)]:
                figure size

            kwargs["facecolor"] (str)[default="white"]:
                plot background color


    Returns:

        matplotlib Fig object
