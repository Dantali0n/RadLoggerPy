# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Dantali0n
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock
import os

from babel import localedata
import oslo_i18n

import radloggerpy
from radloggerpy import _i18n

from radloggerpy.tests import base


class Testi18n(base.TestCase):

    def setUp(self):
        super(Testi18n, self).setUp()

    def test_domain(self):
        self.assertEqual(_i18n.DOMAIN, _i18n._translators.domain)

    @mock.patch.object(oslo_i18n._gettextutils, '_AVAILABLE_LANGUAGES')
    @mock.patch.object(os, 'environ')
    def test_translate(self, m_environ, m_languages_get):
        m_languages_get.return_value = None
        m_environ.get.side_effect = [
            'nl', 'nl', 'nl', 'nl', 'radloggerpy/locale'
        ]

        m_translated_nl = _i18n._("RadLoggerPy opstarten met PID %s")
        m_untranslated = _i18n._("Starting RadLoggerPy service on PID %s")

        self.assertEqual(m_translated_nl,
                         _i18n.translate(m_untranslated, 'nl_NL'))

    def test_get_available_languages(self):
        m_languages = ['en_US']

        self.assertEqual(m_languages, _i18n.get_available_languages())

    @mock.patch.object(oslo_i18n._gettextutils, '_AVAILABLE_LANGUAGES')
    @mock.patch.object(os, 'environ')
    def test_get_available_languages_real(self, m_environ, m_languages_get):
        """Ensure all languages are registered if the localedir is set

        :param m_environ: patch os.environ.get to fake RADLOGGERPY_LOCALEDIR
        :param m_languages_get: reset _factory _AVAILALE_LANGUAGES variable
        :return:
        """
        m_languages_get.return_value = None
        m_environ.get.return_value = 'radloggerpy/locale'

        m_languages = ['en_US']
        locale_identifiers = localedata.locale_identifiers()

        m_locale = radloggerpy.__path__[0] + '/locale'
        m_locale_dirs = [o for o in os.listdir(m_locale)
                         if os.path.isdir(os.path.join(m_locale, o))]

        for m_locale_dir in m_locale_dirs:
            m_languages.extend(language for language in locale_identifiers
                               if m_locale_dir in language)

        self.assertItemsEqual(m_languages, _i18n.get_available_languages())