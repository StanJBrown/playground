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

    def add_input_nodes(self, tree):
        # pdb.set_trace()
        index = 0
        input_nodes_len = len(self.config["input_nodes"])
        term_nodes_len = len(tree.term_nodes)
        inputs = randint(input_nodes_len, term_nodes_len)

        print "input_nodes_len: " + str(input_nodes_len)
        print "term_nodes_len: " + str(term_nodes_len)
        print "inputs: " + str(inputs)

        while inputs != 0:
            print "INPUT!!"
            # get random terminal node
            term_node_index = randint(0, len(tree.term_nodes) - 1)
            term_node = tree.term_nodes[term_node_index]
            # print "term_index: " + str(term_node_index)
            # print "term_node: " + str(term_node.value)

            # print("\nPROGRAM STACK!")
            # for block in tree.program:
            #     self.tree_parser._print_node(block)
            # print("")

            # get linked node and also which branch the term node belongs
            linked_node = tree.get_linked_node(term_node)
            # print "linked_node: " + str(linked_node.name)
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

    def full_method(self, tree):
        # setup
        tree.root = self._gen_random_func_node()

        # build tree
        self._full_method_build_tree(tree.root, tree, 0)

        # finish up
        # tree.program = self.tree_parser.post_order_traverse(tree.root)
        # tree.update_func_nodes()
        # tree.size = len(tree.program)
        # tree.depth = self.config["max_depth"]
