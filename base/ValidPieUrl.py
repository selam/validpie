#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

from ValidPieRegex import ValidPieRegex

class ValidPieUrl(ValidPieRegex):
  def configure(self, options = {}, messages = {}):
    options.update({
      'pattern': '^(https?|ftps|http|ftp?)://(([a-z0-9-]+\.)+[a-z]{2,6}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:[0-9]+)?($|/?|/\S+)$'
    })

    ValidPieRegex.configure(self, options, messages)

print ValidPieUrl({'reqired': True}).clean('http://www.sinelist.com/callback.php#falanca')