#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

import unittest

import bootstrap
from ValidPieSchema import ValidPieSchema
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

class FooValidPieSchema(ValidPieSchema):
  def setUp(self, options = {}, messages = {}):
      self.setValidPies({
        'foo': ValidPieIdentity()
      })

class ValidPieSchemaTest(unittest.TestCase):
      def testBind(self):
        schema = FooValidPieSchema()
        schema.clean({
          'foo': 'b'
        })

        self.assertEqual(schema.isValid(), True)

      def testBindWithFalse(self):
        schema = FooValidPieSchema()
        schema.clean({
          'foo': 'b',
          'bar': '?'
        })

        self.assertEqual(schema.isValid(), False)
        for error in schema.getErrors():
          self.assertEqual(isinstance(error, ValidPieError), True)
          self.assertEqual(error.getMessage(), 'Unexpected extra field named "bar".')
          self.assertEqual(error.getCode(), 'extra_fields')
          self.assertEqual(error.getArguments(), {'field': 'bar'})
      def testNamedError(self):
        schema = FooValidPieSchema()
        schema.clean({
          'foo': 'b',
          'bar': '?'
        })

        for error in schema.getErrorSchema().getGlobalErrors():
          self.assertEqual(isinstance(error, ValidPieError), True)
          self.assertEqual(error.getMessage(), 'Unexpected extra field named "bar".')
          self.assertEqual(error.getCode(), 'extra_fields')
          self.assertEqual(error.getArguments(), {'field': 'bar'})

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieSchemaTest)
unittest.TextTestRunner(verbosity=2).run(suite)