# playground.gp.tree.parser
This module contains tree parsing methods.

**Classes**:
- TreeParser(object)


## TreeParser(object)
`TreeParser` is responsible for tree parsing operations.

**Methods**:
- print_tree(root_node)
- post_order_traverse(node, stack=None)
- parse_tree(tree, node, depth=None, stack=None)
- parse_equation(node, eq_str=None)


### print_tree(root_node)
Prints the tree structure in dot graph language

    Args:

        root_node (TreeNode): root of the tree


### post_order_traverse(node, stack=None)
Traverses the tree in post-order, as the tree is traversed a stack is built.

    Args:

        node (TreeNode):
            node to start traversing from (usually node is the root)

        stack (list of TreeNode):
            stack in post-order form

    Returns:

        A list of TreeNode in post-order form


### parse_tree(tree, node, depth=None, stack=None)
`parse_tree` traverses the tree in post-order, it updates `tree`'s attributes
on the fly, namely the `depth`, `size`, `branches` and `open_branches`. And
also creates a stack in post-order form as well.

    Args:

        tree (Tree):
            Tree to be parsed

        node (TreeNode):
            Tree node to start parsing from

        depth (int):
            Depth of the tree

        stack (int):
            Stack of the tree in post-order form

    Returns:

        A list of TreeNode in post-order form


### parse_equation(node, eq_str=None)
Returns a string representation of the `Tree` in infix-order.


    Args:

        node (TreeNode):
            Tree node to start parsing from

        eq_str (str):
            String the tree in infix-order form

    Returns:

        Infix order of the tree


