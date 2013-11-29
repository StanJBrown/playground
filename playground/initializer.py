#!/usr/bin/env python
import pdb
from random import randint

from playground.tree import Tree
from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.tree import TreeNodeBranch
from playground.tree import TreeParser


class TreeInitializer(object):
    def __init__(self, config):
        self.config = config
        self.tree_parser = TreeParser()

    def _gen_random_func_node(self):
        index = randint(0, len(self.config["function_nodes"]) - 1)
        node = self.config["function_nodes"][index]
        func_node = TreeNode(node["type"], name=node["name"])
        return func_node

    def _gen_random_term_node(self):
        index = randint(0, len(self.config["terminal_nodes"]) - 1)
        node = self.config["terminal_nodes"][index]
        term_node = TreeNode(
            node["type"],
            name=node.get("name", None),
            value=node.get("value", None)
        )
        return term_node

    def _gen_input_node(self, index):
        node = self.config["input_nodes"][index]
        input_node = TreeNode(node["type"], name=node.get("name", None))
        return input_node

    def _full_method_gen_new_node(self, tree, depth):
        if depth + 1 == self.config["max_depth"]:
                term_node = self._gen_random_term_node()
                tree.term_nodes.append(term_node)
                tree.size += 1
                tree.depth = self.config["max_depth"]
                return term_node
        else:
                func_node = self._gen_random_func_node()
                tree.func_nodes.append(func_node)
                tree.size += 1
                return func_node

    def _full_method_build_tree(self, node, tree, depth):
        if depth <= self.config["max_depth"]:
            if node.node_type == TreeNodeType.UNARY_OP:
                # value
                value_node = self._full_method_gen_new_node(tree, depth)
                node.value_branch = value_node

                self._full_method_build_tree(value_node, tree, depth + 1)

            elif node.node_type == TreeNodeType.BINARY_OP:
                # left
                left_node = self._full_method_gen_new_node(tree, depth)
                node.left_branch = left_node

                self._full_method_build_tree(left_node, tree, depth + 1)

                # right
                right_node = self._full_method_gen_new_node(tree, depth)
                node.right_branch = right_node

                self._full_method_build_tree(right_node, tree, depth + 1)

    def _add_input_nodes(self, tree):
        index = 0
        input_nodes_len = len(self.config["input_nodes"])
        term_nodes_len = len(tree.term_nodes)

        start = input_nodes_len
        end = 0
        if term_nodes_len / 4 > input_nodes_len:
            end = term_nodes_len / 4
        elif term_nodes_len / 3 > input_nodes_len:
            end = term_nodes_len / 3
        elif term_nodes_len / 2 > input_nodes_len:
            end = term_nodes_len / 2
        else:
            end = term_nodes_len
        inputs = randint(start, end)

        while inputs != 0:
            # get random terminal node
            term_node_index = randint(0, len(tree.term_nodes) - 1)
            term_node = tree.term_nodes[term_node_index]

            # get linked node and also which branch the term node belongs
            linked_node = tree.get_linked_node(term_node)
            branch = linked_node.has_value_node(term_node)

            # get input node
            input_node = self._gen_input_node(index)

            # replace term node with input node
            if branch == TreeNodeBranch.VALUE:
                linked_node.value_branch = input_node
            elif branch == TreeNodeBranch.LEFT:
                linked_node.left_branch = input_node
            elif branch == TreeNodeBranch.RIGHT:
                linked_node.right_branch = input_node
            tree.term_nodes.remove(term_node)
            tree.input_nodes.append(input_node)

            # increment index
            index += 1
            if index == len(self.config["input_nodes"]) - 1:
                index = 0

            # increment inputs modified
            inputs -= 1

        # finish up
        tree.update_program()  # <- VERY IMPORTANT

    def full_method(self, tree):
        print "FULL-> " + str(id(tree))
        # setup
        tree.root = self._gen_random_func_node()

        # build tree
        self._full_method_build_tree(tree.root, tree, 0)
        tree.update_program()

        # add input nodes
        self._add_input_nodes(tree)
