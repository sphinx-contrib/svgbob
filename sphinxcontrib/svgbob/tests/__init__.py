from . import (
    test_sphinx,
    test_svgbob,
)

def load_tests(loader, suite, pattern):
    suite.addTests(loader.loadTestsFromModule(test_sphinx))
    suite.addTests(loader.loadTestsFromModule(test_svgbob))
    return suite
