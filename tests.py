from pprint import pprint
from unittest import TestCase, TestSuite, TextTestRunner

class TestCnoc(TestCase):

    def testErrors(self):
        from cnoc import compiler, CnocException

        with self.assertRaises(CnocException) as cm:
            compiler.parse('("a" or "b") or')
        self.assertIn('Expecting node or right parenthesis', cm.exception.args[0])

        with self.assertRaises(CnocException) as cm:
            compiler.parse('("a" or "b"')
        self.assertIn('Expecting node or right parenthesis', cm.exception.args[0])

        with self.assertRaises(CnocException) as cm:
            compiler.parse('or "a" and "b"')
        self.assertIn('Operation OR missing first operand', cm.exception.args[0])

        with self.assertRaises(CnocException) as cm:
            compiler.parse('"a" and "b")')
        self.assertIn('Too many right parenthesis', cm.exception.args[0])

        with self.assertRaises(CnocException) as cm:
            compiler.parse('"a" and b"')
        self.assertIn('Illegal character \'b\'', cm.exception.args[0])

    def testParse(self):
        from cnoc import compiler, And, Or, Str, Not

        node = compiler.parse('"a" and ("b" or "c")')
        self.assertEqual(type(node), And)
        self.assertEqual(type(node.a), Str)
        self.assertEqual(node.a.data, 'a')
        self.assertEqual(type(node.b), Or)
        self.assertEqual(type(node.b.a), Str)

        self.assertEqual(node.run("c"), False)
        self.assertEqual(node.run("ab"), True)
        self.assertEqual(node.run("abc"), True)
        self.assertEqual(node.run("d"), False)

        node = compiler.parse('("a" and "b") or "c"')
        self.assertEqual(type(node), Or)
        self.assertEqual(type(node.a), And)
        self.assertEqual(type(node.a.b), Str)
        self.assertEqual(node.a.b.data, 'b')
        self.assertEqual(type(node.b), Str)

        self.assertEqual(node.run("c"), True)
        self.assertEqual(node.run("ab"), True)
        self.assertEqual(node.run("abc"), True)
        self.assertEqual(node.run("d"), False)

        node = compiler.parse('not ("a" and "b") or "c"')
        self.assertEqual(type(node), Or)
        self.assertEqual(type(node.a), Not)
        self.assertEqual(type(node.a.a), And)

        self.assertEqual(node.run("c"), True)
        self.assertEqual(node.run("ab"), False)
        self.assertEqual(node.run("abc"), True)
        self.assertEqual(node.run("d"), True)

        node = compiler.parse('not "a" and "b" or "c"')
        self.assertEqual(node.string(), '(not "a" and "b") or "c"')

        self.assertEqual(node.run("c"), True)
        self.assertEqual(node.run("ab"), False)
        self.assertEqual(node.run("abc"), True)
        self.assertEqual(node.run("d"), False)


def suite():
    suite = TestSuite()
    suite.addTest(TestCnoc('testErrors'))
    suite.addTest(TestCnoc('testParse'))
    return suite

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
