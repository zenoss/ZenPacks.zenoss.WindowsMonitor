###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import unittest
from Products.ZenTestCase.BaseTestCase import BaseTestCase
from ZenPacks.zenoss.WindowsMonitor.winreg import extractUnicodeString

class TestUnicodeStrings(BaseTestCase):

    # test the extraction of a Unicode string that ends in a NUL
    def testNulTerminated(self):
        testStr = u'_Total\u0000'
        bytes = testStr.encode("utf-16-le")
        str = extractUnicodeString(bytes, 0, len(bytes), "utf-16-le")
        self.assert_(str == u'_Total')

        testStr = u'yet another\u0000blah blah blah'
        bytes = testStr.encode("utf-16-le")
        str = extractUnicodeString(bytes, 0, len(bytes), "utf-16-le")
        self.assert_(str == 'yet another')

    # test the extraction of a Unicode string that does not end in a NUL
    # but simply occupies the full buffer space
    def testUnterminated(self):
        testStr = u'_Total'
        bytes = testStr.encode("utf-16-le")
        str = extractUnicodeString(bytes, 0, len(bytes), "utf-16-le")
        self.assert_(str == u'_Total')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUnicodeStrings))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
