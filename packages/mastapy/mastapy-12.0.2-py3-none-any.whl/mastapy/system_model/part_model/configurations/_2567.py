"""_2567.py

ActiveFESubstructureSelectionGroup
"""


from mastapy.system_model.part_model.configurations import _2572, _2566
from mastapy.system_model.part_model import _2409
from mastapy.system_model.fe import _2340
from mastapy._internal.python_net import python_net_import

_ACTIVE_FE_SUBSTRUCTURE_SELECTION_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveFESubstructureSelectionGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveFESubstructureSelectionGroup',)


class ActiveFESubstructureSelectionGroup(_2572.PartDetailConfiguration['_2566.ActiveFESubstructureSelection', '_2409.FEPart', '_2340.FESubstructure']):
    """ActiveFESubstructureSelectionGroup

    This is a mastapy class.
    """

    TYPE = _ACTIVE_FE_SUBSTRUCTURE_SELECTION_GROUP

    def __init__(self, instance_to_wrap: 'ActiveFESubstructureSelectionGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
