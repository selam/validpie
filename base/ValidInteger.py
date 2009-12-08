#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

class ValidInteger(ValidPieBase):

  def configure(self, options ={}, messages = {}):
    self.addMessage('max', '"%(value)s" must be at most %(max)s.')
    self.addMessage('min', '"%(value)s" must be at least %(min)s.')

    self.addOption('min');
    self.addOption('max');

    self.setMessage('invalid', '"%(value)s" is not an integer.')


  def doClean(self, value):
    try:
      clean = int(value);
    except ValueError:
      raise ValidPieError(self, 'invalid', {'value': value})

    if (str(clean) != value):
      ValidPieError(self, 'invalid', {'value' : value});

    if self.hasOption('max') and clean > self.getOption('max'):
      raise ValidPieError(self, 'max', {'value' : value, 'max' :self.getOption('max')})

    if self.hasOption('min') and clean < self.getOption('min'):
      raise ValidPieError(self, 'min', {'value' : value, 'min' :self.getOption('min')})

    return clean;

if __name__ == '__main__':
  import unittest

  class TestValidInteger(unittest.TestCase):
    def setUp(self):
        self.__v = ValidInteger({'min': 1, 'max': 5}, {'invalid': 'invalid'});

    def testValidValue(self):
        self.assertEqual(self.__v.clean('1'), 1)

    def testInvalidValue(self):
        try:
          self.__v.clean('si')
          self.fail('fail if given value is string (a-z)')
        except ValidPieError, e:
          self.assertEqual(e.getMessage(), 'invalid')
        try:
          self.__v.clean('A')
          self.fail('fail if given value is string (A-Z)')
        except ValidPieError, e:
          self.assertEqual(e.getMessage(), 'invalid')

  suite = unittest.TestLoader().loadTestsFromTestCase(TestValidInteger)
  unittest.TextTestRunner(verbosity=2).run(suite)