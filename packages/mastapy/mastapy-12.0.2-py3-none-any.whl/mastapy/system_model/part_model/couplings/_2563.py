﻿"""_2563.py

TorqueConverterPump
"""


from mastapy.system_model.part_model.couplings import _2539
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterPump')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPump',)


class TorqueConverterPump(_2539.CouplingHalf):
    """TorqueConverterPump

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_PUMP

    def __init__(self, instance_to_wrap: 'TorqueConverterPump.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
