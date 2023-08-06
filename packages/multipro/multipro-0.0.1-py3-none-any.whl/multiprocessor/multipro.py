#!/usr/bin/env python

"""
The objective of this module is to allow anyone to run a parallel execution on any function
This is 100% agnostic.
"""

from multiprocessing import Pool
from multiprocessing import set_start_method


# set the start method
set_start_method('fork')


def execute_code(function_name, pyload, proc_=10):
    """This function enables parallel execution of any code
        you just need to pass the function you want to use, the data for the function and how many processes you want
        to use. The default number of processes to be used is 10, but you can set more or less.
    """

    if function_name:
        p = Pool(proc_)
        result = p.map(function_name, pyload)
        p.close()
        p.join()

        print("\nDone with all processing .... \n".upper())
        return result
    else:
        return

