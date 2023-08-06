"""_3461.py

AssemblySteadyStateSynchronousResponseAtASpeed
"""


from typing import List

from mastapy.system_model.part_model import _2390, _2430
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6749, _6878
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _3462, _3464, _3466, _3473,
    _3474, _3496, _3477, _3482,
    _3484, _3497, _3500, _3502,
    _3510, _3508, _3511, _3517,
    _3524, _3527, _3529, _3530,
    _3532, _3536, _3539, _3540,
    _3541, _3543, _3545, _3549,
    _3550, _3554, _3558, _3561,
    _3564, _3571, _3574, _3576,
    _3579, _3582, _3454
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'AssemblySteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblySteadyStateSynchronousResponseAtASpeed',)


class AssemblySteadyStateSynchronousResponseAtASpeed(_3454.AbstractAssemblySteadyStateSynchronousResponseAtASpeed):
    """AssemblySteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = _ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'AssemblySteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2390.Assembly':
        """Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        if _2390.Assembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6749.AssemblyLoadCase':
        """AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        if _6749.AssemblyLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearings(self) -> 'List[_3462.BearingSteadyStateSynchronousResponseAtASpeed]':
        """List[BearingSteadyStateSynchronousResponseAtASpeed]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def belt_drives(self) -> 'List[_3464.BeltDriveSteadyStateSynchronousResponseAtASpeed]':
        """List[BeltDriveSteadyStateSynchronousResponseAtASpeed]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BeltDrives

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3466.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelDifferentialGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bolted_joints(self) -> 'List[_3473.BoltedJointSteadyStateSynchronousResponseAtASpeed]':
        """List[BoltedJointSteadyStateSynchronousResponseAtASpeed]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoltedJoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bolts(self) -> 'List[_3474.BoltSteadyStateSynchronousResponseAtASpeed]':
        """List[BoltSteadyStateSynchronousResponseAtASpeed]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bolts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cv_ts(self) -> 'List[_3496.CVTSteadyStateSynchronousResponseAtASpeed]':
        """List[CVTSteadyStateSynchronousResponseAtASpeed]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CVTs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def clutches(self) -> 'List[_3477.ClutchSteadyStateSynchronousResponseAtASpeed]':
        """List[ClutchSteadyStateSynchronousResponseAtASpeed]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Clutches

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_couplings(self) -> 'List[_3482.ConceptCouplingSteadyStateSynchronousResponseAtASpeed]':
        """List[ConceptCouplingSteadyStateSynchronousResponseAtASpeed]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptCouplings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3484.ConceptGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[ConceptGearSetSteadyStateSynchronousResponseAtASpeed]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3497.CycloidalAssemblySteadyStateSynchronousResponseAtASpeed]':
        """List[CycloidalAssemblySteadyStateSynchronousResponseAtASpeed]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3500.CycloidalDiscSteadyStateSynchronousResponseAtASpeed]':
        """List[CycloidalDiscSteadyStateSynchronousResponseAtASpeed]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalDiscs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3502.CylindricalGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[CylindricalGearSetSteadyStateSynchronousResponseAtASpeed]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def fe_parts(self) -> 'List[_3510.FEPartSteadyStateSynchronousResponseAtASpeed]':
        """List[FEPartSteadyStateSynchronousResponseAtASpeed]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEParts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def face_gear_sets(self) -> 'List[_3508.FaceGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[FaceGearSetSteadyStateSynchronousResponseAtASpeed]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3511.FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed]':
        """List[FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlexiblePinAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3517.HypoidGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[HypoidGearSetSteadyStateSynchronousResponseAtASpeed]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3524.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3527.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def mass_discs(self) -> 'List[_3529.MassDiscSteadyStateSynchronousResponseAtASpeed]':
        """List[MassDiscSteadyStateSynchronousResponseAtASpeed]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MassDiscs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def measurement_components(self) -> 'List[_3530.MeasurementComponentSteadyStateSynchronousResponseAtASpeed]':
        """List[MeasurementComponentSteadyStateSynchronousResponseAtASpeed]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeasurementComponents

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def oil_seals(self) -> 'List[_3532.OilSealSteadyStateSynchronousResponseAtASpeed]':
        """List[OilSealSteadyStateSynchronousResponseAtASpeed]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OilSeals

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3536.PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed]':
        """List[PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PartToPartShearCouplings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planet_carriers(self) -> 'List[_3539.PlanetCarrierSteadyStateSynchronousResponseAtASpeed]':
        """List[PlanetCarrierSteadyStateSynchronousResponseAtASpeed]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetCarriers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def point_loads(self) -> 'List[_3540.PointLoadSteadyStateSynchronousResponseAtASpeed]':
        """List[PointLoadSteadyStateSynchronousResponseAtASpeed]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PointLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def power_loads(self) -> 'List[_3541.PowerLoadSteadyStateSynchronousResponseAtASpeed]':
        """List[PowerLoadSteadyStateSynchronousResponseAtASpeed]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def ring_pins(self) -> 'List[_3543.RingPinsSteadyStateSynchronousResponseAtASpeed]':
        """List[RingPinsSteadyStateSynchronousResponseAtASpeed]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RingPins

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3545.RollingRingAssemblySteadyStateSynchronousResponseAtASpeed]':
        """List[RollingRingAssemblySteadyStateSynchronousResponseAtASpeed]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollingRingAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3549.ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed]':
        """List[ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftHubConnections

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def shafts(self) -> 'List[_3550.ShaftSteadyStateSynchronousResponseAtASpeed]':
        """List[ShaftSteadyStateSynchronousResponseAtASpeed]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shafts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3554.SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spring_dampers(self) -> 'List[_3558.SpringDamperSteadyStateSynchronousResponseAtASpeed]':
        """List[SpringDamperSteadyStateSynchronousResponseAtASpeed]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpringDampers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3561.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelDiffGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3564.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def synchronisers(self) -> 'List[_3571.SynchroniserSteadyStateSynchronousResponseAtASpeed]':
        """List[SynchroniserSteadyStateSynchronousResponseAtASpeed]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Synchronisers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def torque_converters(self) -> 'List[_3574.TorqueConverterSteadyStateSynchronousResponseAtASpeed]':
        """List[TorqueConverterSteadyStateSynchronousResponseAtASpeed]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueConverters

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3576.UnbalancedMassSteadyStateSynchronousResponseAtASpeed]':
        """List[UnbalancedMassSteadyStateSynchronousResponseAtASpeed]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UnbalancedMasses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3579.WormGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[WormGearSetSteadyStateSynchronousResponseAtASpeed]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3582.ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        """List[ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
