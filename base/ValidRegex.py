#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase
from ValidString import ValidString

class ValidRegex(ValidString):
  def configure(self, options = {}, messages = {}):
      super(ValidString, self).configure(options, messages)
      self.addRequiredOption('pattern')


  def doClean(self, value):
      clean = ValidString.doClean(self, value)
      import re
      matchResult = re.compile(self.getOption('pattern')).match(clean)
      if not matchResult:
        raise ValidPieError(self, 'invalid', {'value': value})

      return clean;

if __name__ == '__main__':
  import unittest
  class TestValidRegex(unittest.TestCase):
        def setUp(self):
          self.__v = ValidRegex({'pattern': r'deneme'}, {'invalid': 'invalid "%(value)s"'})

        def testValidValue(self):
          value = self.__v.clean('deneme');
          self.assertEqual(value, u'deneme')

        def testInvalidValue(self):
          try:
            value = self.__v.clean('sarkimi soylerken');
            self.fail('fail if not match')
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), u'invalid "sarkimi soylerken"')

  suite = unittest.TestLoader().loadTestsFromTestCase(TestValidRegex)
  unittest.TextTestRunner(verbosity=2).run(suite)