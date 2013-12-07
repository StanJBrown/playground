-- POPULATIONS
CREATE TABLE IF NOT EXISTS populations 
(
    population_id SERIAL,

    generation INT NOT NULL,
    best_score REAL NOT NULL,
    best_individual TEXT NOT NULL,

    PRIMARY KEY (population_id)
);

-- INDIVIDUALS
CREATE TABLE IF NOT EXISTS trees
(
    tree_id SERIAL,

    population_id INT NOT NULL,
    generation INT NOT NULL,
    score REAL NOT NULL,

    size INT NOT NULL,
    depth INT NOT NULL,
    branches INT NOT NULL,

    func_nodes_len INT NOT NULL,
    term_nodes_len INT NOT NULL,
    input_nodes_len INT NOT NULL,

    func_nodes TEXT[] NOT NULL,
    term_nodes TEXT[] NOT NULL,
    input_nodes TEXT[] NOT NULL,

    program TEXT NOT NULL,
    dot_graph TEXT NOT NULL,

    PRIMARY KEY (tree_id)
);

-- SELECTION
CREATE TABLE IF NOT EXISTS selections
(
    selection_id SERIAL,

    method TEXT NOT NULL,
    selected INT NOT NULL,

    PRIMARY KEY (selection_id)
);

-- CROSSOVER
CREATE TABLE IF NOT EXISTS crossovers
(
    crossover_id SERIAL,

    method TEXT NOT NULL,
    crossover_probability REAL NOT NULL,
    random_probability REAL NOT NULL,
    crossovered BOOL NOT NULL,

    PRIMARY KEY (crossover_id)
);

-- MUTATION
CREATE TABLE IF NOT EXISTS mutations
(
    mutation_id SERIAL,

    generation INT NOT NULL,
    method TEXT NOT NULL,
    probability REAL NOT NULL,
    probability_threshold REAL NOT NULL,

    target_id INT NOT NULL,
    mutated BOOL NOT NULL,

    PRIMARY KEY (mutation_id)
);

-- PRIVILEDGES
GRANT ALL PRIVILEGES ON TABLE populations to playground_user;
GRANT ALL PRIVILEGES ON TABLE trees to playground_user;
GRANT ALL PRIVILEGES ON TABLE selections to playground_user;
GRANT ALL PRIVILEGES ON TABLE crossovers to playground_user;
GRANT ALL PRIVILEGES ON TABLE mutations to playground_user;

GRANT USAGE, SELECT ON SEQUENCE populations_population_id_seq TO playground_user;
GRANT USAGE, SELECT ON SEQUENCE trees_tree_id_seq TO playground_user;
GRANT USAGE, SELECT ON SEQUENCE selections_selection_id_seq TO playground_user;
GRANT USAGE, SELECT ON SEQUENCE crossovers_crossover_id_seq TO playground_user;
GRANT USAGE, SELECT ON SEQUENCE mutations_mutation_id_seq TO playground_user;
