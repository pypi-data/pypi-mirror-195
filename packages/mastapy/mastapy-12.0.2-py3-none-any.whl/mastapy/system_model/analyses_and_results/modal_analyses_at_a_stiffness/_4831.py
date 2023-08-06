﻿"""_4831.py

ConceptGearSetModalAnalysisAtAStiffness
"""


from typing import List

from mastapy.system_model.part_model.gears import _2477
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6773
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4830, _4829, _4861
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'ConceptGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetModalAnalysisAtAStiffness',)


class ConceptGearSetModalAnalysisAtAStiffness(_4861.GearSetModalAnalysisAtAStiffness):
    """ConceptGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    def __init__(self, instance_to_wrap: 'ConceptGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2477.ConceptGearSet':
        """ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6773.ConceptGearSetLoadCase':
        """ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def concept_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4830.ConceptGearModalAnalysisAtAStiffness]':
        """List[ConceptGearModalAnalysisAtAStiffness]: 'ConceptGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearsModalAnalysisAtAStiffness

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4829.ConceptGearMeshModalAnalysisAtAStiffness]':
        """List[ConceptGearMeshModalAnalysisAtAStiffness]: 'ConceptMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptMeshesModalAnalysisAtAStiffness

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
