import unittest
import sys

sys.path.append('cfBroker')

def get_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__package__)
    return suite