"""_6149.py

OilSealCompoundHarmonicAnalysisOfSingleExcitation
"""


from typing import List

from mastapy.system_model.part_model import _2422
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _6020
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _6107
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'OilSealCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundHarmonicAnalysisOfSingleExcitation',)


class OilSealCompoundHarmonicAnalysisOfSingleExcitation(_6107.ConnectorCompoundHarmonicAnalysisOfSingleExcitation):
    """OilSealCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _OIL_SEAL_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    def __init__(self, instance_to_wrap: 'OilSealCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2422.OilSeal':
        """OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6020.OilSealHarmonicAnalysisOfSingleExcitation]':
        """List[OilSealHarmonicAnalysisOfSingleExcitation]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6020.OilSealHarmonicAnalysisOfSingleExcitation]':
        """List[OilSealHarmonicAnalysisOfSingleExcitation]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
