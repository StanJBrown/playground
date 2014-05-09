# playground.gp.tree.evaluation_2
This module contains methods needed to evaluate the GP tree structure.

**Functions**:
- eval_node(node, stack)
- eval_program(program, tree_size)
- evaluate(tree)

**Classes**:
- TreeEvaluator(object)


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

        node (TreeNode):
            Node to be evaluated

        stack (list of TreeNode):
            Evaluation stack

    Throws:

        EvalationError if an error occurred during evaluation


### eval_program(program, tree_size)
Evaluates the tree's program, in other words the tree's stack in post-order
form.

    Args:

        program (list of TreeNode):
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
