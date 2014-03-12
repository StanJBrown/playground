#!/usr/bin/env python
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import playground.benchmark.symreg_test_funcs as sym_reg


class SymRegTests(unittest.TestCase):
    def test_write_test_data(self):
        # write test data
        fp = "test.dat"
        data = ["1, 2"]
        sym_reg.write_test_data(fp, data)

        # assert
        test_data_file = open(fp, "rb")
        test_data = test_data_file.read().replace(",", "").split()
        test_data_file.close()

        self.assertEquals(test_data, ["var1", "answer", "1", "2"])

        # clean up
        os.remove(fp)

    def test_generate_random_matrix(self):
        # generate random matrix
        bounds = [
            {"lower": 0, "upper": 10},
            {"lower": 0, "upper": 10}
        ]
        points = 5
        matrix = sym_reg.generate_random_matrix(bounds, points)

        # assert
        self.assertEquals(len(matrix), points)
        # test for unique point set
        test_matrix = list(matrix)
        print matrix
        for i in matrix:
            point_set = test_matrix.pop()
            self.assertFalse(point_set in test_matrix)

    def test_generate_series_matrix(self):
        # generate series matrix
        bounds = [
            {"lower": 0, "upper": 10},
            {"lower": 0, "upper": 10}
        ]
        points = 5
        matrix = sym_reg.generate_series_matrix(bounds, points)

        # assert
        solution = [[0, 0], [2, 2], [4, 4], [6, 6], [8, 8]]
        self.assertEquals(matrix, solution)

        # bounds = [
        #     {"lower": -1, "upper": 1},
        #     {"lower": -1, "upper": 1}
        # ]
        # points = 10
        # matrix = sym_reg.generate_series_matrix(bounds, points)
        # print matrix

    def test_evaluate_test_function(self):
        # evaluate test function
        equation = "v[0] + v[0]"
        var_values = [[1]]
        result = sym_reg.evaluate_test_function(equation, var_values)

        # assert
        self.assertEquals(result, ["1, 2"])

    def test_arabas_et_al_test_functions(self):
        dest = "."
        sym_reg.arabas_et_al_test_functions(dest)

        for i in range(4):
            data_fp = "arabas_et_al-f{0}{1}".format(i + 1, ".dat")
            data_file = open(data_fp, "rb")
            data = data_file.read()
            data_file.close()
            self.assertTrue(len(data) > 0)
            os.unlink(os.path.join(dest, data_fp))

    def test_nguyen_et_al_test_functions(self):
        dest = "."
        sym_reg.nguyen_et_al_test_functions(dest)

        for i in range(10):
            data_fp = "nguyen_et_al-f{0}{1}".format(i + 1, ".dat")
            data_file = open(data_fp, "rb")
            data = data_file.read()
            data_file.close()

            print data
            print
            print

            self.assertTrue(len(data) > 0)
            os.remove(os.path.join(dest, data_fp))

if __name__ == '__main__':
    unittest.main()
