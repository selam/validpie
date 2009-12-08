#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist


from ValidPieChoice import ValidPieChoice

class ValidChoiceMany(ValidPieChoice):
  def configure(self, options = {}, messages = {}):
    ValidPieChoice.configure(self, options, messages)
    self.addOption('multiple', True)



if __name__ == '__main__':
  import unittest
  from ValidPieError import ValidPieError
  class TestValidChoiceMany(unittest.TestCase):
    def setUp(self):
      try:
        self.__v = ValidPieChoiceMany();
      except Exception, e:
        self.assertEqual(e.getMessage(), 'ValidChoiceMany requires the following option: "choices"')
      self.__v = ValidPieChoiceMany({'choices': ['a', 'b', 'c']});

    def testValidTrueValue(self):
        self.assertEqual(self.__v.clean('a'), ['a'])
        self.assertEqual(self.__v.clean('b'), ['b'])
        self.assertEqual(self.__v.clean('c'), ['c'])

    def testValidMultipleValue(self):

        try:
          self.__v.clean(['a', 'b', 'c']);
        except ValidPieError, e:
          self.fail(e.getMessage());
        #self.assertEqual(, '')


    def testValidCallableValue(self):
        class callableValue(object):
            def __call__(self):
              return ['a', 'b']

        callableObject = callableValue();

        self.__v.setOption('choices', callableObject)
        try:
          self.assertEqual(self.__v.clean(['a', 'b']), ['a', 'b'])
        except ValidPieError:
          self.fail('callableobject is fail if given value is multiple')

    def testEmptyValue(self):
        try:
          self.assertEqual(self.__v.clean(''), '')
        except ValidPieError, e:
          self.assertEqual(e.getMessage(), 'required')
    def testInvalidValue(self):
        try:
          self.assertEqual(self.__v.clean('a'), ['a'])
        except ValidPieError, e:
          self.assertEqual(e.getMessage(), 'invalid')

  suite = unittest.TestLoader().loadTestsFromTestCase(TestValidChoiceMany)
  unittest.TextTestRunner(verbosity=2).run(suite)
