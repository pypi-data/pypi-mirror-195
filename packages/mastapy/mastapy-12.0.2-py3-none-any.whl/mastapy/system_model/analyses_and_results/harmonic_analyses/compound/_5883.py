"""_5883.py

KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis
"""


from typing import List

from mastapy.system_model.part_model.gears import _2494
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5714
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5881, _5882, _5880
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis(_5880.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis):
    """KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis.TYPE'):
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
    def assembly_analysis_cases_ready(self) -> 'List[_5714.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis]':
        """List[KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_harmonic_analysis(self) -> 'List[_5881.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis]':
        """List[KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundHarmonicAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_harmonic_analysis(self) -> 'List[_5882.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis]':
        """List[KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundHarmonicAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5714.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis]':
        """List[KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
