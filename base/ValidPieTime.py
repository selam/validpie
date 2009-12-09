#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

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
        if not isinstance(value, (dict)):
          clean = self.convertTimeDictToTimestamp(value)
        elif self.hasOption('time_format'):
          try:
            value = time.strptime(value, self.getOption('time_format'))
          except ValueError:
            raise ValidPieError(self, 'invalid', {'value': value})

          clean = self.convertTimeDictToTimestamp({
            'hour': value.hour,
            'second': value.second,
            'minute': value.minute
          });
        else:
          try:
            clean = int(value)
          except TypeError:
            raise ValidPieError(self, 'bad_format', {'value': value, 'time_format': self.getOption('time_format_error') if self.hasOption('time_format_error') else self.getOption('time_format')})
          except ValueError:
            raise ValidPieError(self, 'invalid', {'value': value})

        return clean if clean == self.getEmptyValue() else  time.strftime(clean, self.getOption('time_output'));

    def convertTimeDictToTimestamp(self, value):
        for key in ('hour', 'minute', 'second'):
            if value.has_key(key)  and value[key] is not None and re.compile('^\d+').match(str(value[key])) is None:
                raise ValidPieError(self, 'invalid', {'value' : value})

        if (self.isValueSet(value, 'second') and \
              (self.isValueSet(value, 'minute') == False or self.isValueSet(value, 'hour') == False)) or  \
              (self.isValueSet(value, 'minute') and self.isValueSet(value, 'hour') == False):
              raise ValidPieError(self, 'invalid', {'value': value})
        return int(time.mktime((0, 0, 0, int(value['hour']) if value.has_key('hour') else 0, int(value['minute']) if value.has_key('minute') else 0, int(value['second']) if value.has_key('second') else 0, 0, 0, -1)))

    def isValueSet(self, values, key):
        return True if values.has_key(key) and values[key] not in (None, '') else False
