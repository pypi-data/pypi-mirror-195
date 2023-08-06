"""_2223.py

AbstractShaftToMountableComponentConnection
"""


from mastapy.system_model.part_model import (
    _2420, _2396, _2403, _2418,
    _2419, _2422, _2425, _2427,
    _2428, _2433, _2435, _2392
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.gears import (
    _2468, _2470, _2472, _2473,
    _2474, _2476, _2478, _2480,
    _2482, _2483, _2485, _2489,
    _2491, _2493, _2495, _2498,
    _2500, _2502, _2504, _2505,
    _2506, _2508
)
from mastapy.system_model.part_model.cycloidal import _2525, _2524
from mastapy.system_model.part_model.couplings import (
    _2534, _2537, _2539, _2542,
    _2544, _2545, _2551, _2553,
    _2556, _2559, _2560, _2561,
    _2563, _2565
)
from mastapy.system_model.part_model.shaft_model import _2438
from mastapy.system_model.connections_and_sockets import _2230
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'AbstractShaftToMountableComponentConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftToMountableComponentConnection',)


class AbstractShaftToMountableComponentConnection(_2230.Connection):
    """AbstractShaftToMountableComponentConnection

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION

    def __init__(self, instance_to_wrap: 'AbstractShaftToMountableComponentConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mountable_component(self) -> '_2420.MountableComponent':
        """MountableComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2420.MountableComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MountableComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_bearing(self) -> '_2396.Bearing':
        """Bearing: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2396.Bearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Bearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_connector(self) -> '_2403.Connector':
        """Connector: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2403.Connector.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Connector. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_mass_disc(self) -> '_2418.MassDisc':
        """MassDisc: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2418.MassDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MassDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_measurement_component(self) -> '_2419.MeasurementComponent':
        """MeasurementComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2419.MeasurementComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MeasurementComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_oil_seal(self) -> '_2422.OilSeal':
        """OilSeal: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2422.OilSeal.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to OilSeal. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_planet_carrier(self) -> '_2425.PlanetCarrier':
        """PlanetCarrier: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2425.PlanetCarrier.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PlanetCarrier. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_point_load(self) -> '_2427.PointLoad':
        """PointLoad: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2427.PointLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PointLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_power_load(self) -> '_2428.PowerLoad':
        """PowerLoad: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2428.PowerLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PowerLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_unbalanced_mass(self) -> '_2433.UnbalancedMass':
        """UnbalancedMass: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2433.UnbalancedMass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to UnbalancedMass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_virtual_component(self) -> '_2435.VirtualComponent':
        """VirtualComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2435.VirtualComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to VirtualComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_agma_gleason_conical_gear(self) -> '_2468.AGMAGleasonConicalGear':
        """AGMAGleasonConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2468.AGMAGleasonConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to AGMAGleasonConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_bevel_differential_gear(self) -> '_2470.BevelDifferentialGear':
        """BevelDifferentialGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2470.BevelDifferentialGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_bevel_differential_planet_gear(self) -> '_2472.BevelDifferentialPlanetGear':
        """BevelDifferentialPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2472.BevelDifferentialPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_bevel_differential_sun_gear(self) -> '_2473.BevelDifferentialSunGear':
        """BevelDifferentialSunGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2473.BevelDifferentialSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_bevel_gear(self) -> '_2474.BevelGear':
        """BevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2474.BevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_concept_gear(self) -> '_2476.ConceptGear':
        """ConceptGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2476.ConceptGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConceptGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_conical_gear(self) -> '_2478.ConicalGear':
        """ConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2478.ConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_cylindrical_gear(self) -> '_2480.CylindricalGear':
        """CylindricalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2480.CylindricalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CylindricalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_cylindrical_planet_gear(self) -> '_2482.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2482.CylindricalPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CylindricalPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_face_gear(self) -> '_2483.FaceGear':
        """FaceGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2483.FaceGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to FaceGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_gear(self) -> '_2485.Gear':
        """Gear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2485.Gear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Gear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_hypoid_gear(self) -> '_2489.HypoidGear':
        """HypoidGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2489.HypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to HypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2491.KlingelnbergCycloPalloidConicalGear':
        """KlingelnbergCycloPalloidConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2491.KlingelnbergCycloPalloidConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2493.KlingelnbergCycloPalloidHypoidGear':
        """KlingelnbergCycloPalloidHypoidGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2493.KlingelnbergCycloPalloidHypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2495.KlingelnbergCycloPalloidSpiralBevelGear':
        """KlingelnbergCycloPalloidSpiralBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2495.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_spiral_bevel_gear(self) -> '_2498.SpiralBevelGear':
        """SpiralBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2498.SpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_straight_bevel_diff_gear(self) -> '_2500.StraightBevelDiffGear':
        """StraightBevelDiffGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2500.StraightBevelDiffGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelDiffGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_straight_bevel_gear(self) -> '_2502.StraightBevelGear':
        """StraightBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2502.StraightBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_straight_bevel_planet_gear(self) -> '_2504.StraightBevelPlanetGear':
        """StraightBevelPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2504.StraightBevelPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_straight_bevel_sun_gear(self) -> '_2505.StraightBevelSunGear':
        """StraightBevelSunGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2505.StraightBevelSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_worm_gear(self) -> '_2506.WormGear':
        """WormGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2506.WormGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to WormGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_zerol_bevel_gear(self) -> '_2508.ZerolBevelGear':
        """ZerolBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2508.ZerolBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ZerolBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_ring_pins(self) -> '_2525.RingPins':
        """RingPins: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2525.RingPins.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to RingPins. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_clutch_half(self) -> '_2534.ClutchHalf':
        """ClutchHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2534.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_concept_coupling_half(self) -> '_2537.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2537.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_coupling_half(self) -> '_2539.CouplingHalf':
        """CouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2539.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_cvt_pulley(self) -> '_2542.CVTPulley':
        """CVTPulley: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2542.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_part_to_part_shear_coupling_half(self) -> '_2544.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2544.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_pulley(self) -> '_2545.Pulley':
        """Pulley: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2545.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_rolling_ring(self) -> '_2551.RollingRing':
        """RollingRing: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2551.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_shaft_hub_connection(self) -> '_2553.ShaftHubConnection':
        """ShaftHubConnection: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2553.ShaftHubConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ShaftHubConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_spring_damper_half(self) -> '_2556.SpringDamperHalf':
        """SpringDamperHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2556.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_synchroniser_half(self) -> '_2559.SynchroniserHalf':
        """SynchroniserHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2559.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_synchroniser_part(self) -> '_2560.SynchroniserPart':
        """SynchroniserPart: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2560.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_synchroniser_sleeve(self) -> '_2561.SynchroniserSleeve':
        """SynchroniserSleeve: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2561.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_torque_converter_pump(self) -> '_2563.TorqueConverterPump':
        """TorqueConverterPump: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2563.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_torque_converter_turbine(self) -> '_2565.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2565.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaft(self) -> '_2392.AbstractShaft':
        """AbstractShaft: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shaft

        if temp is None:
            return None

        if _2392.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast shaft to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaft_of_type_shaft(self) -> '_2438.Shaft':
        """Shaft: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shaft

        if temp is None:
            return None

        if _2438.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast shaft to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaft_of_type_cycloidal_disc(self) -> '_2524.CycloidalDisc':
        """CycloidalDisc: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shaft

        if temp is None:
            return None

        if _2524.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast shaft to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
