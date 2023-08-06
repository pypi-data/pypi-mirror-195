﻿"""_1652.py

MomentOfInertia
"""


from mastapy.utility.units_and_measurements import _1572
from mastapy._internal.python_net import python_net_import

_MOMENT_OF_INERTIA = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'MomentOfInertia')


__docformat__ = 'restructuredtext en'
__all__ = ('MomentOfInertia',)


class MomentOfInertia(_1572.MeasurementBase):
    """MomentOfInertia

    This is a mastapy class.
    """

    TYPE = _MOMENT_OF_INERTIA

    def __init__(self, instance_to_wrap: 'MomentOfInertia.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
