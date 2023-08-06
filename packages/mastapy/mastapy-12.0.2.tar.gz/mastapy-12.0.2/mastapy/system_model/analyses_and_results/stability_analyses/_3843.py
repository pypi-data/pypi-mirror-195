﻿"""_3843.py

ZerolBevelGearSetStabilityAnalysis
"""


from typing import List

from mastapy.system_model.part_model.gears import _2509
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6917
from mastapy.system_model.analyses_and_results.stability_analyses import _3844, _3842, _3730
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ZerolBevelGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetStabilityAnalysis',)


class ZerolBevelGearSetStabilityAnalysis(_3730.BevelGearSetStabilityAnalysis):
    """ZerolBevelGearSetStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_SET_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2509.ZerolBevelGearSet':
        """ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6917.ZerolBevelGearSetLoadCase':
        """ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def zerol_bevel_gears_stability_analysis(self) -> 'List[_3844.ZerolBevelGearStabilityAnalysis]':
        """List[ZerolBevelGearStabilityAnalysis]: 'ZerolBevelGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelGearsStabilityAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def zerol_bevel_meshes_stability_analysis(self) -> 'List[_3842.ZerolBevelGearMeshStabilityAnalysis]':
        """List[ZerolBevelGearMeshStabilityAnalysis]: 'ZerolBevelMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelMeshesStabilityAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
