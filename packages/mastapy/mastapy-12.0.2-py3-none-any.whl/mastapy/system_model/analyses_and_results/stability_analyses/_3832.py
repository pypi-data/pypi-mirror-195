"""_3832.py

SynchroniserStabilityAnalysis
"""


from mastapy.system_model.part_model.couplings import _2557
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6898
from mastapy.system_model.analyses_and_results.stability_analyses import _3812
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'SynchroniserStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserStabilityAnalysis',)


class SynchroniserStabilityAnalysis(_3812.SpecialisedAssemblyStabilityAnalysis):
    """SynchroniserStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'SynchroniserStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2557.Synchroniser':
        """Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6898.SynchroniserLoadCase':
        """SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
