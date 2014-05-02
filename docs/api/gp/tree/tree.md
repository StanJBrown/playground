# playground.gp.tree

**Classes**:
- TreeNode(object)
- Tree(object)


## TreeNode(object)
`TreeNode` represents a node in a tree, be it a function, terminal or input
node.


    Attributes:

        node_type (str):
            type of node

        name (str):
            name of node

        value (object):
            value of node

        left_branch (object):
            left value of function node

        right_branch (object):
            right value of function node

        value_branch (object):
            value of function node


    Constructor Arguments:

        node_type (str):
            node type

        **kwargs:

            # function node specific
            if node_type is TreeNodeType.UNARY_OP:
                name (str) and value_branch (object) are expected.

            else if node_type is TreeNodeType.BINARY_OP:
                name (str), left_branch (object) and right_branch (object) are
                expected.

            # terminal node specific
            if node_type is TreeNodeType.TERM:
                name (str) and value (object) are expected.

            else node_type is TreeNodeType.INPUT:
                name (str) is expected.

**Methods**:

- has_value_node(node)
- is_function()
- is_terminal()
- is_input()
- equals(node)


### has_value_node(node)
A boolean function that checks whether the instance has a node `node`. This is
useful if the instance is a function node, say a unary node. If `node` is
indeed a value node of the unary function node, `has_value_node(node)` would
return `True`, else `False`.

    Args:

        node (TreeNode):
            node to check against

    Returns:

        True or False


### is_function()
A boolean function that checks to see if `TreeNode` instance is a function.

    Returns:

        True or False


### is_terminal()
A boolean function that checks to see if `TreeNode` instance is a terminal.

    Returns:

        True or False


### is_input()
A boolean function that checks to see if `TreeNode` instance is an input.

    Returns:

        True or False


### equals(node)
A boolean function that checks to see if `TreeNode` instance is equals to node.

    Args:

        node (TreeNode):
            node to check against

    Returns:

        True or False



## Tree(object)
`Tree` represents the a whole tree, it contains information of all the nodes
within a tree, as well as the size and depth, etc.


    Attributes

        score (float):
            score of the tree

        root (TreeNode):
            root of the tree

        depth (int):
            depth of the tree

        size (int):
            size or total number of nodes in a tree

        branches (int):
            number of branches in a tree

        open_branches (int):
            number of open branches in a tree

        program (list of TreeNode):
            tree in post-order form in a stack

        func_nodes (list of TreeNode):
            list of function nodes

        term_nodes (list of TreeNode):
            list of terminal nodes

        input_nodes (list of TreeNode):
            list of input nodes

        tree_parser (TreeParser):
            tree parser instance

**Methods**:
- valid(config_input_nodes)
- get_linked_node(target_node)
- replace_node(target_node, replace_with, override_update=False)
- equals(tree)
- update_program()
- update_func_nodes()
- update_term_nodes()
- update()


### valid(config_input_nodes)
A boolean function that checks to see if `Tree` instance is valid. The criteria
is if it constains a minimum of 1 copy of each input node in
`config_input_nodes` then the tree is valid.

    Args:

        config_input_nodes (list of dict):
            a list of dictionary objects containing the name of each input node
            to be checked. Assumes all dictionary objects have key "name".

    Returns:

        True or False


### get_linked_node(target_node)
Returns a function node to which contains `target_node` in the function node's
branches. This is useful in situations where one needs to replace the
`target_node`, but also need to reflect the changes back to the linked function
node.

    Args:

        target_node (TreeNode):
            target node to be used to find the function node that contains this
            `target_node`

    Returns:

        linked function node (TreeNode)


### replace_node(target_node, replace_with, override_update=False)
Replaces the `taget_node` with `replace_with` in the tree. There is also the
option to prevent the tree from updating it's attributes with `override_update`
set to `True`.

    Args:

        target_node (TreeNode):
            target node to replace

        replace_with (TreeNode):
            node to replace with

        override_update (bool)[default=False]:
            flag to override update


### equals(tree)
A boolean function to check to see if `tree` is equals to `Tree` instance.

    Args:

        tree (Tree):
            tree to check against

    Returns:

        True or False


### update_program()
Updates the postfix stack of the tree.


### update_func_nodes()
Updates the list of function nodes in the tree.


### update_term_nodes()
Updates the list of terminal nodes in the tree.


### update_input_nodes()
Updates the list of input nodes in the tree.

### update()
Updates every attribute in the tree, from the depth, size, to list of function,
terminal and input nodes.
