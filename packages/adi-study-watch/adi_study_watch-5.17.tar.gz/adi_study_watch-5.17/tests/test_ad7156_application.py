# ******************************************************************************
# Copyright (c) 2019 Analog Devices, Inc.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
# - Modified versions of the software must be conspicuously marked as such.
# - This software is licensed solely and exclusively for use with
#  processors/products manufactured by or for Analog Devices, Inc.
# - This software may not be combined or merged with other code in any manner
#  that would cause the software to become subject to terms and conditions
#  which differ from those listed here.
# - Neither the name of Analog Devices, Inc. nor the names of its contributors
#  may be used to endorse or promote products derived from this software
#  without specific prior written permission.
# - The use of this software may or may not infringe the patent rights of one
#  or more patent holders.  This license does not release you from the
#  requirement that you obtain separate licenses from these patent holders to
#  use this software.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES, INC. AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# NONINFRINGEMENT, TITLE, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ANALOG DEVICES, INC. OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, DAMAGES ARISING OUT OF
# CLAIMS OF INTELLECTUAL PROPERTY RIGHTS INFRINGEMENT; PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ******************************************************************************

from unittest import TestCase

from ..adi_study_watch import SDK
from ..adi_study_watch.core.enums.common_enums import CommonStatus


class TestAD7156Application(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.application = SDK("COM4").get_ad7156_application()

    def test_load_configuration(self):
        x = self.application.load_configuration()
        assert (x["payload"]["status"] == CommonStatus.OK)

    def test_device_configuration_block(self):
        x = self.application.write_device_configuration_block([[0x10, 2], [0x11, 0x1]])
        assert (x["payload"]["size"] == 0)
        x = self.application.read_device_configuration_block()
        assert (x["payload"]["data"] == [['0x10', '0x2'], ['0x11', '0x1']])
        x = self.application.delete_device_configuration_block()
        assert (x["payload"]["size"] == 0)

    def test_register(self):
        x = self.application.write_register([[0xa, 0x5], [0xb, 0x2]])
        assert (x["payload"]["size"] == 2)
        assert (x["payload"]["data"] == [['0xA', '0x5'], ['0xB', '0x2']])
        x = self.application.read_register([0xa, 0xb])
        assert (x["payload"]["size"] == 2)
        assert (x["payload"]["data"] == [['0xA', '0x5'], ['0xB', '0x2']])
