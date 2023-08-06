"""_2569.py

ActiveShaftDesignSelectionGroup
"""


from mastapy.system_model.part_model.configurations import _2572, _2568
from mastapy.system_model.part_model.shaft_model import _2438
from mastapy.shafts import _43
from mastapy._internal.python_net import python_net_import

_ACTIVE_SHAFT_DESIGN_SELECTION_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveShaftDesignSelectionGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveShaftDesignSelectionGroup',)


class ActiveShaftDesignSelectionGroup(_2572.PartDetailConfiguration['_2568.ActiveShaftDesignSelection', '_2438.Shaft', '_43.SimpleShaftDefinition']):
    """ActiveShaftDesignSelectionGroup

    This is a mastapy class.
    """

    TYPE = _ACTIVE_SHAFT_DESIGN_SELECTION_GROUP

    def __init__(self, instance_to_wrap: 'ActiveShaftDesignSelectionGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
