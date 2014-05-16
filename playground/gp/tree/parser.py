#!/usr/bin/env python2


class TreeParser(object):
    def post_order_traverse(self, node, stack=None):
        stack = stack if stack is not None else []

        if node.is_terminal() or node.is_input():
            stack.append(node)

        elif node.is_function():
            for value_node in node.branches:
                self.post_order_traverse(value_node, stack)
            stack.append(node)

        return stack

    def parse_tree(self, tree, node, depth=None, stack=None):
        if depth is None and stack is None:
            depth = 0
            stack = []

            tree.size = 0
            tree.depth = 0
            del tree.func_nodes[:]
            del tree.term_nodes[:]
            del tree.input_nodes[:]

        if node.is_terminal():
            tree.size += 1
            tree.term_nodes.append(node)

            stack.append(node)

        elif node.is_input():
            tree.size += 1
            tree.input_nodes.append(node)

            stack.append(node)

        elif node.is_function() or node.is_class_function():
            for value_node in node.branches:
                self.parse_tree(tree, value_node, depth + 1, stack)

            tree.size += 1
            if node is not tree.root:
                tree.func_nodes.append(node)

            stack.append(node)

        tree.depth = depth if depth > tree.depth else tree.depth
        return stack

    def parse_equation(self, node, eq_str=None):
        eq_str = eq_str if eq_str is not None else ""

        if node.is_terminal():
            if node.name is not None:
                eq_str += node.name
            else:
                eq_str += str(node.value)

        elif node.arity == 1:
            eq_str += "("
            eq_str += node.name
            eq_str += "("
            eq_str = self.parse_equation(node.branches[0], eq_str)
            eq_str += ")"
            eq_str += ")"

        elif node.arity == 2:
            eq_str += "("
            eq_str = self.parse_equation(node.branches[0], eq_str)
            eq_str += " " + node.name + " "
            eq_str = self.parse_equation(node.branches[1], eq_str)
            eq_str += ")"
        else:
            raise RuntimeError("arity of > 2 has not been implemented!")

        return eq_str

    def parse_classification_tree(self, node, tree_str=None):
        tree_str = tree_str if tree_str is not None else ""

        if node.is_terminal():
            tree_str += "{0}[{1}]".format(node.name, node.value)

        elif node.arity == 1:
            child = node.branches[0]

            tree_str += "("
            tree_str += node.name
            tree_str += "("
            tree_str = self.parse_classification_tree(child, tree_str)
            tree_str += ")"
            tree_str += ")"

        elif node.arity == 2:
            child_1 = node.branches[0]
            child_2 = node.branches[1]

            tree_str += "("
            tree_str = self.parse_classification_tree(child_1, tree_str)
            tree_str += " {0}[{1}][{2}] ".format(
                node.name,
                node.class_attribute,
                node.value
            )
            tree_str = self.parse_classification_tree(child_2, tree_str)
            tree_str += ")"

        else:
            raise RuntimeError("arity of > 2 has not been implemented!")

        return tree_str

    def tree_to_dict(self, tree, node, results=None):
        if results is None:
            results = {
                "id": str(id(tree)),
                "program": []
            }

        # traverse tree
        if node.is_terminal() or node.is_input():
            if node.name is not None:
                results["program"].append({
                    "type": node.node_type,
                    "name": node.name
                })
            else:
                results["program"].append({
                    "type": node.node_type,
                    "value": node.value
                })

        elif node.is_function():
            for value_node in node.branches:
                self.tree_to_dict(tree, value_node, results)

            if node is tree.root:
                results["program"].append({
                    "root": True,
                    "type": node.node_type,
                    "arity": node.arity,
                    "name": node.name
                })
            else:
                results["program"].append({
                    "type": node.node_type,
                    "arity": node.arity,
                    "name": node.name
                })

        return results
