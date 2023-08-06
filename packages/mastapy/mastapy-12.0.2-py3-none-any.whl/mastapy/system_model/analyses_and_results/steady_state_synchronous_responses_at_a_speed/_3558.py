"""_3558.py

SpringDamperSteadyStateSynchronousResponseAtASpeed
"""


from mastapy.system_model.part_model.couplings import _2555
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6888
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3493
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'SpringDamperSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperSteadyStateSynchronousResponseAtASpeed',)


class SpringDamperSteadyStateSynchronousResponseAtASpeed(_3493.CouplingSteadyStateSynchronousResponseAtASpeed):
    """SpringDamperSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'SpringDamperSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2555.SpringDamper':
        """SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6888.SpringDamperLoadCase':
        """SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
