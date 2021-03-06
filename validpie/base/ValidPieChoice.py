#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

import collections

class ValidPieChoice(ValidPieBase):
    def configure(self, options = {}, messages = {}):
        self.addRequiredOption('choices')
        self.addOption('multiple', False)

    def doClean(self, value):
        choices = self.getOption('choices')

        if hasattr(choices, '__call__'):
          choices = choices();

        if self.getOption('multiple'):

           if not isinstance(value, (tuple, list, dict)):
              value = [value]
           for v in value:
             if not self.inChoices(v, choices):
                raise ValidPieError(self, 'invalid', {'value': v})
        else:
          if not self.inChoices(value, choices):
            raise ValidPieError(self, 'invalid', {'value': value})

        return value

    def inChoices(self, value, choices):
        return True if value in choices else False
