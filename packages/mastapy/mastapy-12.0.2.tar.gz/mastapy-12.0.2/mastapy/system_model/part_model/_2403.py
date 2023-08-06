"""_2403.py

Connector
"""


from typing import Optional

from mastapy.system_model.part_model import (
    _2392, _2400, _2401, _2420
)
from mastapy._internal import constructor
from mastapy.system_model.part_model.shaft_model import _2438
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.cycloidal import _2524
from mastapy.system_model.connections_and_sockets import (
    _2230, _2223, _2226, _2227,
    _2231, _2239, _2245, _2250,
    _2253, _2234, _2224, _2225,
    _2232, _2237, _2238, _2240,
    _2241, _2242, _2243, _2244,
    _2246, _2247, _2248, _2251,
    _2252
)
from mastapy.system_model.connections_and_sockets.gears import (
    _2257, _2259, _2261, _2263,
    _2265, _2267, _2269, _2271,
    _2273, _2276, _2277, _2278,
    _2281, _2283, _2285, _2287,
    _2289, _2268
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2293, _2296, _2299, _2291,
    _2292, _2294, _2295, _2297,
    _2298
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2300, _2302, _2304, _2306,
    _2308, _2310, _2301, _2303,
    _2305, _2307, _2309, _2311,
    _2312
)
from mastapy._internal.python_net import python_net_import

_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')


__docformat__ = 'restructuredtext en'
__all__ = ('Connector',)


