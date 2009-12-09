#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from ValidPieBase import ValidPieBase
from ValidPieError import ValidPieError

class ValidPieDateRange(ValidPieBase):
    def configure(self, options = {}, messages = {}):
        self.addMessage('invalid', 'The begin date must be before the end date.')

        self.addRequiredOption('from_date')
        self.addRequiredOption('to_date')


    def doClean(self, value):
        if not isinstance(value, (dict)):
          raise ValidPieError(self, 'invalid', {'value': value})

        value['from'] = self.getOption('from_date').clean(value['from'] if value.has_key('from') else None)
        value['to']   = self.getOption('to_date').clean(value['to'] if value.has_key('to') else None)

        return value;