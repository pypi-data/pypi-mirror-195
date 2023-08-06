"""_7076.py

AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
"""


from typing import List

from mastapy.system_model.part_model import _2390, _2430
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6945
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
    _7077, _7079, _7082, _7089,
    _7088, _7110, _7090, _7095,
    _7100, _7112, _7114, _7118,
    _7125, _7124, _7126, _7133,
    _7140, _7143, _7144, _7145,
    _7147, _7149, _7154, _7155,
    _7156, _7158, _7160, _7165,
    _7164, _7170, _7171, _7176,
    _7179, _7182, _7186, _7190,
    _7194, _7197, _7069
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation',)


class AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation(_7069.AbstractAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation):
    """AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _ASSEMBLY_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    def __init__(self, instance_to_wrap: 'AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2390.Assembly':
        """Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2390.Assembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

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
    def assembly_analysis_cases_ready(self) -> 'List[_6945.AssemblyAdvancedTimeSteppingAnalysisForModulation]':
        """List[AssemblyAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bearings(self) -> 'List[_7077.BearingCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[BearingCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def belt_drives(self) -> 'List[_7079.BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BeltDrives

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_7082.BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelDifferentialGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bolted_joints(self) -> 'List[_7089.BoltedJointCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[BoltedJointCompoundAdvancedTimeSteppingAnalysisForModulation]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoltedJoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bolts(self) -> 'List[_7088.BoltCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[BoltCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bolts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cv_ts(self) -> 'List[_7110.CVTCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[CVTCompoundAdvancedTimeSteppingAnalysisForModulation]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CVTs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def clutches(self) -> 'List[_7090.ClutchCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[ClutchCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Clutches

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_couplings(self) -> 'List[_7095.ConceptCouplingCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[ConceptCouplingCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptCouplings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_gear_sets(self) -> 'List[_7100.ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_7112.CycloidalAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[CycloidalAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cycloidal_discs(self) -> 'List[_7114.CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalDiscs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_7118.CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def fe_parts(self) -> 'List[_7125.FEPartCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[FEPartCompoundAdvancedTimeSteppingAnalysisForModulation]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEParts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def face_gear_sets(self) -> 'List[_7124.FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_7126.FlexiblePinAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[FlexiblePinAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlexiblePinAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_7133.HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_7140.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_7143.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def mass_discs(self) -> 'List[_7144.MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MassDiscs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def measurement_components(self) -> 'List[_7145.MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeasurementComponents

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def oil_seals(self) -> 'List[_7147.OilSealCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[OilSealCompoundAdvancedTimeSteppingAnalysisForModulation]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OilSeals

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_7149.PartToPartShearCouplingCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[PartToPartShearCouplingCompoundAdvancedTimeSteppingAnalysisForModulation]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PartToPartShearCouplings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planet_carriers(self) -> 'List[_7154.PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetCarriers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def point_loads(self) -> 'List[_7155.PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PointLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def power_loads(self) -> 'List[_7156.PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def ring_pins(self) -> 'List[_7158.RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RingPins

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_7160.RollingRingAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[RollingRingAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollingRingAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_7165.ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftHubConnections

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def shafts(self) -> 'List[_7164.ShaftCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[ShaftCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shafts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_7170.SpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[SpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spring_dampers(self) -> 'List[_7171.SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpringDampers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_7176.StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelDiffGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_7179.StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def synchronisers(self) -> 'List[_7182.SynchroniserCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[SynchroniserCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Synchronisers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def torque_converters(self) -> 'List[_7186.TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueConverters

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def unbalanced_masses(self) -> 'List[_7190.UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UnbalancedMasses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_gear_sets(self) -> 'List[_7194.WormGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[WormGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_7197.ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]':
        """List[ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6945.AssemblyAdvancedTimeSteppingAnalysisForModulation]':
        """List[AssemblyAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
