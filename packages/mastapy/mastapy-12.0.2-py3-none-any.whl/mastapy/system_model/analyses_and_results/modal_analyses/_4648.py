"""_4648.py

UnbalancedMassModalAnalysis
"""


from mastapy.system_model.part_model import _2433
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6910
from mastapy.system_model.analyses_and_results.system_deflections import _2784
from mastapy.system_model.analyses_and_results.modal_analyses import _4649
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'UnbalancedMassModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassModalAnalysis',)


class UnbalancedMassModalAnalysis(_4649.VirtualComponentModalAnalysis):
    """UnbalancedMassModalAnalysis

    This is a mastapy class.
    """

    TYPE = _UNBALANCED_MASS_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'UnbalancedMassModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2433.UnbalancedMass':
        """UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6910.UnbalancedMassLoadCase':
        """UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2784.UnbalancedMassSystemDeflection':
        """UnbalancedMassSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
