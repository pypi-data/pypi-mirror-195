"""_3648.py

HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed
"""


from typing import List

from mastapy.system_model.part_model.gears import _2490
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3517
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3646, _3647, _3590
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed',)


class HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed(_3590.AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed):
    """HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2490.HypoidGearSet':
        """HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2490.HypoidGearSet':
        """HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3517.HypoidGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[HypoidGearSetSteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_gears_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3646.HypoidGearCompoundSteadyStateSynchronousResponseAtASpeed]':
        """List[HypoidGearCompoundSteadyStateSynchronousResponseAtASpeed]: 'HypoidGearsCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearsCompoundSteadyStateSynchronousResponseAtASpeed

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_meshes_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3647.HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]':
        """List[HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]: 'HypoidMeshesCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidMeshesCompoundSteadyStateSynchronousResponseAtASpeed

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3517.HypoidGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[HypoidGearSetSteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
