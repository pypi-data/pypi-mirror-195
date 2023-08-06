﻿"""_3450.py

WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft
"""


from typing import List

from mastapy.system_model.part_model.gears import _2507
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _3320
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _3448, _3449, _3385
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft',)


class WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft(_3385.GearSetCompoundSteadyStateSynchronousResponseOnAShaft):
    """WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2507.WormGearSet':
        """WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2507.WormGearSet':
        """WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3320.WormGearSetSteadyStateSynchronousResponseOnAShaft]':
        """List[WormGearSetSteadyStateSynchronousResponseOnAShaft]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_gears_compound_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_3448.WormGearCompoundSteadyStateSynchronousResponseOnAShaft]':
        """List[WormGearCompoundSteadyStateSynchronousResponseOnAShaft]: 'WormGearsCompoundSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearsCompoundSteadyStateSynchronousResponseOnAShaft

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_meshes_compound_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_3449.WormGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]':
        """List[WormGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]: 'WormMeshesCompoundSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormMeshesCompoundSteadyStateSynchronousResponseOnAShaft

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3320.WormGearSetSteadyStateSynchronousResponseOnAShaft]':
        """List[WormGearSetSteadyStateSynchronousResponseOnAShaft]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
