# playground.benchmark.analyzer

**Functions**:
- parse_data(fp)
- summarize_population(population, summary)
- summarize_evaluation(evaluation, summary)
- summarize_crossover(crossover, summary)
- summarize_mutation(mutation, summary)
- summarize_selection(selection, summary)
- summarize_data(fp)
- plot_summary_graph(data, labels, field_key, **kwargs)
- plot_summary(data, labels, fig_title=None)



## parse_data(fp)
Parse data file, the raw file is assumed to have file extension
'.dat', though you may compress the file with zip. (i.e. the function also
accepts '.zip')


    Args:

        fp (str):
            file path to parse data. Raw data file must have extension '.dat'.
            a zipped file is also acceptable

    Returns:

        list of dict objects


## summarize_population(population, summary)
Summarize `population` dict and appends the result to `summary` dict. This
function expects the following keys from `population` and `summary`:

- generation
- best_score
- best_individual


    Args:

        population (dict):
            population to be summarized

        summary (dict):
            results from summary to be added to


## summarize_evaluation(evaluation, summary)
Summarize `evaluation` dict and appends the result to `summary` dict. This
function expects the following keys from `evaluation` and `summary`:

- cache_size
- diversity
- matched_cache
- trees_evaluated
- tree_nodes_evaluated


    Args:

        evaluation (dict):
            evaluation to be summarized

        summary (dict):
            results from summary to be added to


## summarize_crossover(crossover, summary)
Summarize `crossover` dict and appends the result to `summary` dict. This
function expects the following keys from `crossover` and `summary`:

- crossovers
- no_crossovers
- instances
- crossover_method["success"]
- crossover_method["failed"]
- crossover_method["frequency"]

*Note*: crossover_method is the actual method name (e.g. "POINT_CROSSOVER")


    Args:

        crossover (dict):
            crossover to be summarized

        summary (dict):
            results from summary to be added to


## summarize_mutation(mutation, summary)
Summarize `mutation` dict and appends the result to `summary` dict. This
function expects the following keys from `mutation` and `summary`:

- mutations
- no_mutations
- instances
- mutation_method["success"]
- mutation_method["failed"]
- mutation_method["frequency"]

*Note*: mutation_method is the actual method name (e.g. "POINT_MUTATION")


    Args:

        mutation (dict):
            mutation to be summarized

        summary (dict):
            results from summary to be added to


## summarize_selection(selection, summary)
Summarize `selection` dict and appends the result to `summary` dict. This
function expects the following keys from `selection` and `summary`:

- method
- selection_method["selected"]

*Note*: selection_method is the actual method name (e.g. "ROULETTE_SELECTION")


    Args:

        selection (dict):
            selection to be summarized

        summary (dict):
            results from summary to be added to


## summarize_data(fp)
Is a wrapper function that performs the following summarization in one go:

- population
- evaluation
- selection
- crossover
- mutation


    Args:

        fp (str):
            file path to data to be summarized


    Returns:

        dictionary:
            population
                generation
                best_score
                best_individual

            evaluation
                cache_size
                diversity
                matched_cache
                trees_evaluated
                tree_nodes_evaluated

            crossover
                crossvers
                no_crossovers

            mutation
                mutations
                no_mutations

            selection



## plot_summary_graph(data, labels, field_key, **kwargs)
Creates a summary scatter plot.

    Args:

        data (list of dict):
            data to be plotted, expects a list of dictionary containing
            generation statistics per dict

        lables (list of str):
            labels for the series of data to be plotted

        field_key (str):
           dictionary key to plot against generation, expects a string of the
           form "population.best_score"

        **kwargs:
            kwargs["fignum"] (int):
                i-th figure number

            kwargs["sharex"] (matplotlib.axes)[default=None]:
                x-axis to share plot with

            kwargs["show_legend"] (bool)[default=False]:
                show lengend

            kwargs["ylabel"] (str):
                set y-axis lable

            kwargs["ydiff"] (float)[default=10]:
                the extra y-range


    Return:

        plot axis (matplotlib.axes)


## plot_summary(data, labels, fig_title=None)
Wrapper function that plots multiple summary scatter plots, with generation against:

- population.best_score
- evaluation.diversity
- evaluation.cache_size
- evaluation.trees_evaluated
- evaluation.tree_nodes_evaluated


    Args:

        data (list of dict):
            data to be plotted, expects a list of dictionary containing
            generation statistics per dict

        lables (list of str):
            labels for the series of data to be plotted

        fig_title (str)[default=None]:
            figure title
