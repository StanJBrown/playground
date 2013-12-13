#!/usr/bin/env python
from playground.gp_tree.tree_node import TreeNodeType


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
        if node.node_type == TreeNodeType.UNARY_OP:
            # value
            self._print_relation(node, node.value_branch, node_list)
            self._print_tree_structure(node.value_branch, node_list)
        elif node.node_type == TreeNodeType.BINARY_OP:
            # left
            self._print_relation(node, node.left_branch, node_list)
            self._print_tree_structure(node.left_branch, node_list)

            # right
            self._print_relation(node, node.right_branch, node_list)
            self._print_tree_structure(node.right_branch, node_list)

    def print_tree(self, root_node):
        node_list = []
        node_list.append(root_node)
        self._print_tree_structure(root_node, node_list)

        for node in node_list:
            self._print_node_label(node)

    def post_order_traverse(self, node, stack=None):
        stack = stack if stack is not None else []
        n_type = node.node_type

        if n_type == TreeNodeType.TERM or n_type == TreeNodeType.INPUT:
            stack.append(node)

        elif n_type == TreeNodeType.UNARY_OP:
            self.post_order_traverse(node.value_branch, stack)
            stack.append(node)

        elif n_type == TreeNodeType.BINARY_OP:
            self.post_order_traverse(node.left_branch, stack)
            self.post_order_traverse(node.right_branch, stack)
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

        if node.node_type == TreeNodeType.TERM:
            tree.size += 1
            tree.open_branches -= 1
            tree.term_nodes.append(node)

            stack.append(node)

        elif node.node_type == TreeNodeType.INPUT:
            tree.size += 1
            tree.open_branches -= 1
            tree.input_nodes.append(node)

            stack.append(node)

        elif node.node_type == TreeNodeType.UNARY_OP:
            self.parse_tree(tree, node.value_branch, depth + 1, stack)

            tree.size += 1
            if node is not tree.root:
                tree.func_nodes.append(node)

            stack.append(node)

        elif node.node_type == TreeNodeType.BINARY_OP:
            self.parse_tree(tree, node.left_branch, depth + 1, stack)
            self.parse_tree(tree, node.right_branch, depth + 1, stack)

            tree.size += 1
            tree.branches += 1
            tree.open_branches += 1
            if node is not tree.root:
                tree.func_nodes.append(node)

            stack.append(node)

        tree.depth = depth if depth > tree.depth else tree.depth
        return stack

    def parse_equation(self, node, eq_str=None):
        eq_str = eq_str if eq_str is not None else ""
        n_type = node.node_type

        if n_type == TreeNodeType.TERM or n_type == TreeNodeType.INPUT:
            if node.name is not None:
                eq_str += node.name
            else:
                eq_str += str(node.value)

        elif n_type == TreeNodeType.UNARY_OP:
            eq_str += "("
            eq_str += node.name
            eq_str += "("
            eq_str = self.parse_equation(node.value_branch, eq_str)
            eq_str += ")"
            eq_str += ")"

        elif n_type == TreeNodeType.BINARY_OP:
            eq_str += "("
            eq_str = self.parse_equation(node.left_branch, eq_str)
            eq_str += " " + node.name + " "
            eq_str = self.parse_equation(node.right_branch, eq_str)
            eq_str += ")"

        eq_str = eq_str.replace("ADD", "+")
        eq_str = eq_str.replace("SUB", "-")
        eq_str = eq_str.replace("MUL", "*")
        eq_str = eq_str.replace("DIV", "/")
        eq_str = eq_str.replace("COS", "cos")
        eq_str = eq_str.replace("SIN", "sin")

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

        elif node.node_type == TreeNodeType.UNARY_OP:
            self.tree_to_dict(tree, node.value_branch, results)
            results["program"].append({
                "type": node.node_type,
                "name": node.name
            })

        elif node.node_type == TreeNodeType.BINARY_OP:
            self.tree_to_dict(tree, node.left_branch, results)
            self.tree_to_dict(tree, node.right_branch, results)
            results["program"].append({
                "type": node.node_type,
                "name": node.name
            })

        return results
