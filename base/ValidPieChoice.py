#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

import collections

class ValidChoice(ValidPieBase):
    def configure(self, options = {}, messages = {}):
        self.addRequiredOption('choices')
        self.addOption('multiple', False)

    def doClean(self, value):
        choices = self.getOption('choices')

        if isinstance(choices, collections.Callable) or hasattr(choices, '__call__'):
          choices = choices();

        if self.getOption('multiple'):

           if not isinstance(value, (tuple, list, dict)):
              value = [value]
           for v in value:
             if not self.inChoices(v, choices):
                raise ValidPieError(self, 'invalid', {'value': v})
        else:
          if not self.inChoices(value, choices):
            raise ValidPieError(self, 'invalid', {'value': value})

        return value

    def inChoices(self, value, choices):
        return True if value in choices else False

if __name__ == '__main__':
  import unittest
  class TestValidChoice(unittest.TestCase):
    def setUp(self):
      try:
        self.__v = ValidPieChoice();
      except Exception, e:
        self.assertEqual(e.getMessage(), 'ValidChoice requires the following option: "choices"')
      self.__v = ValidPieChoice({'choices': ['a', 'b', 'c']});

    def testValidTrueValue(self):
        self.assertEqual(self.__v.clean('a'), 'a')
        self.assertEqual(self.__v.clean('b'), 'b')
        self.assertEqual(self.__v.clean('c'), 'c')

    def testValidCallableValue(self):
        class callableValue(object):
            def __call__(self):
              return ['a', 'b']

        callableObject = callableValue();

        self.__v.setOption('choices', callableObject)
        self.assertEqual(self.__v.clean('a'), 'a')

    def testEmptyValue(self):
        try:
          self.assertEqual(self.__v.clean(''), '')
        except ValidPieError, e:
          self.assertEqual(e.getMessage(), 'required')
    def testInvalidValue(self):
        try:
          self.assertEqual(self.__v.clean('aa'), 'a')
        except ValidPieError, e:
          self.assertEqual(e.getMessage(), 'invalid')

  suite = unittest.TestLoader().loadTestsFromTestCase(TestValidChoice)
  unittest.TextTestRunner(verbosity=2).run(suite)

