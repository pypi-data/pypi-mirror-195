"""_5689.py

FlexiblePinAssemblyHarmonicAnalysis
"""


from mastapy.system_model.part_model import _2410
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6818
from mastapy.system_model.analyses_and_results.system_deflections import _2708
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5744
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'FlexiblePinAssemblyHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyHarmonicAnalysis',)


class FlexiblePinAssemblyHarmonicAnalysis(_5744.SpecialisedAssemblyHarmonicAnalysis):
    """FlexiblePinAssemblyHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2410.FlexiblePinAssembly':
        """FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6818.FlexiblePinAssemblyLoadCase':
        """FlexiblePinAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2708.FlexiblePinAssemblySystemDeflection':
        """FlexiblePinAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
