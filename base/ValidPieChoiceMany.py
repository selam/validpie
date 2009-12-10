#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist


from ValidPieChoice import ValidPieChoice

class ValidPieChoiceMany(ValidPieChoice):
  def configure(self, options = {}, messages = {}):
    ValidPieChoice.configure(self, options, messages)
    self.addOption('multiple', True)