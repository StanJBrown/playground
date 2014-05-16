# tree
`tree` contains classes and methods to do with the representation and
generation of a tree, be it a node of a tree, the actual tree or a parser or
evaluator.

    Classes:
        - NodeType
        - NodeBranch
        - Node
        - Tree
        - TreeGenerator
        - TreeEvaluator



## NodeType(object)
`NodeType` encapsulates the idea of what type of tree node one is. It
denotes tree nodes:

- Unary function node
- Binary function node
- Terminal node
- Input node


    Constants:

        UNARY_OP
        BINARY_OP
        TERM
        INPUT



## NodeBranch(object)
`NodeBranch` encapsulates the idea of which branch a particular node
resides inrespect to a function node (assuming the node in concern is indeed a
value of the function node).

    Constants:

        VALUE
        LEFT
        RIGHT



## Node(object)
`Node` represents a node in a tree, be it a function, terminal or input
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
            if node_type is NodeType.UNARY_OP:
                name (str) and value_branch (object) are expected.

            else if node_type is NodeType.BINARY_OP:
                name (str), left_branch (object) and right_branch (object) are
                expected.

            # terminal node specific
            if node_type is NodeType.CONSTANT:
                name (str) and value (object) are expected.

            else node_type is NodeType.INPUT:
                name (str) is expected.


### has_value_node(node)
A boolean function that checks whether the instance has a node `node`. This is
useful if the instance is a function node, say a unary node. If `node` is
indeed a value node of the unary function node, `has_value_node(node)` would
return `True`, else `False`.

    Args:

        node (Node):
            node to check against

    Returns:

        True or False


### is_function()
A boolean function that checks to see if `Node` instance is a function.

    Returns:

        True or False


### is_terminal()
A boolean function that checks to see if `Node` instance is a terminal.

    Returns:

        True or False


### is_input()
A boolean function that checks to see if `Node` instance is an input.

    Returns:

        True or False


### equals(node)
A boolean function that checks to see if `Node` instance is equals to node.

    Args:

        node (Node):
            node to check against

    Returns:

        True or False



## Tree(object)
`Tree` represents the a whole tree, it contains information of all the nodes
within a tree, as well as the size and depth, etc.


    Attributes

        score (float):
            score of the tree

        root (Node):
            root of the tree

        depth (int):
            depth of the tree

        size (int):
            size or total number of nodes in a tree

        branches (int):
            number of branches in a tree

        open_branches (int):
            number of open branches in a tree

        program (list of Node):
            tree in post-order form in a stack

        func_nodes (list of Node):
            list of function nodes

        term_nodes (list of Node):
            list of terminal nodes

        input_nodes (list of Node):
            list of input nodes

        parser (TreeParser):
            tree parser instance


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

        target_node (Node):
            target node to be used to find the function node that contains this
            `target_node`

    Returns:

        linked function node (Node)


### replace_node(target_node, replace_with, override_update=False)
Replaces the `taget_node` with `replace_with` in the tree. There is also the
option to prevent the tree from updating it's attributes with `override_update`
set to `True`.

    Args:

        target_node (Node):
            target node to replace

        replace_with (Node):
            node to replace with


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



## TreeGenerator(object)
`TreeGenerator` is responsible for creating an population of `Tree`s used in
the Genetic Programming process. It supports tree intialization using the:

- Full Method
- Grow Method


    Attributes:

        config (dict):
            configuration

        parser (TreeParser):
            tree parser instance

        tree_evaluator (TreeEvaluator):
            tree evaluator instance


### full_method()
Initializes a single `Tree` using the full method

    Returns:

        A `Tree` object


### grow_method()
Initializes a single `Tree` using the grow method

    Returns:

        A `Tree` object


### generate_tree()
A general method that looks at `config` for which type of tree initialization
should be used. The `config` key expected is "tree_init_method".

    Returns:

        A `Tree` object


### init()
Initializes a population of trees. It looks at `config` for which type of tree
initialization should be used. The `config` key expected is "tree_init_method".

    Returns:

        A `Population` object full of initialized `Tree` objects



## TreeParser(object)
`TreeParser` is responsible for tree parsing operations.


### print_tree(root_node)
Prints the tree structure in dot graph language

    Args:

        root_node (Node): root of the tree


### post_order_traverse(node, stack=None)
Traverses the tree in post-order, as the tree is traversed a stack is built.

    Args:

        node (Node):
            node to start traversing from (usually node is the root)

        stack (list of Node):
            stack in post-order form

    Returns:

        A list of Node in post-order form


### parse_tree(tree, node, depth=None, stack=None)
`parse_tree` traverses the tree in post-order, it updates `tree`'s attributes
on the fly, namely the `depth`, `size`, `branches` and `open_branches`. And
also creates a stack in post-order form as well.

    Args:

        tree (Tree):
            Tree to be parsed

        node (Node):
            Tree node to start parsing from

        depth (int):
            Depth of the tree

        stack (int):
            Stack of the tree in post-order form

    Returns:

        A list of Node in post-order form


### parse_equation(node, eq_str=None)
Returns a string representation of the `Tree` in infix-order.


    Args:

        node (Node):
            Tree node to start parsing from

        eq_str (str):
            String the tree in infix-order form

    Returns:

        Infix order of the tree


## TreeEvaluator(object)
`TreeEvaluator` evaluates a `Tree` object to determine its fitness score.


    Attributes

        config (dict):
            configuration

        functions (GPFunctionRegistry):
            GPFunctionRegistry instance

        parser (TreeParser):
            TreeParser instance


    Constructor Arguments:

        config (dict):
            configuration

        function_registry (GPFunctionRegistry):
            GPFunctionRegistry instance


### eval_node(node, stack)
Evaluates `node` in question. If `node` is a terminal, it is added to the
stack, else if `node` is a function node, the inputs for the function node will
be popped from the `stack` and used for evaluation, with the results pushed
back into the stack.

    Args:

        node (Node):
            Node to be evaluated

        stack (list of Node):
            Evaluation stack

    Throws:

        EvalationError if an error occurred during evaluation


### eval_program(program, tree_size)
Evaluates the tree's program, in other words the tree's stack in post-order
form.

    Args:

        program (list of Node):
            Tree in post-order form in a stack

        tree_size ():
            Evaluation stack

    Throws:

        EvalationError if an error occurred during evaluation


### evaluate(tree)
Evaluates the tree.

    Args:

        Tree (Tree):
            Tree to be evaluated

    Throws:

        EvalationError if an error occurred during evaluation
