#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist


import datetime
import re
import time

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

class ValidPieDate(ValidPieBase):
    def configure(self, options={}, messages = {}):
        self.addMessage('bad_format', '"%(value)s" does not match the date format (%(date_format)s).')
        self.addMessage('max', 'The date must be before %(max)s.')
        self.addMessage('min', 'The date must be after %(min)s.')
        self.setMessage('invalid', 'Invalid date %(value)s.')

        self.addOption('date_format', None)
        self.addOption('with_time', False)
        self.addOption('date_output', '%Y-%m-%d')
        self.addOption('datetime_output', '%Y-%m-%d %H:%i:%s')
        self.addOption('date_format_error')
        self.addOption('min', None)
        self.addOption('max', None)
        self.addOption('date_format_range_error', '%d/%m/%Y %H:%i:%s')

    def doClean(self, value):
        if isinstance(value, (dict)):
          clean = self.convertDateDictToTimestamp(value)
        elif self.hasOption('date_format'):
          try:
            value = datetime.datetime.strptime(value, self.getOption('date_format'))
          except ValueError:
            raise ValidPieError(self, 'invalid', {'value': value})
          clean = self.convertDateDictToTimestamp({'year': value.year, 'month': value.month, 'day': value.day, 'hour': value.hour, 'minute': value.minute, 'second': value.second})
        else:
          try:
            clean = int(value)
          except TypeError:
            raise ValidPieError(self, 'bad_format', {'value': value, 'date_format': self.getOption('date_format_error') if self.hasOption('date_format_error') else self.getOption('date_format')})
          except ValueError:
            raise ValidPieError(self, 'invalid', {'value': value})

        if self.hasOption('max') and clean > self.getOption('max'):
            raise ValidPieError(self, 'max', {'value' : value, 'max' : datetime.datetime.strftime(self.getOption('date_format_range_error'), datetime.datetime.fromtimestamp(clean))})

        if self.hasOption('min') and clean < self.getOption('min'):
            raise ValidPieError(self, 'min', {'value' : value, 'min': datetime.datetime.strftime(self.getOption('date_format_range_error'), datetime.datetime.fromtimestamp(clean))})

        return clean if clean == self.getEmptyValue() else  datetime.datetime.strftime(datetime.datetime.fromtimestamp(int(clean)), self.getOption('datetime_output')  if self.getOption('with_time') else self.getOption('date_output'));


    def convertDateDictToTimestamp(self, value):
        for key in ['year', 'month', 'day', 'hour', 'minute', 'second']:

          if value.has_key(key)  and value[key] is not None and re.compile('^\d+').match(str(value[key])) is None:
              raise ValidPieError(self, 'invalid', {'value' : value})

        empties = (0  if value.has_key('year') else 1) + \
                  (0  if value.has_key('month')  else 1) + \
                  (0  if value.has_key('day')  else 1)

        if empties > 0 and empties < 3:
          raise ValidPieError(self, 'invalid', {'value' :value})
        elif 3 == empties:
          return self.getEmptyValue()
        try:
          date = time.mktime((int(value['year']), int(value['month']), int(value['day']),  0, 0, 0, 0, 0, 0))
          if time.localtime(date)[:3] != (int(value['year']), int(value['month']), int(value['day']),):
            raise ValidPieError(self, 'invalid', {'value': value})
        except Exception, e:
          raise ValidPieError(self, 'invalid', {'value': value})

        if self.getOption('with_time'):
           if (self.isValueSet(value, 'second') and \
              (self.isValueSet(value, 'minute') == False or self.isValueSet(value, 'hour') == False)) or  \
              (self.isValueSet(value, 'minute') and self.isValueSet(value, 'hour') == False):
              raise ValidPieError(self, 'invalid', {'value': value})
           clean = time.mktime((int(value['year']), int(value['month']), int(value['day']), int(value['hour']) if value.has_key('hour') else 0, int(value['minute']) if value.has_key('minute') else 0, int(value['second']) if value.has_key('second') else 0, 0, 0, -1))
        else:
          clean = date

        return clean

    def isValueSet(self, values, key):
        return True if values.has_key(key) and values[key] not in (None, '') else False


if __name__ == '__main__':
  import unittest
  class TestValidPieDate(unittest.TestCase):
        def setUp(self):
            self.__v = ValidPieDate();

        def testValidDate(self):
            self.assertEqual(self.__v.clean({'year': '2007', 'month': '10', 'day': '10'}), '2007-10-10')
            self.__v.setOption('date_format', '%Y-%m-%d')
            self.assertEqual(self.__v.clean('2007-10-10'), '2007-10-10')
            self.assertEqual(self.__v.clean('2007-10-10'), '2007-10-10')
            self.__v.setOption('with_time', True)
            self.__v.setOption('date_format', '%Y-%m-%d %H')
            self.__v.addOption('datetime_output', '%Y-%m-%d %H')
            self.assertEqual(self.__v.clean('2007-10-10 23'), '2007-10-10 23')
        def testInvalidDate(self):
            self.__v.setOption('date_format', None)
            try:
              self.__v.clean({'year': '2007', 'month': '2', 'day': '31'})
            except ValidPieError, e:
              self.assertEqual(e.getMessage(), "Invalid date {'month': '2', 'day': '31', 'year': '2007'}.")

            self.__v.setOption('date_format', '%Y-%m-%d')
            try:
              self.__v.clean('2009-2-30')
            except ValidPieError, e:
              self.assertEqual(e.getMessage(), "Invalid date 2009-2-30.")
            self.__v.setOption('date_format', '%Y-%m-%d')
            try:
              self.__v.clean('test')
            except ValidPieError, e:
              self.assertEqual(e.getMessage(), "Invalid date test.")
            self.__v.setOption('date_format', None)
            try:
              self.__v.clean('test')
            except ValidPieError, e:
              self.assertEqual(e.getMessage(), "Invalid date test.")
            try:
              self.__v.clean({'year': 2007})
            except ValidPieError, e:
              self.assertEqual(e.getMessage(), "Invalid date {'year': 2007}.")
            self.__v.setOption('with_time', True)
            try:
              self.__v.clean({'year': 2007, 'month': 3, 'day': '4', 'second': '55'})
            except ValidPieError, e:
              self.assertEqual(e.getMessage(), "Invalid date {'second': '55', 'month': 3, 'day': '4', 'year': 2007}.")
            try:
              self.__v.clean({'year': 2007, 'month': 3, 'day': '4', 'second': '55', 'minute': '11'})
            except ValidPieError, e:
              self.assertEqual(e.getMessage(), "Invalid date {'second': '55', 'month': 3, 'day': '4', 'minute': '11', 'year': 2007}.")
  suite = unittest.TestLoader().loadTestsFromTestCase(TestValidPieDate)
  unittest.TextTestRunner(verbosity=2).run(suite)