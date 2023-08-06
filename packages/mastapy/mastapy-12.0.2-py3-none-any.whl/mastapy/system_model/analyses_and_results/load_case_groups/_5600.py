"""_5600.py

AbstractStaticLoadCaseGroup
"""


from typing import List

from mastapy.system_model.analyses_and_results.load_case_groups import (
    _5609, _5610, _5598, _5608,
    _5599
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import _5613, _5616, _5617
from mastapy.system_model.part_model import (
    _2396, _2409, _2427, _2428
)
from mastapy.system_model.analyses_and_results.static_loads import (
    _6750, _6791, _6793, _6795,
    _6817, _6868, _6869, _6735,
    _6748
)
from mastapy.system_model.part_model.gears import _2481, _2480
from mastapy.system_model.connections_and_sockets.gears import _2267
from mastapy.system_model.analyses_and_results.power_flows.compound import _4162
from mastapy.system_model.analyses_and_results import (
    _2636, _2631, _2613, _2623,
    _2633, _2626, _2616, _2632,
    _2615, _2620, _2574
)
from mastapy._internal.python_net import python_net_import

_ABSTRACT_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'AbstractStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractStaticLoadCaseGroup',)


class AbstractStaticLoadCaseGroup(_5599.AbstractLoadCaseGroup):
    """AbstractStaticLoadCaseGroup

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_STATIC_LOAD_CASE_GROUP

    def __init__(self, instance_to_wrap: 'AbstractStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_optimisation(self) -> '_5609.SystemOptimiserGearSetOptimisation':
        """SystemOptimiserGearSetOptimisation: 'GearSetOptimisation' is the original name of this property."""

        temp = self.wrapped.GearSetOptimisation

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5609.SystemOptimiserGearSetOptimisation)(value) if value is not None else None

    @gear_set_optimisation.setter
    def gear_set_optimisation(self, value: '_5609.SystemOptimiserGearSetOptimisation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearSetOptimisation = value

    @property
    def max_number_of_load_cases_to_display(self) -> 'int':
        """int: 'MaxNumberOfLoadCasesToDisplay' is the original name of this property."""

        temp = self.wrapped.MaxNumberOfLoadCasesToDisplay

        if temp is None:
            return 0

        return temp

    @max_number_of_load_cases_to_display.setter
    def max_number_of_load_cases_to_display(self, value: 'int'):
        self.wrapped.MaxNumberOfLoadCasesToDisplay = int(value) if value else 0

    @property
    def number_of_configurations_to_create(self) -> 'int':
        """int: 'NumberOfConfigurationsToCreate' is the original name of this property."""

        temp = self.wrapped.NumberOfConfigurationsToCreate

        if temp is None:
            return 0

        return temp

    @number_of_configurations_to_create.setter
    def number_of_configurations_to_create(self, value: 'int'):
        self.wrapped.NumberOfConfigurationsToCreate = int(value) if value else 0

    @property
    def number_of_possible_system_designs(self) -> 'int':
        """int: 'NumberOfPossibleSystemDesigns' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfPossibleSystemDesigns

        if temp is None:
            return 0

        return temp

    @property
    def optimum_tooth_numbers_target(self) -> '_5610.SystemOptimiserTargets':
        """SystemOptimiserTargets: 'OptimumToothNumbersTarget' is the original name of this property."""

        temp = self.wrapped.OptimumToothNumbersTarget

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5610.SystemOptimiserTargets)(value) if value is not None else None

    @optimum_tooth_numbers_target.setter
    def optimum_tooth_numbers_target(self, value: '_5610.SystemOptimiserTargets'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OptimumToothNumbersTarget = value

    @property
    def system_optimiser_log(self) -> 'str':
        """str: 'SystemOptimiserLog' is the original name of this property."""

        temp = self.wrapped.SystemOptimiserLog

        if temp is None:
            return ''

        return temp

    @system_optimiser_log.setter
    def system_optimiser_log(self, value: 'str'):
        self.wrapped.SystemOptimiserLog = str(value) if value else ''

    @property
    def bearings(self) -> 'List[_5613.ComponentStaticLoadCaseGroup[_2396.Bearing, _6750.BearingLoadCase]]':
        """List[ComponentStaticLoadCaseGroup[Bearing, BearingLoadCase]]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5616.GearSetStaticLoadCaseGroup[_2481.CylindricalGearSet, _2480.CylindricalGear, _6791.CylindricalGearLoadCase, _2267.CylindricalGearMesh, _6793.CylindricalGearMeshLoadCase, _6795.CylindricalGearSetLoadCase]]':
        """List[GearSetStaticLoadCaseGroup[CylindricalGearSet, CylindricalGear, CylindricalGearLoadCase, CylindricalGearMesh, CylindricalGearMeshLoadCase, CylindricalGearSetLoadCase]]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def design_states(self) -> 'List[_5598.AbstractDesignStateLoadCaseGroup]':
        """List[AbstractDesignStateLoadCaseGroup]: 'DesignStates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DesignStates

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def fe_parts(self) -> 'List[_5613.ComponentStaticLoadCaseGroup[_2409.FEPart, _6817.FEPartLoadCase]]':
        """List[ComponentStaticLoadCaseGroup[FEPart, FEPartLoadCase]]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEParts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def loaded_gear_sets(self) -> 'List[_4162.CylindricalGearSetCompoundPowerFlow]':
        """List[CylindricalGearSetCompoundPowerFlow]: 'LoadedGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def parts_with_excitations(self) -> 'List[_5617.PartStaticLoadCaseGroup]':
        """List[PartStaticLoadCaseGroup]: 'PartsWithExcitations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PartsWithExcitations

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def point_loads(self) -> 'List[_5613.ComponentStaticLoadCaseGroup[_2427.PointLoad, _6868.PointLoadLoadCase]]':
        """List[ComponentStaticLoadCaseGroup[PointLoad, PointLoadLoadCase]]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PointLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def power_loads(self) -> 'List[_5613.ComponentStaticLoadCaseGroup[_2428.PowerLoad, _6869.PowerLoadLoadCase]]':
        """List[ComponentStaticLoadCaseGroup[PowerLoad, PowerLoadLoadCase]]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def static_loads(self) -> 'List[_6735.StaticLoadCase]':
        """List[StaticLoadCase]: 'StaticLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def static_loads_limited_by_max_number_of_load_cases_to_display(self) -> 'List[_6735.StaticLoadCase]':
        """List[StaticLoadCase]: 'StaticLoadsLimitedByMaxNumberOfLoadCasesToDisplay' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticLoadsLimitedByMaxNumberOfLoadCasesToDisplay

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def system_optimisation_gear_sets(self) -> 'List[_5608.SystemOptimisationGearSet]':
        """List[SystemOptimisationGearSet]: 'SystemOptimisationGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemOptimisationGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def compound_system_deflection(self) -> '_2636.CompoundSystemDeflectionAnalysis':
        """CompoundSystemDeflectionAnalysis: 'CompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompoundSystemDeflection

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def compound_power_flow(self) -> '_2631.CompoundPowerFlowAnalysis':
        """CompoundPowerFlowAnalysis: 'CompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompoundPowerFlow

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def compound_advanced_system_deflection(self) -> '_2613.CompoundAdvancedSystemDeflectionAnalysis':
        """CompoundAdvancedSystemDeflectionAnalysis: 'CompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompoundAdvancedSystemDeflection

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def compound_harmonic_analysis(self) -> '_2623.CompoundHarmonicAnalysis':
        """CompoundHarmonicAnalysis: 'CompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompoundHarmonicAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def compound_steady_state_synchronous_response(self) -> '_2633.CompoundSteadyStateSynchronousResponseAnalysis':
        """CompoundSteadyStateSynchronousResponseAnalysis: 'CompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompoundSteadyStateSynchronousResponse

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def compound_modal_analysis(self) -> '_2626.CompoundModalAnalysis':
        """CompoundModalAnalysis: 'CompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompoundModalAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def compound_critical_speed_analysis(self) -> '_2616.CompoundCriticalSpeedAnalysis':
        """CompoundCriticalSpeedAnalysis: 'CompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompoundCriticalSpeedAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def compound_stability_analysis(self) -> '_2632.CompoundStabilityAnalysis':
        """CompoundStabilityAnalysis: 'CompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompoundStabilityAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def compound_advanced_time_stepping_analysis_for_modulation(self) -> '_2615.CompoundAdvancedTimeSteppingAnalysisForModulation':
        """CompoundAdvancedTimeSteppingAnalysisForModulation: 'CompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompoundAdvancedTimeSteppingAnalysisForModulation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def compound_dynamic_model_for_modal_analysis(self) -> '_2620.CompoundDynamicModelForModalAnalysis':
        """CompoundDynamicModelForModalAnalysis: 'CompoundDynamicModelForModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompoundDynamicModelForModalAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def calculate_candidates(self):
        """ 'CalculateCandidates' is the original name of this method."""

        self.wrapped.CalculateCandidates()

    def clear_user_specified_excitation_data_for_all_load_cases(self):
        """ 'ClearUserSpecifiedExcitationDataForAllLoadCases' is the original name of this method."""

        self.wrapped.ClearUserSpecifiedExcitationDataForAllLoadCases()

    def create_designs(self):
        """ 'CreateDesigns' is the original name of this method."""

        self.wrapped.CreateDesigns()

    def optimise_gear_sets_quick(self):
        """ 'OptimiseGearSetsQuick' is the original name of this method."""

        self.wrapped.OptimiseGearSetsQuick()

    def perform_system_optimisation(self):
        """ 'PerformSystemOptimisation' is the original name of this method."""

        self.wrapped.PerformSystemOptimisation()

    def run_power_flow(self):
        """ 'RunPowerFlow' is the original name of this method."""

        self.wrapped.RunPowerFlow()

    def set_face_widths_for_specified_safety_factors_from_power_flow(self):
        """ 'SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow' is the original name of this method."""

        self.wrapped.SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow()

    def analysis_of(self, analysis_type: '_6748.AnalysisType') -> '_2574.CompoundAnalysis':
        """ 'AnalysisOf' is the original name of this method.

        Args:
            analysis_type (mastapy.system_model.analyses_and_results.static_loads.AnalysisType)

        Returns:
            mastapy.system_model.analyses_and_results.CompoundAnalysis
        """

        analysis_type = conversion.mp_to_pn_enum(analysis_type)
        method_result = self.wrapped.AnalysisOf(analysis_type)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
