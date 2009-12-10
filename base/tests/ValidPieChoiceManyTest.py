#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

import unittest

import bootstrap
from ValidPieChoiceMany import ValidPieChoiceMany
from ValidPieError import ValidPieError

class ValidPieChoiceManyTest(unittest.TestCase):
  def setUp(self):
    try:
      self.__v = ValidPieChoiceMany();
    except Exception, e:
      self.assertEqual(e.getMessage(), 'ValidPieChoiceMany requires the following option: "choices"')
    self.__v = ValidPieChoiceMany({'choices': ['a', 'b', 'c']});

  def testValidTrueValue(self):
      self.assertEqual(self.__v.clean('a'), ['a'])
      self.assertEqual(self.__v.clean('b'), ['b'])
      self.assertEqual(self.__v.clean('c'), ['c'])

  def testValidMultipleValue(self):
      try:
         self.assertEqual(self.__v.clean(['a', 'b', 'c']), ['a', 'b', 'c']);
      except ValidPieError, e:
        self.fail(e.getMessage());

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

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieChoiceManyTest)
unittest.TextTestRunner(verbosity=2).run(suite)