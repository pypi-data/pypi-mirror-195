import os


###############################################################################
# load_tests protocol
###############################################################################
def load_tests(loader, standard_tests, pattern):
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern='test_*.py')
    standard_tests.addTests(package_tests)

    return standard_tests
