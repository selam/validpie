#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase


class ValidPieNumber(ValidPieBase):
  def configure(self, options ={}, messages = {}):
    self.addMessage('max', '"%(value)s" must be at most %(max)s.');
    self.addMessage('min', '"%(value)s" must be at least %(min)s.');
    self.addOption('min');
    self.addOption('max');
    self.setMessage('invalid', '"%(value)s" is not a number.');

  def doClean(self, value):
    if not isinstance(value, (unicode, str, int, float)):
        raise ValidPieError(self, 'invalid', {'value': value})
    elif isinstance(value, (unicode, str)):
        if not value.isdigit():
          raise ValidPieError(self, 'invalid', {'value': value})
    try:
      clean = float(value);
    except TypeError:
      raise ValidPieError(self, 'invalid', {'value': value})

    if self.hasOption('max') and clean > self.getOption('max'):
      raise ValidPieError(self, 'max', {'value' : value, 'max' : self.getOption('max')})

    if self.hasOption('min') and clean < self.getOption('min'):
      raise ValidPieError(self, 'min', {'value' : value, 'min' : self.getOption('min')});

    return clean;
if __name__ == '__main__':
  import unittest
  class TestValidNumber(unittest.TestCase):
      def setUp(self):
        self.__v = ValidPieNumber();

      def testValidValue(self):
        self.assertEqual(self.__v.clean('1'), 1.0)
        self.assertEqual(self.__v.clean(1), 1.0)
        self.assertEqual(self.__v.clean(0), 0.0)
        self.assertEqual(self.__v.clean(2), 2.0)

  suite = unittest.TestLoader().loadTestsFromTestCase(TestValidNumber)
  unittest.TextTestRunner(verbosity=2).run(suite)
