#!/usr/bin/env python


class TreeParser(object):
    def _print_node(self, node):
        if hasattr(node, "name") and node.name is None:
            print('"{0}{1}"'.format(node.value, id(node)))
        else:
            print('"{0}{1}"'.format(node.name, id(node)))

    def _print_node_label(self, node):
        if hasattr(node, "name") and node.name is None:
            print('{0}{1}[label="{0}"];'.format(node.value, id(node)))
        else:
            print('{0}{1}[label="{0}"];'.format(node.name, id(node)))

    def _print_relation(self, from_node, to_node, node_list):
        from_node_id = None
        to_node_id = None

        if from_node.name is None:
            from_node_id = from_node.value
        else:
            from_node_id = from_node.name

        if to_node.name is None:
            to_node_id = to_node.value
        else:
            to_node_id = to_node.name

        print(
            '"{0}{1}" -> "{2}{3}";'.format(
                from_node_id,
                id(from_node),
                to_node_id,
                id(to_node)
            )
        )

        node_list.append(to_node)

    def _print_tree_structure(self, node, node_list):
        if node.is_function():
            for value_node in node.branches:
                self._print_relation(node, value_node, node_list)
                self._print_tree_structure(value_node, node_list)

    def print_tree(self, root_node):
        node_list = []
        node_list.append(root_node)
        self._print_tree_structure(root_node, node_list)

        for node in node_list:
            self._print_node_label(node)

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
            tree.branches = 1
            tree.open_branches = 1
            del tree.func_nodes[:]
            del tree.term_nodes[:]
            del tree.input_nodes[:]

        if node.is_terminal():
            tree.size += 1
            tree.open_branches -= 1
            tree.term_nodes.append(node)

            stack.append(node)

        elif node.is_input():
            tree.size += 1
            tree.open_branches -= 1
            tree.input_nodes.append(node)

            stack.append(node)

        elif node.is_function():
            for value_node in node.branches:
                self.parse_tree(tree, value_node, depth + 1, stack)

            tree.size += 1
            tree.branches += (node.arity - 1)
            tree.open_branches += (node.arity - 1)
            if node is not tree.root:
                tree.func_nodes.append(node)

            stack.append(node)

        tree.depth = depth if depth > tree.depth else tree.depth
        return stack

    def parse_equation(self, node, eq_str=None):
        eq_str = eq_str if eq_str is not None else ""

        if node.is_terminal() or node.is_input():
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
