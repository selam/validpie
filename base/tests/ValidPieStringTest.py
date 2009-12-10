#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

import unittest

import bootstrap
from ValidPieString import ValidPieString
from ValidPieError import ValidPieError

class ValidPieStringTest(unittest.TestCase):
        def setUp(self):
          self.__v = ValidPieString({'required': True, 'min_length': 5, 'max_length': 15}, {'invalid': 'invalid value', 'min_length': 'value too short', 'max_length': 'value too long'});

        def testTooShortValue(self):
          try:
            self.__v.clean('str')
            self.fail('validator not calculate len value')
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), 'value too short')

        def testTooLongValue(self):
          try:
            self.__v.clean('strstrstrstrstrstr')
            self.fail('validator not calculate len value')
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), 'value too long')

        def testInvalidValue(self):
          try:
            value = self.__v.clean(['a'])
            self.fail('validator is not casting string value')
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), 'invalid value')
          try:
            value = self.__v.clean({'as': 'a'})
            self.fail('validator is not casting string value')
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), 'invalid value')
          try:
            value = self.__v.clean(('ddddddd',))
            self.fail('validator is not casting string value')
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), 'invalid value')

        def testValidValue(self):
          try:
            value = self.__v.clean("['a']")
            self.assertEqual(value, "['a']")
            value = self.__v.clean("['ş']")
            self.assertEqual(value, u"['ş']")
          except ValidPieError, e:
            self.fail('validator is not casting string value')

        def testValidValue(self):
          try:
            value = self.__v.clean("şğüIİ")
            self.assertEqual(value, u"şğüIİ")
            self.assertEqual(len(value), 5);
            self.assertEqual(isinstance(value, unicode), True)
            value = self.__v.clean("asdfg")
            self.assertEqual(value, u"asdfg")
            self.assertEqual(len(value), 5);
            self.assertEqual(isinstance(value, unicode), True)
            self.assertEqual(self.__v.clean(55555), '55555')
            self.assertEqual(self.__v.clean(0.0001), '0.0001')
          except ValidPieError, e:
            self.fail('validator is not casting string value %s ' % e.getMessage())

        def testNotRequiredValue(self):
          self.__v.setOption('required', False)
          try:
            self.assertEqual(self.__v.clean(""), '')
            self.assertEqual(self.__v.clean(None), '')
            self.assertEqual(self.__v.clean({}), '')
            self.assertEqual(self.__v.clean([]), '')
            self.assertEqual(self.__v.clean(()), '')
            self.assertEqual(self.__v.clean('ayşegülİçerken'), u'ayşegülİçerken')
          except ValidPieError, e:
            self.fail('validator is not casting string value %s ' % e.getMessage())

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieStringTest)
unittest.TextTestRunner(verbosity=2).run(suite)