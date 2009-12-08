#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

class ValidBoolean(ValidPieBase):
  def configure(self, options = {}, messages = {}):
      self.addOption('true_values',  ('true', 't', 'yes', 'y', 'on', '1',True, 1));
      self.addOption('false_values', ('false', 'f', 'no', 'n', 'off', '0', False, None, 0));

      self.setOption('required', False);
      self.setOption('empty_value', False);

  def doClean(self, value=None):
    if value in self.getOption('true_values'):
      return True
    elif value in self.getOption('false_values'):
      return False
    else:
      raise ValidPieError(self, 'invalid', {'value' : value})


if __name__ == '__main__':
  import unittest
  class TestValidBoolean(unittest.TestCase):
    def setUp(self):
      self.__v = ValidBoolean();

    def testValidTrueValue(self):
      self.assertEqual(self.__v.clean('true'), True);
      self.assertEqual(self.__v.clean('yes'), True);
      self.assertEqual(self.__v.clean('y'), True);
      self.assertEqual(self.__v.clean('on'), True);
      self.assertEqual(self.__v.clean('1'), True);
      self.assertEqual(self.__v.clean(True), True);
      self.assertEqual(self.__v.clean(1), True);

    def testValidFalseValue(self):
      self.assertEqual(self.__v.clean('false'), False);
      self.assertEqual(self.__v.clean('no'), False);
      self.assertEqual(self.__v.clean('n'), False);
      self.assertEqual(self.__v.clean('off'), False);
      self.assertEqual(self.__v.clean('0'), False);
      self.assertEqual(self.__v.clean(False), False);
      self.assertEqual(self.__v.clean(None), False);
      self.assertEqual(self.__v.clean(0), False);

    def testEmptyValue(self):
      self.assertEqual(self.__v.clean(), False);

    def testInvalidValue(self):
      self.__v.setOption('required', True);
      try:
        self.assertEqual(self.__v.clean([]), False)
        self.fail('list, should not be true or false')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'required')
      try:
        self.assertEqual(self.__v.clean({}), False)
        self.fail('list, should not be true or false')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'required')
      try:
        self.assertEqual(self.__v.clean('aa'), False)
        self.fail('code is fail if given value invalid string')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'invalid')
      try:
        self.assertEqual(self.__v.clean(1111), False)
        self.fail('code is fail if given value invalid integer')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'invalid')

  suite = unittest.TestLoader().loadTestsFromTestCase(TestValidBoolean)
  unittest.TextTestRunner(verbosity=2).run(suite)
