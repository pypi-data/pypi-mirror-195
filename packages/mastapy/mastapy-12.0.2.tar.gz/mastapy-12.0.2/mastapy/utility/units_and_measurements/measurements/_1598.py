"""_1598.py

Decibel
"""


from mastapy.utility.units_and_measurements import _1572
from mastapy._internal.python_net import python_net_import

_DECIBEL = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Decibel')


__docformat__ = 'restructuredtext en'
__all__ = ('Decibel',)


class Decibel(_1572.MeasurementBase):
    """Decibel

    This is a mastapy class.
    """

    TYPE = _DECIBEL

    def __init__(self, instance_to_wrap: 'Decibel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
