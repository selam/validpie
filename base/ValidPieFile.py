#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

# global settings for using magic
useMagic = True

import os
try:

  import magic
  # initialize magic library
  ms = magic.open(magic.MAGIC_MIME)
  ms.load()
except:
  useMagic = False

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase
from Exceptions import InvalidArgumentException

class ValidPieFile(ValidPieBase):
    def configure(self, options = {}, messages = {}):
        self.addOption('max_size')
        self.addOption('mime_types')
        self.addOption('mime_type_guessers', [
          [self, 'guessWithMagicCookie']
        ])

        self.addOption('mime_categories', {
          'web_images' : [
            'image/jpeg',
            'image/pjpeg',
            'image/png',
            'image/x-png',
            'image/gif',
        ]})


        self.addOption('path', None)

        self.addMessage('max_size', 'File is too large (maximum is %(max_size)s bytes).')
        self.addMessage('mime_types', 'Invalid mime type "%(mime_type)s".')

    def doClean(self, value):
        if not isinstance(value, (dict)) or not value.has_key('tmp_name'):
           raise ValidPieError(self, 'invalid', {'value' : value});

        if not value.has_key('size'):
          value['size'] = os.path.getsize(value['tmp_name'])

        if  not value.has_key('type'):
          value['type'] = 'application/octet-stream';

        if self.getOption('max_size') and value['size'] > integer(self.getOption('max_size')):
           raise ValidPieError(self, 'max_size', {'max_size': self.getOption('max_size'), 'size' : value['size']});

        mimeType = self.getMimeType(value['tmp_name'], value['type'])

        # check mime type
        if self.hasOption('mime_types'):
          mimeTypes = self.getOption('mime_types') if isinstance(self.getOption('mime_types'), (list)) else self.getMimeTypesFromCategory(self.getOption('mime_types'))
          if mimeType not in mimeTypes:
            raise ValidPieError(self, 'mime_types', {'mime_types' : mimeTypes, 'mime_type' :mimeType})

        return value;

    def getMimeTypesFromCategory(self, category):
        categories = self.getOption('mime_categories')

        if not categories.has_key(category):
          InvalidArgumentException('Invalid mime type category "%s".' % (category))

        return categories[category];


    def getMimeType(self, filePath, defaultMimeType = None):
        for guessers in self.getOption('mime_type_guessers'):
          mimeType = getattr(guessers[0], guessers[1])(filePath)
          if mimeType is not None and mimeType is not False:
            return mimeType;
        return defaultMimeType;


    def guessWithMagicCookie(self, filePath):

        if useMagic:
          mimeType =  ms.file(filePath)
          if mimeType:
            return mimeType.split(';')[0]
        return None;


if __name__ == '__main__':
  import unittest
  class testValidFile(unittest.TestCase):
    def setUp(self):
        self.__v = ValidPieFile({'mime_types': 'web_images'});

    def testValidValues(self):
        self.assertEqual(self.__v.clean({'tmp_name': 'fixtures/validimage.jpg'}), True)

    def testInvalidValues(self):
        try:
          self.assertEqual(self.__v.clean({'tmp_name': 'fixtures/invalid.jpg'}), True)
          self.fail('invalid image should not return true value')
        except ValidPieError, e:
          self.assertEqual(e.getMessage(), 'Invalid mime type "text/plain".')


  suite = unittest.TestLoader().loadTestsFromTestCase(testValidFile)
  unittest.TextTestRunner(verbosity=2).run(suite)