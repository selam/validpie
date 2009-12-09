#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from ValidPieDate import ValidPieDate

class ValidPieDateTime(ValidPieDate):
  def configure(self, options = {}, messages = {}):
    ValidPieDate.configure(self, options, messages)
    self.setOption('with_time', True)
    self.addOption('date_format', '%Y-%m-%d %H:%i:%s')
