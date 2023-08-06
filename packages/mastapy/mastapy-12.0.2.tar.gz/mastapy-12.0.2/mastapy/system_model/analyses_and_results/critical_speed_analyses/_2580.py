﻿"""_2580.py

CriticalSpeedAnalysis
"""


from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6515
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _7478
from mastapy._internal.python_net import python_net_import

_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'CriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CriticalSpeedAnalysis',)


class CriticalSpeedAnalysis(_7478.StaticLoadAnalysisCase):
    """CriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'CriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def critical_speed_analysis_options(self) -> '_6515.CriticalSpeedAnalysisOptions':
        """CriticalSpeedAnalysisOptions: 'CriticalSpeedAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CriticalSpeedAnalysisOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