class Connector(_2420.MountableComponent):
    """Connector

    This is a mastapy class.
    """

    TYPE = _CONNECTOR

    def __init__(self, instance_to_wrap: 'Connector.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def outer_component(self) -> '_2392.AbstractShaft':
        """AbstractShaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterComponent

        if temp is None:
            return None

        if _2392.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_component to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_component_of_type_shaft(self) -> '_2438.Shaft':
        """Shaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterComponent

        if temp is None:
            return None

        if _2438.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_component to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_component_of_type_cycloidal_disc(self) -> '_2524.CycloidalDisc':
        """CycloidalDisc: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterComponent

        if temp is None:
            return None

        if _2524.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_component to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection(self) -> '_2230.Connection':
        """Connection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2230.Connection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to Connection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_2223.AbstractShaftToMountableComponentConnection':
        """AbstractShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2223.AbstractShaftToMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_belt_connection(self) -> '_2226.BeltConnection':
        """BeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2226.BeltConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BeltConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_coaxial_connection(self) -> '_2227.CoaxialConnection':
        """CoaxialConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2227.CoaxialConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CoaxialConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_cvt_belt_connection(self) -> '_2231.CVTBeltConnection':
        """CVTBeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2231.CVTBeltConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CVTBeltConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_inter_mountable_component_connection(self) -> '_2239.InterMountableComponentConnection':
        """InterMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2239.InterMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to InterMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_planetary_connection(self) -> '_2245.PlanetaryConnection':
        """PlanetaryConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2245.PlanetaryConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PlanetaryConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_rolling_ring_connection(self) -> '_2250.RollingRingConnection':
        """RollingRingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2250.RollingRingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RollingRingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_shaft_to_mountable_component_connection(self) -> '_2253.ShaftToMountableComponentConnection':
        """ShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2253.ShaftToMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ShaftToMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_agma_gleason_conical_gear_mesh(self) -> '_2257.AGMAGleasonConicalGearMesh':
        """AGMAGleasonConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2257.AGMAGleasonConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AGMAGleasonConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_bevel_differential_gear_mesh(self) -> '_2259.BevelDifferentialGearMesh':
        """BevelDifferentialGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2259.BevelDifferentialGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelDifferentialGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_bevel_gear_mesh(self) -> '_2261.BevelGearMesh':
        """BevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2261.BevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_concept_gear_mesh(self) -> '_2263.ConceptGearMesh':
        """ConceptGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2263.ConceptGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_conical_gear_mesh(self) -> '_2265.ConicalGearMesh':
        """ConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2265.ConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_cylindrical_gear_mesh(self) -> '_2267.CylindricalGearMesh':
        """CylindricalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2267.CylindricalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CylindricalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_face_gear_mesh(self) -> '_2269.FaceGearMesh':
        """FaceGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2269.FaceGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to FaceGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_gear_mesh(self) -> '_2271.GearMesh':
        """GearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2271.GearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to GearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_hypoid_gear_mesh(self) -> '_2273.HypoidGearMesh':
        """HypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2273.HypoidGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to HypoidGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_2276.KlingelnbergCycloPalloidConicalGearMesh':
        """KlingelnbergCycloPalloidConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2276.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2277.KlingelnbergCycloPalloidHypoidGearMesh':
        """KlingelnbergCycloPalloidHypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2277.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2278.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        """KlingelnbergCycloPalloidSpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2278.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_spiral_bevel_gear_mesh(self) -> '_2281.SpiralBevelGearMesh':
        """SpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2281.SpiralBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpiralBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_straight_bevel_diff_gear_mesh(self) -> '_2283.StraightBevelDiffGearMesh':
        """StraightBevelDiffGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2283.StraightBevelDiffGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelDiffGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_straight_bevel_gear_mesh(self) -> '_2285.StraightBevelGearMesh':
        """StraightBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2285.StraightBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_worm_gear_mesh(self) -> '_2287.WormGearMesh':
        """WormGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2287.WormGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to WormGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_zerol_bevel_gear_mesh(self) -> '_2289.ZerolBevelGearMesh':
        """ZerolBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2289.ZerolBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ZerolBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2293.CycloidalDiscCentralBearingConnection':
        """CycloidalDiscCentralBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2293.CycloidalDiscCentralBearingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2296.CycloidalDiscPlanetaryBearingConnection':
        """CycloidalDiscPlanetaryBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2296.CycloidalDiscPlanetaryBearingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_ring_pins_to_disc_connection(self) -> '_2299.RingPinsToDiscConnection':
        """RingPinsToDiscConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2299.RingPinsToDiscConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RingPinsToDiscConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_clutch_connection(self) -> '_2300.ClutchConnection':
        """ClutchConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2300.ClutchConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ClutchConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_concept_coupling_connection(self) -> '_2302.ConceptCouplingConnection':
        """ConceptCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2302.ConceptCouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptCouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_coupling_connection(self) -> '_2304.CouplingConnection':
        """CouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2304.CouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_part_to_part_shear_coupling_connection(self) -> '_2306.PartToPartShearCouplingConnection':
        """PartToPartShearCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2306.PartToPartShearCouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PartToPartShearCouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_spring_damper_connection(self) -> '_2308.SpringDamperConnection':
        """SpringDamperConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2308.SpringDamperConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpringDamperConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_torque_converter_connection(self) -> '_2310.TorqueConverterConnection':
        """TorqueConverterConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2310.TorqueConverterConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to TorqueConverterConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket(self) -> '_2234.CylindricalSocket':
        """CylindricalSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2234.CylindricalSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_bearing_inner_socket(self) -> '_2224.BearingInnerSocket':
        """BearingInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2224.BearingInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to BearingInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_bearing_outer_socket(self) -> '_2225.BearingOuterSocket':
        """BearingOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2225.BearingOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to BearingOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cvt_pulley_socket(self) -> '_2232.CVTPulleySocket':
        """CVTPulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2232.CVTPulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CVTPulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_inner_shaft_socket(self) -> '_2237.InnerShaftSocket':
        """InnerShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2237.InnerShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_inner_shaft_socket_base(self) -> '_2238.InnerShaftSocketBase':
        """InnerShaftSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2238.InnerShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_mountable_component_inner_socket(self) -> '_2240.MountableComponentInnerSocket':
        """MountableComponentInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2240.MountableComponentInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_mountable_component_outer_socket(self) -> '_2241.MountableComponentOuterSocket':
        """MountableComponentOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2241.MountableComponentOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_mountable_component_socket(self) -> '_2242.MountableComponentSocket':
        """MountableComponentSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2242.MountableComponentSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_outer_shaft_socket(self) -> '_2243.OuterShaftSocket':
        """OuterShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2243.OuterShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_outer_shaft_socket_base(self) -> '_2244.OuterShaftSocketBase':
        """OuterShaftSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2244.OuterShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_planetary_socket(self) -> '_2246.PlanetarySocket':
        """PlanetarySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2246.PlanetarySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_planetary_socket_base(self) -> '_2247.PlanetarySocketBase':
        """PlanetarySocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2247.PlanetarySocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_pulley_socket(self) -> '_2248.PulleySocket':
        """PulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2248.PulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_rolling_ring_socket(self) -> '_2251.RollingRingSocket':
        """RollingRingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2251.RollingRingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RollingRingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_shaft_socket(self) -> '_2252.ShaftSocket':
        """ShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2252.ShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cylindrical_gear_teeth_socket(self) -> '_2268.CylindricalGearTeethSocket':
        """CylindricalGearTeethSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2268.CylindricalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_axial_left_socket(self) -> '_2291.CycloidalDiscAxialLeftSocket':
        """CycloidalDiscAxialLeftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2291.CycloidalDiscAxialLeftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_axial_right_socket(self) -> '_2292.CycloidalDiscAxialRightSocket':
        """CycloidalDiscAxialRightSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2292.CycloidalDiscAxialRightSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscAxialRightSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_inner_socket(self) -> '_2294.CycloidalDiscInnerSocket':
        """CycloidalDiscInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2294.CycloidalDiscInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_outer_socket(self) -> '_2295.CycloidalDiscOuterSocket':
        """CycloidalDiscOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2295.CycloidalDiscOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2297.CycloidalDiscPlanetaryBearingSocket':
        """CycloidalDiscPlanetaryBearingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2297.CycloidalDiscPlanetaryBearingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_ring_pins_socket(self) -> '_2298.RingPinsSocket':
        """RingPinsSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2298.RingPinsSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RingPinsSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_clutch_socket(self) -> '_2301.ClutchSocket':
        """ClutchSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2301.ClutchSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ClutchSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_concept_coupling_socket(self) -> '_2303.ConceptCouplingSocket':
        """ConceptCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2303.ConceptCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ConceptCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_coupling_socket(self) -> '_2305.CouplingSocket':
        """CouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2305.CouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_part_to_part_shear_coupling_socket(self) -> '_2307.PartToPartShearCouplingSocket':
        """PartToPartShearCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2307.PartToPartShearCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PartToPartShearCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_spring_damper_socket(self) -> '_2309.SpringDamperSocket':
        """SpringDamperSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2309.SpringDamperSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to SpringDamperSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_torque_converter_pump_socket(self) -> '_2311.TorqueConverterPumpSocket':
        """TorqueConverterPumpSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2311.TorqueConverterPumpSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterPumpSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_torque_converter_turbine_socket(self) -> '_2312.TorqueConverterTurbineSocket':
        """TorqueConverterTurbineSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2312.TorqueConverterTurbineSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterTurbineSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def house_in(self, shaft: '_2392.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2230.Connection':
        """ 'HouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.connections_and_sockets.Connection
        """

        offset = float(offset)
        method_result = self.wrapped.HouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def other_component(self, component: '_2400.Component') -> '_2392.AbstractShaft':
        """ 'OtherComponent' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.AbstractShaft
        """

        method_result = self.wrapped.OtherComponent(component.wrapped if component else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def try_house_in(self, shaft: '_2392.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2401.ComponentsConnectedResult':
        """ 'TryHouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        """

        offset = float(offset)
        method_result = self.wrapped.TryHouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
