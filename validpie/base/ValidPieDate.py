#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

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
        self.addOption('datetime_output', '%Y-%m-%d %H:%M:%S')
        self.addOption('date_format_error')
        self.addOption('min', None)
        self.addOption('max', None)
        self.addOption('date_format_range_error', '%d/%m/%Y %H:%M:%S')

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