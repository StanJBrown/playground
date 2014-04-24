# config
`config` contains functions that loads a json configuration file into a python
dictionary.

    Functions:
        - load_configuration(config_file)


## load_config(config_file)
Loads the configuration file in JSON format into a python dictionary. If the
json file contains a "data_file" key, `load_config` loads the data file as
well. The data file is assumed to be a CSV file.

    Args:

        config_file (str): config file path

    Returns:

        Dictionary of config
