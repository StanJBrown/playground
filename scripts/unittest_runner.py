#!/usr/bin/env python
import os
import re
import sys
import shutil
import subprocess


# SETTINGS
keep_unittest_logs = False
unittests_bin_dir = "bin"
unittests_log_dir = "unittests_log"
unittests_file_pattern = "^[a-zA-Z0-9_]*_tests$"


class TermColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def print_stdout(unittest_output_fp):
    # open unittest stdout log file
    unittest_output = open(unittest_output_fp, 'r')
    output_content = unittest_output.read()
    unittest_output.close()

    # print unittest stdout
    print("-" * 79)
    print(output_content)
    print("-" * 79)


if __name__ == "__main__":
    orig_cwd = os.getcwd()

    # make log dir if not already exist
    if not os.path.exists(unittests_log_dir):
        os.mkdir(unittests_log_dir)

    # gather all unittests
    file_list = os.listdir(unittests_bin_dir)
    unittests = []
    for f in file_list:
        if re.match(unittests_file_pattern, f):
            unittests.append(f)

    # execute all unittests
    os.chdir(unittests_bin_dir)
    error = False
    return_val = 0
    for unittest in unittests:
        print("UNITTEST [{0}] ".format(unittest)),

        # execute unittest
        try:
            unittest_output_fp = os.path.join(
                orig_cwd,
                unittests_log_dir,
                unittest + ".log"
            )

            unittest_output = open(unittest_output_fp, 'w')
            return_val = subprocess.check_call(
                "./{0}".format(unittest),
                stdout=unittest_output,
                stderr=unittest_output
            )
            unittest_output.close()
            print("{0}PASSED!{1}".format(TermColors.OKGREEN, TermColors.ENDC))

        except:
            unittest_output.close()
            print("{0}FAILED!{1}".format(TermColors.FAIL, TermColors.ENDC))
            print_stdout(unittest_output_fp)
            error = True


    # remove unittest stdout dir
    os.chdir(orig_cwd)
    shutil.rmtree(unittests_log_dir)

    if error is True:
        sys.exit(-1)
    else:
        sys.exit(0)
