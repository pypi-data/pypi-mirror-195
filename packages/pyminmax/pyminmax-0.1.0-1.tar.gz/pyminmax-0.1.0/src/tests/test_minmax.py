###############################################################################
# Imports
###############################################################################
import unittest

from pyminmax import minmax


###############################################################################
# Tests
###############################################################################
class MinmaxTest(unittest.TestCase):
    # Most of the tests here are adapted from test_max() in the CPython test
    # suite.
    def test_minmax(self):
        self.assertEqual(minmax('123123'), ('1', '3'))
        self.assertEqual(minmax(1, 2, 3), (1, 3))
        self.assertEqual(minmax((1, 2, 3, 1, 2, 3)), (1, 3))
        self.assertEqual(minmax([1, 2, 3, 1, 2, 3]), (1, 3))

        self.assertEqual(minmax(1, 2, 3.0), (1, 3.0))
        self.assertEqual(minmax(1, 2.0, 3), (1, 3))
        self.assertEqual(minmax(1.0, 2, 3), (1.0, 3))

        with self.assertRaisesRegex(
            TypeError, "minmax expected at least 1 argument, got 0"):
            minmax()

        self.assertRaises(TypeError, minmax, 42)

        with self.assertRaisesRegex(ValueError,
                                    "minmax() iterable argument is empty"):
            minmax(())

        with self.assertRaisesRegex(TypeError,
            "Cannot specify a default for minmax() with multiple positional "
            "arguments"):
            minmax(1, 2, default=None)

        class BadSeq:
            def __getitem__(self, index):
                raise ValueError
        self.assertRaises(ValueError, minmax, BadSeq())

        for stmt in (
            "minmax(key=int)",                 # no args
            "minmax(default=None)",
            "minmax(1, 2, default=None)",      # require container for default
            "minmax(default=None, key=int)",
            "minmax(1, key=int)",              # single arg not iterable
            "minmax(1, 2, keystone=int)",      # wrong keyword
            "minmax(1, 2, key=int, abc=int)",  # two many keywords
            "minmax(1, 2, key=1)",             # keyfunc is not callable
            ):
            try:
                exec(stmt, globals())
            except TypeError:
                pass
            else:
                self.fail(stmt)

        self.assertEqual(minmax((1,), key=neg), (1, 1))    # one elem iterable
        self.assertEqual(minmax((1, 2), key=neg), (2, 1))  # two elem iterable
        self.assertEqual(minmax(1, 2, key=neg), (2, 1))    # two elems

        # zero elem iterable
        self.assertEqual(minmax((), default=None), (None,None))
        # one elem iterable
        self.assertEqual(minmax((1,), default=None), (1, 1))
        # two elem iterable
        self.assertEqual(minmax((1,2), default=None), (1, 2))

        self.assertEqual(minmax((), default=1, key=neg), (1,1))
        self.assertEqual(minmax((1, 2), default=3, key=neg), (2, 1))

        self.assertEqual(minmax((1, 2), key=None), (1, 2))

        data = [random.randrange(200) for i in range(100)]
        keys = dict((elem, random.randrange(50)) for elem in data)
        f = keys.__getitem__
        sdata = sorted(reversed(data), key=f)
        self.assertEqual(minmax(data, key=f), (sdata[0], sdata[-1]))

if __name__ == "__main__":
    unittest.main()
