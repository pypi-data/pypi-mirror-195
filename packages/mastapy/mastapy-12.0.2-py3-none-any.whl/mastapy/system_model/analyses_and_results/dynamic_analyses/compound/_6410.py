"""_6410.py

KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis
"""


from typing import List

from mastapy.system_model.part_model.gears import _2494
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6281
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6408, _6409, _6407
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis(_6407.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis):
    """KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2494.KlingelnbergCycloPalloidHypoidGearSet':
        """KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2494.KlingelnbergCycloPalloidHypoidGearSet':
        """KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6281.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]':
        """List[KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_dynamic_analysis(self) -> 'List[_6408.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]':
        """List[KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundDynamicAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_dynamic_analysis(self) -> 'List[_6409.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]':
        """List[KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundDynamicAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6281.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]':
        """List[KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
