#!/usr/bin/env python

from playground.tree import TreeNodeType
from playground.functions import FunctionRegistry


class TreeEvaluator(object):
    def __init__(self):
        print ""

    def eval_node(self, node, stack):
        ntype = node.node_type

        if ntype == TreeNodeType.TERM:
            stack.push(node)
        elif ntype == TreeNodeType.UNARY_OP:
            value = stack.pop()

            stack.push(node)
        elif ntype == TreeNodeType.BINARY_OP:


# int evaluate_node(struct ast *node, struct stack *s)
# {
#         struct ast *value;
#         struct ast *x;
#         struct ast *y;
#         struct ast *result = NULL;
#
#         if (node->tag == INTEGER || node->tag == REAL) {
#                 stack_push(s, node);
#
#         } else if (node->tag == STRING) {
#                 stack_push(s, node);
#
#         } else if (node->tag == UNARY_OP) {
#                 value = stack_pop(s);
#
#                 result = execute_unary_function(node, value);
#                 stack_push(s, result);
#
#                 ast_destroy(value);
#                 ast_destroy(node);
#
#         } else if (node->tag == BINARY_OP) {
#                 y = stack_pop(s);
#                 x = stack_pop(s);
#
#                 result = execute_binary_function(node, x, y);
#                 stack_push(s, result);
#
#                 ast_destroy(x);
#                 ast_destroy(y);
#                 ast_destroy(node);
#
#         } else {
#                 log_err("Error! Unknown node->tag!");
#                 goto error;
#         }
#
#         return 0;
# error:
#         return -1;
# }
