#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import re

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase
from ValidPieString import ValidPieString

class ValidPieRegex(ValidPieString):
  def configure(self, options = {}, messages = {}):
      ValidPieString.configure(self, options, messages)
      self.addRequiredOption('pattern')


  def doClean(self, value):
      clean = ValidPieString.doClean(self, value)

      if not re.compile(self.getOption('pattern')).match(clean):
        raise ValidPieError(self, 'invalid', {'value': value})

      return clean;