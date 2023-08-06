"""_4530.py

BevelDifferentialGearModalAnalysis
"""


from mastapy.system_model.part_model.gears import _2470, _2472, _2473
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6753, _6756, _6757
from mastapy.system_model.analyses_and_results.system_deflections import _2653, _2654, _2655
from mastapy.system_model.analyses_and_results.modal_analyses import _4535
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'BevelDifferentialGearModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearModalAnalysis',)


class BevelDifferentialGearModalAnalysis(_4535.BevelGearModalAnalysis):
    """BevelDifferentialGearModalAnalysis

    This is a mastapy class.
    """

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2470.BevelDifferentialGear':
        """BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2470.BevelDifferentialGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6753.BevelDifferentialGearLoadCase':
        """BevelDifferentialGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        if _6753.BevelDifferentialGearLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_load_case to BevelDifferentialGearLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2653.BevelDifferentialGearSystemDeflection':
        """BevelDifferentialGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        if _2653.BevelDifferentialGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BevelDifferentialGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
