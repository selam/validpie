#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import unittest

import bootstrap
from Exceptions import InvalidArgumentException
from ValidPieBase import ValidPieBase
from ValidPieError import ValidPieError

class ValidPieIdentity(ValidPieBase):
    def configure(self, options = {}, messages = {}):
        self.addOption('foo', 'bar')
        self.addMessage('foo', 'bar')

    def testIsEmpty(self, value):
        return self.isEmpty(value)

    def doClean(self, value):
        return value

class ValidPieIdentityWithRequired(ValidPieBase):
      def configure(self, options={}, messages={}):
          self.addRequiredOption('foo')

      def doClean(self, value):
          return value

class ValidPieBaseTest(unittest.TestCase):
      def testDefaultOptions(self):
        v = ValidPieIdentity()
        self.assertEqual(v.getOption('foo'), 'bar')

      def testOverrideDefaultOptionValues(self):
        v = ValidPieIdentity({'foo': 'foobar'})
        self.assertEqual(v.getOption('foo'), 'foobar')

      def testDefaultMessage(self):
        v = ValidPieIdentity()
        self.assertEqual(v.getMessage('foo'), 'bar')

      def testOverrideDefaultMessages(self):
        v = ValidPieIdentity({}, {'foo': 'foobar'})
        self.assertEqual(v.getMessage('foo'), 'foobar')

      def testNonExistantArgument(self):
        try:
          v = ValidPieIdentity({'nonexistant': False, 'foo': 'foobar', 'anothernonexistant': 'bar', 'required': True })
          self.fail('__init__() throws an InvalidArgumentException if you pass some non existant options')
        except InvalidArgumentException, e:
          self.assertEqual(e.getMessage(), 'ValidPieIdentity does not support the following options "anothernonexistant, nonexistant"')

      def testNonExistantErrorCodes(self):
        try:
          v = ValidPieIdentity({}, {'required': 'This is required.', 'nonexistant': 'foo', 'anothernonexistant': False})
          self.fail('__init__() throws an InvalidArgumentException if you pass some non existant error codes')
        except InvalidArgumentException, e:
          self.assertEqual(e.getMessage(), 'ValidPieIdentity does not support the following error codes "anothernonexistant, nonexistant"')

      def testRequiredOptions(self):
          v = ValidPieIdentityWithRequired({'foo' : 'bar'})
          self.assertEqual(v.getRequiredOptions(), ['foo'])

      def testRequiredOptionsNotGiven(self):
          try:
            v = ValidPieIdentityWithRequired()
            self.fail('__init__() throws an InvalidArgumentException if you dont pass some required options')
          except InvalidArgumentException, e:
            self.assertEqual(e.getMessage(), 'ValidPieIdentityWithRequired requires the following option: "foo"')

      def testCleanValue(self):
          v = ValidPieIdentity()
          self.assertEqual(v.clean('foo'), 'foo')
          try:
            self.assertEqual(v.clean(''), '')
            self.fail('clean() throws a ValidPieError exception if the data does not validate')
          except ValidPieError, e:
            self.assertEqual(e.getCode(), 'required')
          self.assertEqual(v.clean('  foo  '), '  foo  ')
          v.setOption('trim', True)
          self.assertEqual(v.clean('  foo  '), 'foo')

      def testIsEmpty(self):
          v = ValidPieIdentity()
          self.assertEqual(v.testIsEmpty(None), True)
          self.assertEqual(v.testIsEmpty(''), True)
          self.assertEqual(v.testIsEmpty({}), True)
          self.assertEqual(v.testIsEmpty([]), True)
          self.assertEqual(v.testIsEmpty(['a']), False)
          self.assertEqual(v.testIsEmpty({'a':'a'}), False)
          self.assertEqual(v.testIsEmpty(' '), False)
          self.assertEqual(v.testIsEmpty(True), False)
          self.assertEqual(v.testIsEmpty(False), False)
          self.assertEqual(v.testIsEmpty(0), False)

      def testGetEmptyValue(self):
        v = ValidPieIdentity()
        v.setOption('required', False)
        v.setOption('empty_value', 'defaultnullvalue')
        self.assertEqual(v.clean(''), 'defaultnullvalue')
        v.setOption('empty_value', None)
        self.assertEqual(v.clean(''), None)
        self.assertEqual(v.clean(None), None)

      def testOptionChanges(self):
        v = ValidPieIdentity()
        v.setOption('required', False)
        self.assertEqual(v.getOption('required'), False)
        v.setOption('required', True)
        self.assertEqual(v.getOption('required'), True)

      def testMessageChanges(self):
        v = ValidPieIdentity()
        self.assertEqual(v.getMessage('required'), 'required')
        v.setMessage('required', 'test')
        self.assertEqual(v.getMessage('required'), 'test')

      def testSetOption(self):
        v = ValidPieIdentity()
        try:
          v.setOption('foobar', 'foo')
          self.fail('setOption throws an InvalidArgumentException if the option is not registered')
        except InvalidArgumentException, e:
          self.assertEqual(e.getMessage(), 'ValidPieIdentity does not support the following option: "foobar"')

      def testHasOption(self):
        v = ValidPieIdentity()
        self.assertEqual(v.hasOption('required'), True)
        self.assertEqual(v.hasOption('nonexistant'), False)

      def testGetOption(self):
        v = ValidPieIdentity()
        self.assertEqual(v.getOption('required'), True)
        self.assertEqual(v.getOption('nonexistant'), None)

      def testAddOption(self):
        v = ValidPieIdentity()
        v.addOption('foobar')
        v.setOption('foobar', 'foo')
        self.assertEqual(v.getOption('foobar'), 'foo')

      def testSetOptionsGetOptions(self):
        v = ValidPieIdentity()
        v.setOptions({'required': True, 'trim': False})
        self.assertEqual(v.getOptions(), {'required': True, 'trim': False})

      def testGetMessages(self):
        v = ValidPieIdentity()
        self.assertEqual(v.getMessages(), {'required': 'required', 'invalid': 'invalid', 'foo': 'bar'})

      def testGetMessage(self):
        v = ValidPieIdentity()
        self.assertEqual(v.getMessage('required'), 'required')

      def testSetMessage(self):
        v = ValidPieIdentity()
        v.setMessage('required', 'this field required')
        try:
          v.clean('')
        except ValidPieError, e:
          self.assertEqual(e.getMessage(), 'this field required')
        try:
          v.setMessage('foobar', 'foo')
        except InvalidArgumentException, e:
          self.assertEqual(e.getMessage(), 'ValidPieIdentity does not support the following error code: "foobar"')

      def testSetMessages(self):
        v = ValidPieIdentity()
        v.setMessages({'required': 'this field required'})
        self.assertEqual(v.getMessages(), {'required': 'this field required'})

      def testAddMessage(self):
        v = ValidPieIdentity()
        v.addMessage('foobar', 'foo')
        v.setMessage('foobar', 'bar')
        self.assertEqual(v.getMessage('foobar'), 'bar')

      def testGetErrorCodes(self):
        v = ValidPieIdentity()
        self.assertEqual(v.getErrorCodes(), ['required', 'foo', 'invalid'])

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieBaseTest)
unittest.TextTestRunner(verbosity=2).run(suite)