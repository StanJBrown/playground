#!/usr/bin/env python
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import playground.config as config
from playground.tree import Tree
from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.tree import TreeNodeBranch
from playground.tree import TreeParser
from playground.tree import TreeEvaluator
from playground.tree import TreeInitializer
from playground.functions import FunctionRegistry

# SETTINGS
cwd = os.path.dirname(__file__)
tree_config = os.path.join(cwd, "config/tree.json")
tree_init_config = os.path.join(cwd, "config/initializer.json")
eval_config = os.path.join(cwd, "config/evaluator.json")


class TreeNodeTests(unittest.TestCase):
    def setUp(self):
        self.left_node = TreeNode(TreeNodeType.TERM, value=1.0)
        self.left_node_2 = TreeNode(TreeNodeType.TERM, value=1.0)

        self.right_node = TreeNode(TreeNodeType.TERM, value=2.0)
        self.right_node_2 = TreeNode(TreeNodeType.TERM, value=2.0)

        self.binary_node = TreeNode(
            TreeNodeType.BINARY_OP,
            left_branch=self.left_node,
            right_branch=self.right_node
        )

    def test_has_value_node(self):
        # assert left branch
        res = self.binary_node.has_value_node(self.left_node)
        self.assertEquals(res, TreeNodeBranch.LEFT)

        # assert right branch
        res = self.binary_node.has_value_node(self.right_node)
        self.assertEqual(res, TreeNodeBranch.RIGHT)

        # assert fail left branch
        res = self.binary_node.has_value_node(self.left_node_2)
        self.assertFalse(res)

        # assert fail right branch
        res = self.binary_node.has_value_node(self.right_node_2)
        self.assertFalse(res)

    def test_equal(self):
        term_node = TreeNode(TreeNodeType.TERM, value=2)

        # assert UNARY_OP node
        unary_node = TreeNode(TreeNodeType.UNARY_OP, name="SIN")
        self.assertTrue(unary_node.equals(unary_node))
        self.assertFalse(unary_node.equals(term_node))

        # assert BINARY_OP node
        binary_node = TreeNode(TreeNodeType.UNARY_OP, name="ADD")
        self.assertTrue(binary_node.equals(binary_node))
        self.assertFalse(binary_node.equals(term_node))

        # assert TERM node
        term_node_2 = TreeNode(TreeNodeType.TERM, value=1.0)
        self.assertTrue(term_node_2.equals(term_node_2))
        self.assertFalse(term_node_2.equals(term_node))

        # assert INPUT node
        input_node = TreeNode(TreeNodeType.INPUT, name="x")
        self.assertTrue(input_node.equals(input_node))
        self.assertFalse(input_node.equals(term_node))


class TreeTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(tree_config)
        self.t_parser = TreeParser()
        self.tree = Tree()

        node_x = TreeNode(TreeNodeType.INPUT, name="x")
        node_y = TreeNode(TreeNodeType.INPUT, name="y")
        node_z = TreeNode(TreeNodeType.INPUT, name="z")

        self.tree.input_nodes.append(node_x)
        self.tree.input_nodes.append(node_y)
        self.tree.input_nodes.append(node_z)

    def test_valid(self):
        # assert valid
        res = self.tree.valid(self.config["input_nodes"])
        self.assertTrue(res)

        # assert fail valid
        self.tree.input_nodes.pop()
        res = self.tree.valid(self.config["input_nodes"])
        self.assertFalse(res)

    def test_get_linked_node(self):
        # setup
        del self.tree.input_nodes[:]
        left_node = TreeNode(TreeNodeType.INPUT, name="x")
        right_node = TreeNode(TreeNodeType.INPUT, name="y")
        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=left_node,
            right_branch=right_node
        )
        self.tree.root = add_func
        self.tree.program = self.t_parser.post_order_traverse(self.tree.root)

        # pass test
        linked_node = self.tree.get_linked_node(left_node)
        self.assertTrue(linked_node is add_func)
        linked_node = self.tree.get_linked_node(right_node)
        self.assertTrue(linked_node is add_func)

        # fail test
        random_node = TreeNode(TreeNodeType.INPUT, name="z")
        linked_node = self.tree.get_linked_node(random_node)
        self.assertFalse(linked_node is add_func)

    def test_replace_node(self):
        # setup
        node_x = TreeNode(TreeNodeType.INPUT, name="x")
        node_y = TreeNode(TreeNodeType.INPUT, name="y")
        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=node_x,
            right_branch=node_y
        )

        tree = Tree()
        tree.root = add_func
        tree.update_program()

        # replace node
        new_node = TreeNode(TreeNodeType.INPUT, name="z")
        before_replace = list(tree.program)
        tree.replace_node(node_x, new_node)
        after_replace = list(tree.program)

        # assert
        self.assertTrue(before_replace == before_replace)
        self.assertTrue(after_replace == after_replace)
        self.assertFalse(before_replace == after_replace)
        self.assertTrue(add_func.left_branch is new_node)

    def test_equal(self):
        # create nodes
        left_node_1 = TreeNode(TreeNodeType.TERM, value=1.0)
        right_node_1 = TreeNode(TreeNodeType.TERM, value=2.0)

        left_node_2 = TreeNode(TreeNodeType.TERM, value=3.0)
        right_node_2 = TreeNode(TreeNodeType.TERM, value=4.0)

        cos_func_1 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="COS",
            value_branch=left_node_1,
        )
        sin_func_1 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="SIN",
            value_branch=right_node_1,
        )

        cos_func_2 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="COS",
            value_branch=left_node_2,
        )
        sin_func_2 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="SIN",
            value_branch=right_node_2,
        )

        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=cos_func_1,
            right_branch=sin_func_1
        )

        sub_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="SUB",
            left_branch=sin_func_2,
            right_branch=cos_func_2
        )

        # create tree_1
        tree_1 = Tree()
        tree_1.root = add_func
        tree_1.update_program()
        tree_1.update_func_nodes()
        tree_1.update_term_nodes()

        # create tree_2
        tree_2 = Tree()
        tree_2.root = sub_func
        tree_2.update_program()
        tree_2.update_func_nodes()
        tree_2.update_term_nodes()

        self.assertTrue(tree_1.equals(tree_1))
        self.assertFalse(tree_1.equals(tree_2))
        self.assertTrue(tree_2.equals(tree_2))
        self.assertFalse(tree_2.equals(tree_1))

    def test_str(self):
        # setup
        del self.tree.input_nodes[:]
        left_node = TreeNode(TreeNodeType.INPUT, name="x")
        right_node = TreeNode(TreeNodeType.INPUT, name="y")
        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=left_node,
            right_branch=right_node
        )
        self.tree.root = add_func
        self.tree.program = self.t_parser.post_order_traverse(self.tree.root)

        # assert
        self.assertEquals(str(self.tree), "(x + y)")


class TreeInitializerTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(tree_init_config)

        self.functions = FunctionRegistry()
        self.evaluator = TreeEvaluator(self.config, self.functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

        self.tree_parser = TreeParser()

    def tearDown(self):
        del self.config
        del self.tree_initializer
        del self.tree_parser

    def test_tree_add_input_nodes(self):
        # setup
        # create nodes
        left_node = TreeNode(TreeNodeType.TERM, value=1.0)
        right_node = TreeNode(TreeNodeType.TERM, value=2.0)
        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=left_node,
            right_branch=right_node
        )
        # create tree
        tree = Tree()
        tree.root = add_func
        tree.update_program()
        tree.update_func_nodes()
        tree.update_term_nodes()

        # add input nodes
        self.tree_initializer._add_input_nodes(tree)
        self.assertTrue(len(tree.input_nodes) == 2)

    def test_full_method(self):
        tests = 1000

        for i in range(tests):
            tree = self.tree_initializer.full_method()

            # # func nodes
            # print("FUNCTION NODES!")
            # for func_node in tree.func_nodes:
            #     self.tree_parser._print_node(func_node)

            # # term nodes
            # print("\nTERMINAL NODES!")
            # for term_node in tree.term_nodes:
            #     self.tree_parser._print_node(term_node)

            # program
            # print("\nPROGRAM STACK!")
            # for block in tree.program:
            #     self.tree_parser._print_node(block)

            # # dot graph
            # print("\nDOT GRAPH!")
            # self.tree_parser.print_tree(tree.root)

            # asserts
            self.assertEquals(tree.depth, self.config["max_depth"])
            self.assertTrue(tree.size > self.config["max_depth"])
            self.assertTrue(tree.branches > 0)
            self.assertEquals(tree.open_branches, 0)
            self.assertTrue(
                len(tree.input_nodes) >= len(self.config["input_nodes"])
            )

    def test_grow_method(self):
        tests = 1000

        for i in range(tests):
            tree = self.tree_initializer.grow_method()

            # # func nodes
            # print("FUNCTION NODES!")
            # for func_node in tree.func_nodes:
            #     self.tree_parser._print_node(func_node)

            # # term nodes
            # print("\nTERMINAL NODES!")
            # for term_node in tree.term_nodes:
            #     self.tree_parser._print_node(term_node)

            # # program
            # print("\nPROGRAM STACK!")
            # for block in tree.program:
            #     self.tree_parser._print_node(block)

            # dot graph
            # print("\nDOT GRAPH!")
            # self.tree_parser.print_tree(tree.root)

            # asserts
            self.assertEquals(tree.depth, self.config["max_depth"])
            self.assertTrue(tree.size > self.config["max_depth"])
            self.assertTrue(tree.branches > 0)
            self.assertEquals(tree.open_branches, 0)
            self.assertTrue(
                len(tree.input_nodes) >= len(self.config["input_nodes"])
            )

    def test_init(self):
        population = self.tree_initializer.init()
        self.assertEquals(len(population.individuals), 10)


class TreeParserTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(tree_config)

        self.functions = FunctionRegistry()
        self.evaluator = TreeEvaluator(self.config, self.functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

        self.tree_parser = TreeParser()

        # create nodes
        left_node = TreeNode(TreeNodeType.TERM, value=1.0)
        right_node = TreeNode(TreeNodeType.TERM, value=2.0)

        cos_func = TreeNode(
            TreeNodeType.UNARY_OP,
            name="COS",
            value_branch=left_node,
        )
        sin_func = TreeNode(
            TreeNodeType.UNARY_OP,
            name="SIN",
            value_branch=right_node,
        )

        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=cos_func,
            right_branch=sin_func
        )

        # create tree
        self.tree = Tree()
        self.tree.root = add_func
        self.tree.update_program()
        self.tree.update_func_nodes()
        self.tree.update_term_nodes()

    def tearDown(self):
        del self.config
        del self.tree_initializer
        del self.tree_parser

    def test_parse_tree(self):
        # self.tree_parser.print_tree(tree.root)
        program = self.tree_parser.parse_tree(self.tree, self.tree.root)
        for i in program:
            if i.name is not None:
                print i.name
            else:
                print i.value

        self.assertEquals(self.tree.size, 5)
        self.assertEquals(self.tree.depth, 2)
        self.assertEquals(self.tree.branches, 2)
        self.assertEquals(self.tree.open_branches, 0)

        self.assertEquals(len(self.tree.func_nodes), 2)
        self.assertEquals(len(self.tree.term_nodes), 2)
        self.assertEquals(len(self.tree.input_nodes), 0)

    def test_parse_equation(self):
        # self.tree_parser.print_tree(tree.root)
        equation = self.tree_parser.parse_equation(self.tree.root)
        self.assertEquals(equation, "((cos(1.0)) + (sin(2.0)))")


class TreeEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(eval_config)

        self.functions = FunctionRegistry()
        self.evaluator = TreeEvaluator(self.config, self.functions)
        self.tree_initializer = TreeInitializer(self.config, self.evaluator)

    def tearDown(self):
        del self.config
        del self.tree_initializer
        del self.functions
        del self.evaluator

    def test_gen_term_node(self):
        row = 0
        node_x = TreeNode(TreeNodeType.INPUT, name="x")
        term_node = self.evaluator._gen_term_node(node_x, row)

        # asserts
        self.assertEquals(term_node.node_type, TreeNodeType.TERM)
        self.assertEquals(term_node.name, None)
        self.assertEquals(term_node.value, 10.0)

    def test_eval_node(self):
        term_node_1 = TreeNode(TreeNodeType.TERM, value=0.0)
        term_node_2 = TreeNode(TreeNodeType.TERM, value=90.0)
        term_node_3 = TreeNode(TreeNodeType.TERM, value=10.0)
        unary_node = TreeNode(TreeNodeType.UNARY_OP, name="COS")
        binary_node = TreeNode(TreeNodeType.BINARY_OP, name="ADD")

        # evaluate term_node
        stack = []
        self.evaluator.eval_node(term_node_1, stack)
        self.assertEquals(len(stack), 1)
        self.assertTrue(stack[0] is term_node_1)

        # evaluate unary_node
        stack = []
        stack.append(term_node_1)
        self.evaluator.eval_node(unary_node, stack)
        self.assertEquals(len(stack), 1)
        self.assertTrue(stack[0].value == 1.0)

        # evaluate binary_node
        stack = []
        stack.append(term_node_2)
        stack.append(term_node_3)
        self.evaluator.eval_node(binary_node, stack)
        self.assertEquals(len(stack), 1)
        self.assertTrue(stack[0].value == 100.0)

    def test_eval_program(self):
        # create nodes
        term_node = TreeNode(TreeNodeType.TERM, value=100.0)
        input_node = TreeNode(TreeNodeType.INPUT, name="x")

        rad_func = TreeNode(
            TreeNodeType.UNARY_OP,
            name="RAD",
            value_branch=input_node
        )

        mul_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="MUL",
            left_branch=rad_func,
            right_branch=term_node
        )

        sin_func = TreeNode(
            TreeNodeType.UNARY_OP,
            name="SIN",
            value_branch=mul_func
        )

        # create tree
        tree = Tree()
        tree.root = sin_func
        tree.update_program()
        tree.update_func_nodes()
        tree.update_term_nodes()

        # program
        print("\nPROGRAM STACK!")
        for block in tree.program:
            if block.name is not None:
                print block.name
            else:
                print block.value
        print ""

        # evaluate tree
        res = self.evaluator.eval_program(tree.program, tree.size)

        # assert
        self.assertTrue(res is not None)
        self.assertEquals(round(res, 4), 0.0)

    def test_eval_sub_tree(self):
        # create nodes
        term_node_1 = TreeNode(TreeNodeType.TERM, value=100.0)
        term_node_2 = TreeNode(TreeNodeType.TERM, value=10.0)
        term_node_3 = TreeNode(TreeNodeType.TERM, value=20.0)
        input_node = TreeNode(TreeNodeType.INPUT, name="x")

        div_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="DIV",
            left_branch=term_node_1,
            right_branch=term_node_2
        )

        mul_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="MUL",
            left_branch=term_node_3,
            right_branch=input_node
        )

        root = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=div_func,
            right_branch=mul_func
        )

        # create tree
        tree = Tree()
        tree.root = root
        tree.update()

        # program
        print("\nPROGRAM STACK!")
        for block in tree.program:
            if block.name is not None:
                print block.name
            else:
                print block.value
        print ""

        # evaluate tree
        res = self.evaluator.eval_sub_tree(div_func, tree.size)
        self.assertTrue(res is not None)

    def test_evaluate(self):
        population = self.tree_initializer.init()
        population.evaluator = self.evaluator
        population.evaluate_population()

        for individual in population.individuals:
            self.assertTrue(individual.score is not None)
            self.assertTrue(individual.score > 0)


if __name__ == '__main__':
    unittest.main()
