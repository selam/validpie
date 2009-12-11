#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import re
import time

from ValidPieBase import ValidPieBase
from ValidPieError import ValidPieError

class ValidPieTime(ValidPieBase):
    def configure(self, options = {}, messages = {}):
        self.addMessage('bad_format', '"%(value)s" does not match the time format (%(time_format)s).');

        self.addOption('time_format', '%H:%M:%S');
        self.addOption('time_output', '%H:%M:%S');
        self.addOption('time_format_error');

    def doClean(self, value):
        if isinstance(value, (dict)):
          clean = self.convertTimeDictToTimestamp(value)
        elif self.hasOption('time_format'):
          try:
            value = time.strptime(value, self.getOption('time_format'))
          except ValueError:
            raise ValidPieError(self, 'invalid', {'value': value})

          clean = self.convertTimeDictToTimestamp({
            'hour': value.tm_hour,
            'second': value.tm_sec,
            'minute': value.tm_min
          });
        else:
          try:
            clean = int(value)
          except TypeError:
            raise ValidPieError(self, 'bad_format', {'value': value, 'time_format': self.getOption('time_format_error') if self.hasOption('time_format_error') else self.getOption('time_format')})
          except ValueError:
            raise ValidPieError(self, 'invalid', {'value': value})

        return clean if clean == self.getEmptyValue() else  time.strftime(self.getOption('time_output'), time.localtime(clean));

    def convertTimeDictToTimestamp(self, value):
        for key in ('hour', 'minute', 'second'):
            if value.has_key(key)  and value[key] is not None and value[key] != '' and re.compile('^\d+').match(str(value[key])) is None:
                raise ValidPieError(self, 'invalid', {'value' : value})

        if not self.isValueSet(value, 'second') and not self.isValueSet(value, 'minute') and not self.isValueSet(value, 'hour'):
            if self.getOption('required'):
                raise ValidPieError(self, 'required', {'value' : value})
            else:
              return self.getEmptyValue()

        if (self.isValueSet(value, 'second') and \
              (self.isValueSet(value, 'minute') == False or self.isValueSet(value, 'hour') == False)) or  \
              (self.isValueSet(value, 'minute') and self.isValueSet(value, 'hour') == False):
              raise ValidPieError(self, 'invalid', {'value': value})

        return int(time.mktime((0, 0, 0, self.getValue(value, 'hour'), self.getValue(value, 'minute'), self.getValue(value, 'second'), 0, 0, -1)))

    def getValue(self, values, key):
        return int(values[key]) if values.has_key(key) and values[key] not in (None, '') else 0

    def isValueSet(self, values, key):
        return True if values.has_key(key) and values[key] not in (None, '') else False
