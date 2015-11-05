from .. import boilerplate
import unittest


class ManageExceptionTestCase(unittest.TestCase):

    def test_emitFalse(self):
        import os, sys

        didNotThrow = False

        stdout = sys.stdout
        f = open(os.devnull, 'w')
        try:
            try:
                raise RuntimeError('This message should not be displayed')
            except Exception as e:
                sys.stdout = f
                boilerplate.manageException(e, False)
                didNotThrow = True
        finally:
            sys.stdout = stdout
            f.close()

        self.assertTrue(didNotThrow)


    def test_emitTrue(self):

        didThrow = False
        try:
            raise RuntimeError('test')
        except Exception as e:
            try:
                boilerplate.manageException(e, True)
            except Exception as e:
                didThrow = True

        self.assertTrue(didThrow)
