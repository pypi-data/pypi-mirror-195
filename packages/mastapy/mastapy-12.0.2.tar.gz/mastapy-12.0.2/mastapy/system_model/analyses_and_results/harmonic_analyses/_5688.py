"""_5688.py

FEPartHarmonicAnalysis
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2409
from mastapy.system_model.analyses_and_results.static_loads import _6817
from mastapy.system_model.analyses_and_results.modal_analyses import _4577
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5701, _5621
from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import _5790
from mastapy.system_model.analyses_and_results.system_deflections import _2707
from mastapy._internal.python_net import python_net_import

_FE_PART_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'FEPartHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartHarmonicAnalysis',)


class FEPartHarmonicAnalysis(_5621.AbstractShaftOrHousingHarmonicAnalysis):
    """FEPartHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _FE_PART_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'FEPartHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def export_accelerations(self) -> 'str':
        """str: 'ExportAccelerations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExportAccelerations

        if temp is None:
            return ''

        return temp

    @property
    def export_displacements(self) -> 'str':
        """str: 'ExportDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExportDisplacements

        if temp is None:
            return ''

        return temp

    @property
    def export_forces(self) -> 'str':
        """str: 'ExportForces' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExportForces

        if temp is None:
            return ''

        return temp

    @property
    def export_velocities(self) -> 'str':
        """str: 'ExportVelocities' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExportVelocities

        if temp is None:
            return ''

        return temp

    @property
    def component_design(self) -> '_2409.FEPart':
        """FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6817.FEPartLoadCase':
        """FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def coupled_modal_analysis(self) -> '_4577.FEPartModalAnalysis':
        """FEPartModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoupledModalAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def export(self) -> '_5701.HarmonicAnalysisFEExportOptions':
        """HarmonicAnalysisFEExportOptions: 'Export' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Export

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def results(self) -> '_5790.FEPartHarmonicAnalysisResultsPropertyAccessor':
        """FEPartHarmonicAnalysisResultsPropertyAccessor: 'Results' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Results

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2707.FEPartSystemDeflection':
        """FEPartSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[FEPartHarmonicAnalysis]':
        """List[FEPartHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
