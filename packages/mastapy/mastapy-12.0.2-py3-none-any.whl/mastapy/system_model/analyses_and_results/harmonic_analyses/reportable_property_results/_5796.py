﻿"""_5796.py

HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic
"""


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import _5807, _5795
from mastapy._internal.python_net import python_net_import

_HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_NODE_WITHIN_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic',)


class HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic(_5795.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic):
    """HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic

    This is a mastapy class.
    """

    TYPE = _HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_NODE_WITHIN_A_HARMONIC

    def __init__(self, instance_to_wrap: 'HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def node_name(self) -> 'str':
        """str: 'NodeName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NodeName

        if temp is None:
            return ''

        return temp

    @property
    def acceleration(self) -> '_5807.ResultsForResponseOfANodeOnAHarmonic':
        """ResultsForResponseOfANodeOnAHarmonic: 'Acceleration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Acceleration

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def displacement(self) -> '_5807.ResultsForResponseOfANodeOnAHarmonic':
        """ResultsForResponseOfANodeOnAHarmonic: 'Displacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Displacement

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def force(self) -> '_5807.ResultsForResponseOfANodeOnAHarmonic':
        """ResultsForResponseOfANodeOnAHarmonic: 'Force' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Force

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def velocity(self) -> '_5807.ResultsForResponseOfANodeOnAHarmonic':
        """ResultsForResponseOfANodeOnAHarmonic: 'Velocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Velocity

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
