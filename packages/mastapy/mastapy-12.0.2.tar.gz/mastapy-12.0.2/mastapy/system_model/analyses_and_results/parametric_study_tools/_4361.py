﻿"""_4361.py

SpiralBevelGearSetParametricStudyTool
"""


from typing import List

from mastapy.system_model.part_model.gears import _2499
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6885
from mastapy.system_model.analyses_and_results.system_deflections import _2758
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4360, _4359, _4260
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'SpiralBevelGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetParametricStudyTool',)


class SpiralBevelGearSetParametricStudyTool(_4260.BevelGearSetParametricStudyTool):
    """SpiralBevelGearSetParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_SET_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2499.SpiralBevelGearSet':
        """SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6885.SpiralBevelGearSetLoadCase':
        """SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2758.SpiralBevelGearSetSystemDeflection]':
        """List[SpiralBevelGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblySystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spiral_bevel_gears_parametric_study_tool(self) -> 'List[_4360.SpiralBevelGearParametricStudyTool]':
        """List[SpiralBevelGearParametricStudyTool]: 'SpiralBevelGearsParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelGearsParametricStudyTool

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spiral_bevel_meshes_parametric_study_tool(self) -> 'List[_4359.SpiralBevelGearMeshParametricStudyTool]':
        """List[SpiralBevelGearMeshParametricStudyTool]: 'SpiralBevelMeshesParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelMeshesParametricStudyTool

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
