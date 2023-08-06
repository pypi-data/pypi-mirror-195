"""_4323.py

KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool
"""


from typing import List

from mastapy.system_model.part_model.gears import _2496
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6850
from mastapy.system_model.analyses_and_results.system_deflections import _2725
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4322, _4321, _4317
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool',)


class KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool(_4317.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool):
    """KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2496.KlingelnbergCycloPalloidSpiralBevelGearSet':
        """KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6850.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        """KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2725.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblySystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_parametric_study_tool(self) -> 'List[_4322.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool]: 'KlingelnbergCycloPalloidSpiralBevelGearsParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsParametricStudyTool

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_parametric_study_tool(self) -> 'List[_4321.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool]: 'KlingelnbergCycloPalloidSpiralBevelMeshesParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesParametricStudyTool

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
