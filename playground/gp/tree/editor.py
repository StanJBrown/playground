#!/usr/bin/env python2
from playground.gp.tree import TreeNodeType


def simplify(node, functions):
    try:
        if node.arity == 1:
            func = functions.get_function(node.name)

            # simplify
            node.value = func(node.branches[0].value)

            node.node_type = TreeNodeType.CONSTANT
            node.name = None

        elif node.arity == 2:
            func = functions.get_function(node.name)

            # simplify
            node.value = func(node.branches[0].value, node.branches[1].value)

            node.node_type = TreeNodeType.CONSTANT
            node.name = None

        else:
            raise RuntimeError(
                "Simplify does not support arity of {0}!".format(node.arity)
            )
    except:
        pass


def prune(node, functions):
    node.node_type = TreeNodeType.CONSTANT
    node.name = None
    node.value = 0.0
    node.branches = None


def substitute(node, functions):
    node.node_type = TreeNodeType.CONSTANT
    node.name = None
    node.value = 0.0
    node.branches = None


symreg_edit_rules = {
    "ADD": {
        "CONTAINS_ZERO": simplify,
        "INPUTS_ONLY": None,
        "TERMINALS_ONLY": simplify,
        "INPUT_AND_TERMINALS": None
    },

    "SUB": {
        "CONTAINS_ZERO": simplify,
        "INPUTS_ONLY": None,
        "TERMINALS_ONLY": simplify,
        "INPUT_AND_TERMINALS": None
    },

    "MUL": {
        "CONTAINS_ZERO": prune,
        "INPUTS_ONLY": None,
        "TERMINALS_ONLY": simplify,
        "INPUT_AND_TERMINALS": None
    },

    "DIV": {
        "CONTAINS_ZERO": substitute,
        "INPUTS_ONLY": None,
        "TERMINALS_ONLY": simplify,
        "INPUT_AND_TERMINALS": None
    },

    "POW": {
        "CONTAINS_ZERO": simplify,
        "INPUTS_ONLY": None,
        "TERMINALS_ONLY": simplify,
        "INPUT_AND_TERMINALS": None
    },

    "EXP": {
        "CONTAINS_ZERO": simplify,
        "INPUTS_ONLY": None,
        "TERMINALS_ONLY": simplify,
        "INPUT_AND_TERMINALS": None
    },

    "LN": {
        "CONTAINS_ZERO": simplify,
        "INPUTS_ONLY": None,
        "TERMINALS_ONLY": simplify,
        "INPUT_AND_TERMINALS": None
    }
}


def analyze_children(node):
    contains_zero = False
    terminals_only = True
    inputs_and_terminals = False
    inputs_only = False
    inputs_counter = 0

    for child in node.branches:
        if child.is_constant() is False:
            terminals_only = False
            inputs_and_terminals = True
            inputs_counter += 1
        elif child.value == 0.0:
            contains_zero = True

    if inputs_counter == len(node.branches):
        inputs_only = True
        inputs_and_terminals = False

    return (terminals_only, inputs_and_terminals, inputs_only, contains_zero)


def edit(node, functions):
    analysis = analyze_children(node)

    # see if edit rule exists for function node
    if symreg_edit_rules.get(node.name, False):
        action = None
        rules = symreg_edit_rules[node.name]
        terminals_only = analysis[0]
        inputs_and_terminals = analysis[1]
        inputs_only = analysis[2]
        contains_zero = analysis[3]

        # determine what action to take
        if terminals_only:
            action = rules["TERMINALS_ONLY"]
        if inputs_and_terminals:
            action = rules["INPUT_AND_TERMINALS"]
        if inputs_only:
            action = rules["INPUTS_ONLY"]
        if contains_zero:
            action = rules["CONTAINS_ZERO"]

        # perform edit
        if action is not None:
            action(node, functions)


def edit_tree(tree, node, functions, min_depth=2):
    if node and tree.depth > min_depth:
        # traverse children first
        for child in node.branches:
            if child.is_function():
                edit_tree(tree, child, functions)

        # edit node
        edit(node, functions)


def edit_trees(population, functions):
    for individual in population.individuals:
        # print "BEFORE:", individual
        edit_tree(individual, individual.root, functions)
        # print "AFTER:", individual

        individual.update()
        individual.update_program()
        individual.update_term_nodes()
        individual.update_func_nodes()
        individual.update_input_nodes()
        individual.update_tree_info()
