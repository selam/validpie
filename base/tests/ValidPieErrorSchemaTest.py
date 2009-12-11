#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

import unittest

import bootstrap
from ValidPieErrorSchema import ValidPieErrorSchema
from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

class ValidPieIdentity(ValidPieBase):
    def configure(self, options = {}, messages = {}):
        self.addOption('foo', 'bar')
        self.addMessage('foo', 'bar')

    def testIsEmpty(self, value):
        return self.isEmpty(value)

    def doClean(self, value):
        return value

class ValidPieErrorSchemaTest(unittest.TestCase):
        def setUp(self):
            self.__v1 = ValidPieIdentity()
            self.__v2 = ValidPieIdentity()
            self.__e1 = ValidPieError(self.__v1, 'required', {'value': '', 'required': True})
            self.__e2 = ValidPieError(self.__v2, 'required', {'value': None, 'required': True})
            self.__e  = ValidPieErrorSchema(self.__v1)

        def testInit(self):
            self.assertEqual(isinstance(self.__e.getValidPie(), ValidPieIdentity), True)
            self.assertEqual(self.__e.getValidPie(), self.__v1)
            e = ValidPieErrorSchema(self.__v1, {'e1': self.__e1, 'e2': self.__e2})
            self.assertEqual(e.getErrors(), [self.__e1, self.__e2])

        def testAddError(self):
            self.__e.addError(self.__e1)
            self.__e.addError(self.__e2, 'e2')
            self.__e.addError(self.__e1, '2')
            self.assertEqual(self.__e.getErrors(), [self.__e1, self.__e2, self.__e1])

        def testEmbededErrors(self):
            es1 = ValidPieErrorSchema(self.__v1, {'e1': self.__e1, 'e2': self.__e2})
            es = ValidPieErrorSchema(self.__v1, {'e1': self.__e1, 'e2': es1})

            self.assertEqual(es.getCode(), ' e1 [required] e2 [ e1 [required] e2 [required]]')
            es.addError(self.__e2, 'e1')
            self.assertEqual(es.getCode(), ' e1 [required required ] e2 [ e1 [required] e2 [required]]')
            es.addError(self.__e2)
            self.assertEqual(es.getCode(), 'required e1 [required required ] e2 [ e1 [required] e2 [required]]')
            es.addError(es1, 'e3')
            self.assertEqual(es.getCode(), 'required e1 [required required ] e3 [ e1 [required] e2 [required]] e2 [ e1 [required] e2 [required]]')

        def testAddErrors(self):
            self.__e.addError(self.__e1)
            self.__e.addError(self.__e2, '1')
            es = ValidPieErrorSchema(self.__v1)
            es.addErrors(self.__e)
            self.assertEqual(es.getGlobalErrors(), [self.__e1])
            self.assertEqual(es.getNamedErrors(), {'1': self.__e2})

        def testGetGlobalErrors(self):
            self.__e.addError(self.__e1)
            self.__e.addError(self.__e2, 'e2')
            self.__e.addError(self.__e1, '2')
            self.assertEqual(self.__e.getGlobalErrors(), [self.__e1])

        def testGetNamedErrors(self):
            self.__e.addError(self.__e1)
            self.__e.addError(self.__e2, 'e2')
            self.__e.addError(self.__e1, '2')
            self.assertEqual(self.__e.getNamedErrors(), {'e2': self.__e2, '2': self.__e1})

        def testGetValue(self):
            self.assertEqual(self.__e.getValue(), None)

        def testGetArguments(self):
            self.assertEqual(self.__e.getArguments(), {})
            self.assertEqual(self.__e.getArguments(True), {})

        def testGetMessageFormat(self):
            self.assertEqual(self.__e.getMessageFormat(), '')

        def testGetMessage(self):
            es1 = ValidPieErrorSchema(self.__v1, {'e1': self.__e1, 'e2': self.__e2})
            es = ValidPieErrorSchema(self.__v1, {'e1': self.__e1, 'e2': es1})

            self.assertEqual(es.getMessage(), ' e1 [required] e2 [ e1 [required] e2 [required]]')
            es.addError(self.__e2, 'e1')
            self.assertEqual(es.getMessage(), ' e1 [required required ] e2 [ e1 [required] e2 [required]]')
            es.addError(self.__e2)
            self.assertEqual(es.getMessage(), 'required e1 [required required ] e2 [ e1 [required] e2 [required]]')
            es.addError(es1, 'e3')
            self.assertEqual(es.getMessage(), 'required e1 [required required ] e3 [ e1 [required] e2 [required]] e2 [ e1 [required] e2 [required]]')

        def testGetCode(self):
            es1 = ValidPieErrorSchema(self.__v1, {'e1': self.__e1, 'e2': self.__e2})
            es = ValidPieErrorSchema(self.__v1, {'e1': self.__e1, 'e2': es1})
            self.assertEqual(es.getCode(), ' e1 [required] e2 [ e1 [required] e2 [required]]')
            es.addError(self.__e2, 'e1')
            self.assertEqual(es.getCode(), ' e1 [required required ] e2 [ e1 [required] e2 [required]]')
            es.addError(self.__e2)
            self.assertEqual(es.getCode(), 'required e1 [required required ] e2 [ e1 [required] e2 [required]]')
            es.addError(es1, 'e3')
            self.assertEqual(es.getCode(), 'required e1 [required required ] e3 [ e1 [required] e2 [required]] e2 [ e1 [required] e2 [required]]')

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieErrorSchemaTest)
unittest.TextTestRunner(verbosity=2).run(suite)