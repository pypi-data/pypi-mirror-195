"""_6570.py

RootAssemblyCriticalSpeedAnalysis
"""


from mastapy.system_model.part_model import _2430
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _2580, _6481
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'RootAssemblyCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCriticalSpeedAnalysis',)


class RootAssemblyCriticalSpeedAnalysis(_6481.AssemblyCriticalSpeedAnalysis):
    """RootAssemblyCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'RootAssemblyCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2430.RootAssembly':
        """RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def critical_speed_analysis_inputs(self) -> '_2580.CriticalSpeedAnalysis':
        """CriticalSpeedAnalysis: 'CriticalSpeedAnalysisInputs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CriticalSpeedAnalysisInputs

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
