from logging import log
import logging
import unittest
import os
import sys


class OelintParserTestNew(unittest.TestCase):

    RECIPE = os.path.join(os.path.dirname(__file__), "test-recipe-new_1.0.bb")
    RECIPE_NATIVE = os.path.join(os.path.dirname(__file__), "test-recipe-new-native_1.0.bb")

    def setUp(self):
        sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))

    def test_stash(self):
        from oelint_parser.cls_stash import Stash
        self.__stash = Stash()
        _stash = self.__stash.AddFile(OelintParserTestNew.RECIPE)
        self.assertTrue(_stash, msg="Stash has no items")

    def test_var_a(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTestNew.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER,
                                          attribute=Variable.ATTR_VAR,
                                          attributeValue="A")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarValue, '" X"')
            self.assertEqual(x.VarValueStripped, ' X')
            self.assertEqual(x.VarName, 'A')
            self.assertEqual(x.RawVarName, 'A')
            self.assertEqual(x.get_items(), ["X"])
            self.assertEqual(x.SubItems, ["append"])
            self.assertEqual(x.VarOp, " = ")
            self.assertEqual(x.OverrideDelimiter, ":")

    def test_var_b(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTestNew.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER,
                                          attribute=Variable.ATTR_VAR,
                                          attributeValue="B")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarValue, '"X2"')
            self.assertEqual(x.VarValueStripped, 'X2')
            self.assertEqual(x.VarName, 'B')
            self.assertEqual(x.RawVarName, 'B')
            self.assertEqual(x.get_items(), ["X2"])
            self.assertEqual(x.SubItems, ["remove", "qemuall"])
            self.assertEqual(x.VarOp, " = ")
            self.assertEqual(x.OverrideDelimiter, ":")

    def test_var_src_uri(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTestNew.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER,
                                          attribute=Variable.ATTR_VARRAW,
                                          attributeValue="SRC_URI[foo.md5sum]")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarValue, '"5c274e52576976bd70565cd72505db41"')
            self.assertEqual(x.VarValueStripped, '5c274e52576976bd70565cd72505db41')
            self.assertEqual(x.VarName, 'SRC_URI')
            self.assertEqual(x.Flag, "foo.md5sum")
            self.assertEqual(x.RawVarName, 'SRC_URI[foo.md5sum]')
            self.assertEqual(x.get_items(), ["5c274e52576976bd70565cd72505db41"])
            self.assertEqual(x.VarOp, " = ")

    def test_var_rdepends(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTestNew.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER,
                                          attribute=Variable.ATTR_VAR,
                                          attributeValue="RDEPENDS")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarValue, '"foo"')
            self.assertEqual(x.VarValueStripped, 'foo')
            self.assertEqual(x.VarName, 'RDEPENDS')
            self.assertEqual(x.VarNameComplete, 'RDEPENDS:${PN}-test')
            self.assertEqual(x.RawVarName, 'RDEPENDS')
            self.assertEqual(x.get_items(), ["foo"])
            self.assertEqual(x.SubItems, ["${PN}-test"])
            self.assertEqual(x.VarOp, " += ")
            self.assertEqual(x.OverrideDelimiter, ":")

    def test_function(self):
        from oelint_parser.cls_item import Function
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTestNew.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Function.CLASSIFIER)

        self.assertTrue(_stash, msg="Stash has no items")
        self.assertEqual(_stash[0].IsPython, False)
        self.assertEqual(_stash[0].IsFakeroot, False)
        self.assertEqual(_stash[0].FuncName, "do_example")
        self.assertEqual(_stash[0].FuncNameComplete,
                         "do_example:prepend:qemux86-64:poky")
        self.assertIn('bbwarn "This is an example warning"',
                      _stash[0].FuncBody)
        self.assertIn("prepend", _stash[0].SubItems)
        self.assertEqual(_stash[0].IsAppend(), True)
        self.assertEqual(_stash[0].FuncBodyStripped,
                         'bbwarn "This is an example warning"')
        self.assertEqual(_stash[0].GetDistroEntry(), "poky")
        self.assertEqual(_stash[0].GetMachineEntry(), "qemux86-64")
        self.assertEqual(_stash[0].OverrideDelimiter, ":")

    def test_var_bp(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTestNew.RECIPE_NATIVE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER,
                                          attribute=Variable.ATTR_VAR,
                                          attributeValue="X")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            logging.warning(x.VarValueStripped)
            value = expand_term(self.__stash, OelintParserTestNew.RECIPE, x.VarValueStripped)
            self.assertEqual(value, "test-recipe-new-1.0")

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER,
                                          attribute=Variable.ATTR_VAR,
                                          attributeValue="Y")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            logging.warning(x.VarValueStripped)
            value = expand_term(self.__stash, OelintParserTestNew.RECIPE, x.VarValueStripped)
            self.assertEqual(value, "test-recipe-new-1.0")

    def test_var_p(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTestNew.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER,
                                          attribute=Variable.ATTR_VAR,
                                          attributeValue="Y")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            value = expand_term(self.__stash, OelintParserTestNew.RECIPE, x.VarValueStripped)
            self.assertEqual(value, "test-recipe-new-1.0")


if __name__ == "__main__":
    unittest.main()
