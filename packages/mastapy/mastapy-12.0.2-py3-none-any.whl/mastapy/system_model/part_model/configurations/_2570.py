"""_2570.py

BearingDetailConfiguration
"""


from mastapy.system_model.part_model.configurations import _2572, _2571
from mastapy.system_model.part_model import _2396
from mastapy.bearings.bearing_designs import _2091
from mastapy._internal.python_net import python_net_import

_BEARING_DETAIL_CONFIGURATION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'BearingDetailConfiguration')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingDetailConfiguration',)


class BearingDetailConfiguration(_2572.PartDetailConfiguration['_2571.BearingDetailSelection', '_2396.Bearing', '_2091.BearingDesign']):
    """BearingDetailConfiguration

    This is a mastapy class.
    """

    TYPE = _BEARING_DETAIL_CONFIGURATION

    def __init__(self, instance_to_wrap: 'BearingDetailConfiguration.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
