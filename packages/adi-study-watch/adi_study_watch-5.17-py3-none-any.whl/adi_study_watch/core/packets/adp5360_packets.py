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
from ..data_types.array import Array
from ..data_types.enums import Enums
from ..data_types.integer import Int
from .command_packet import CommandPacket
from ..enums.adp5360_enums import BatteryStatus
from ..enums.dcb_enums import DCBConfigBlockIndex


class BatteryInfoPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x12',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.GET_BAT_INFO_RES: ['0x45']>,
                'status': <PMStatus.OK: ['0x41']>,
                'timestamp': 668880834,
                'battery_status': <BatteryStatus.COMPLETE: ['0x03']>,
                'adp5360_battery_level': 100,
                'custom_battery_level': 100,
                'battery_mv': 4334
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["timestamp"] = Int(4)
        self._config["payload"]["battery_status"] = Enums(1, enum_class=BatteryStatus)
        self._config["payload"]["adp5360_battery_level"] = Int(1)
        self._config["payload"]["custom_battery_level"] = Int(1)
        self._config["payload"]["battery_mv"] = Int(2)


class BatteryThresholdPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xA',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.SET_BAT_THR_RES: ['0x47']>,
                'status': <PMStatus.OK: ['0x41']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["low_level"] = Int(1, value_limit=[0, 100])
        self._config["payload"]["critical_level"] = Int(1, value_limit=[0, 100])
        self._config["payload"]["download_level"] = Int(1)
        self._config["payload"]["voltage_low"] = Int(2)
        self._config["payload"]["voltage_critical"] = Int(2)
        self._config["payload"]["voltage_critical_download"] = Int(2)


class ADP5360RegisterWritePacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 15,
                'checksum': 0
            },
            'payload': {
                'command': <CommonCommand.REGISTER_WRITE_RES: ['0x24']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'size': 1,
                'data': [
                    [ '0x0', '0x10' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=2,
                                                data_types=[
                                                    Int(2, to_hex=True),
                                                    Int(2, to_hex=True)
                                                ])


class ADP5360RegisterReadPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 15,
                'checksum': 0
            },
            'payload': {
                'command': <CommonCommand.REGISTER_READ_RES: ['0x22']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'size': 1,
                'data': [
                    [ '0x0', '0x10' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=2,
                                                data_types=[
                                                    Int(2, value_limit=[0x00, 0x36], to_hex=True),
                                                    Int(2, to_hex=True)
                                                ])


class ADP5360DCBPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 32,
                'checksum': 0
            },
            'payload': {
                'command': <DCBCommand.READ_CONFIG_RES: ['0x98']>,
                'status': <DCBStatus.OK: ['0x97']>,
                'size': 5,
                'data': [
                    [ '0x0', '0x1B58' ],
                    [ '0x1', '0x1388' ],
                    [ '0x2', '0x564' ],
                    [ '0x3', '0x53C' ],
                    [ '0x4', '0x3' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["dcb_block_index"] = Enums(1, enum_class=DCBConfigBlockIndex,
                                                           default=DCBConfigBlockIndex.ADP5360_BLOCK)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=2,
                                                data_types=[
                                                    Int(1, to_hex=True),
                                                    Int(3, to_hex=True)
                                                ], reverse_inner_array=True)


class ADP5360DCBCommandPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.EDA: ['0xC3', '0x02']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 20,
                'checksum': 0
            },
            'payload': {
                'command': <DCBCommand.READ_CONFIG_RES: ['0x98']>,
                'status': <DCBStatus.OK: ['0x97']>,
                'size': 1,
                'data': [
                    [ '0x0', '0x8' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["dcb_block_index"] = Enums(1, enum_class=DCBConfigBlockIndex,
                                                           default=DCBConfigBlockIndex.ADP5360_BLOCK)
