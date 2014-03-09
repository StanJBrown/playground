#!/usr/bin/env python
from playground.gp.tree.tree_node import TreeNodeType


def simplify(node, functions):
    if node.arity == 2:
        func = functions.get_function(node.name)
        keep = None

        # keep non zero child node
        if node.branches[0] == 0.0:
            keep = node.branches[1]
        else:
            keep = node.branches[0]

        # simplify
        node.node_type = keep.node_type
        node.name = None
        node.value = func(node.branches[0].value, node.branches[1].value)
    else:
        raise RuntimeError(
            "Simplify does not support arity of {0}!".format(node.arity)
        )


def prune(node, functions):
    node.node_type = TreeNodeType.TERM
    node.name = None
    node.value = 0.0


def substitute(node, functions):
    node.node_type = TreeNodeType.TERM
    node.name = None
    node.value = 0.0


symreg_edit_rules = {
    "ADD": {
        "CONTAINS_ZERO": simplify,
        "TERMINALS_ONLY": simplify,
        "INPUT_AND_TERMINALS": None
    },

    "SUB": {
        "CONTAINS_ZERO": simplify,
        "TERMINALS_ONLY": simplify,
        "INPUT_AND_TERMINALS": None
    },

    "MUL": {
        "CONTAINS_ZERO": prune,
        "TERMINALS_ONLY": simplify,
        "INPUT_AND_TERMINALS": None
    },

    "DIV": {
        "CONTAINS_ZERO": substitute,
        "TERMINALS_ONLY": simplify,
        "INPUT_AND_TERMINALS": None
    }
}


def analyze_children(node):
    contains_zero = False
    terminals_only = True
    inputs_and_terminals = False

    for child in node.branches:
        if child.is_terminal() is False:
            terminals_only = False
            inputs_and_terminals = True
        elif child.value == 0.0:
            contains_zero = True

    return (terminals_only, inputs_and_terminals, contains_zero)


def edit(node, functions):
    analysis = analyze_children(node)

    # see if edit rule exists for function node
    if symreg_edit_rules.get(node.name, False):
        action = None
        rules = symreg_edit_rules[node.name]
        terminals_only, inputs_and_terminals, contains_zero = analysis

        # determine what action to take
        if terminals_only:
            action = rules["TERMINALS_ONLY"]
        if inputs_and_terminals:
            action = rules["INPUT_AND_TERMINALS"]
        if contains_zero:
            action = rules["CONTAINS_ZERO"]

        # perform edit
        if action is not None:
            action(node, functions)


def edit_tree(node, functions):
    if node is None:
        return False

    else:
        # traverse children first
        for child in node.branches:
            if child.is_function():
                edit_tree(child, functions)

        # edit node
        edit(node, functions)
