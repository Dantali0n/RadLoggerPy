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

from threading import Condition
from unittest import mock

from oslo_log import log
from radloggerpy import config

from radloggerpy.database.objects.serial_device import SerialDeviceObject
from radloggerpy.device.devices import arduino_geiger_pcb as agpcb
from radloggerpy.tests import base
from radloggerpy.types.serial_parity import PARITY_CHOICES
from radloggerpy.types.serial_parity import SerialParityTypes

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestArduinoGeigerPcb(base.TestCase):

    def setUp(self):
        super(TestArduinoGeigerPcb, self).setUp()
        self.m_info = SerialDeviceObject()
        self.m_info.parity = PARITY_CHOICES[SerialParityTypes.PARITY_NONE]
        self.m_condition = Condition()

    def test_name(self):
        m_device = agpcb.ArduinoGeigerPcb(self.m_info, self.m_condition)
        self.assertEqual(agpcb.ArduinoGeigerPcb.NAME, m_device.NAME)

    @mock.patch.object(agpcb, 'serial')
    @mock.patch.object(agpcb, 'time')
    def test_run(self, m_time, m_serial):
        m_time.sleep.side_effect = [InterruptedError]
        m_waiting = mock.Mock()
        m_waiting.inWaiting.side_effect = [1, 0]
        m_waiting.read.return_value.decode.return_value = 'a'
        m_serial.Serial.return_value = m_waiting
        m_device = agpcb.ArduinoGeigerPcb(self.m_info, self.m_condition)

        self.assertRaises(InterruptedError, m_device.run)
        m_serial.Serial.assert_called_once()
