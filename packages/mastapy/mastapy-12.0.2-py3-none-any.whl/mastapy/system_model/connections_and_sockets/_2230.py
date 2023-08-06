"""_2230.py

Connection
"""


from mastapy._internal import constructor
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.part_model import (
    _2400, _2392, _2393, _2396,
    _2398, _2403, _2404, _2408,
    _2409, _2411, _2418, _2419,
    _2420, _2422, _2425, _2427,
    _2428, _2433, _2435
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2438
from mastapy.system_model.part_model.gears import (
    _2468, _2470, _2472, _2473,
    _2474, _2476, _2478, _2480,
    _2482, _2483, _2485, _2489,
    _2491, _2493, _2495, _2498,
    _2500, _2502, _2504, _2505,
    _2506, _2508
)
from mastapy.system_model.part_model.cycloidal import _2524, _2525
from mastapy.system_model.part_model.couplings import (
    _2534, _2537, _2539, _2542,
    _2544, _2545, _2551, _2553,
    _2556, _2559, _2560, _2561,
    _2563, _2565
)
from mastapy.system_model.connections_and_sockets import (
    _2254, _2224, _2225, _2232,
    _2234, _2236, _2237, _2238,
    _2240, _2241, _2242, _2243,
    _2244, _2246, _2247, _2248,
    _2251, _2252
)
from mastapy.system_model.connections_and_sockets.gears import (
    _2258, _2260, _2262, _2264,
    _2266, _2268, _2270, _2272,
    _2274, _2275, _2279, _2280,
    _2282, _2284, _2286, _2288,
    _2290
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2291, _2292, _2294, _2295,
    _2297, _2298
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2301, _2303, _2305, _2307,
    _2309, _2311, _2312
)
from mastapy._internal.python_net import python_net_import
from mastapy.system_model import _2164

_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Socket')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')


__docformat__ = 'restructuredtext en'
__all__ = ('Connection',)


class Connection(_2164.DesignEntity):
    """Connection

    This is a mastapy class.
    """

    TYPE = _CONNECTION

    def __init__(self, instance_to_wrap: 'Connection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_id(self) -> 'str':
        """str: 'ConnectionID' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionID

        if temp is None:
            return ''

        return temp

    @property
    def drawing_position(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'DrawingPosition' is the original name of this property."""

        temp = self.wrapped.DrawingPosition

        if temp is None:
            return ''

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else ''

    @drawing_position.setter
    def drawing_position(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.DrawingPosition = value

    @property
    def speed_ratio_from_a_to_b(self) -> 'float':
        """float: 'SpeedRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpeedRatioFromAToB

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_ratio_from_a_to_b(self) -> 'float':
        """float: 'TorqueRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueRatioFromAToB

        if temp is None:
            return 0.0

        return temp

    @property
    def unique_name(self) -> 'str':
        """str: 'UniqueName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UniqueName

        if temp is None:
            return ''

        return temp

    @property
    def owner_a(self) -> '_2400.Component':
        """Component: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2400.Component.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Component. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_abstract_shaft(self) -> '_2392.AbstractShaft':
        """AbstractShaft: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2392.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_abstract_shaft_or_housing(self) -> '_2393.AbstractShaftOrHousing':
        """AbstractShaftOrHousing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2393.AbstractShaftOrHousing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AbstractShaftOrHousing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bearing(self) -> '_2396.Bearing':
        """Bearing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2396.Bearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bolt(self) -> '_2398.Bolt':
        """Bolt: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2398.Bolt.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bolt. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_connector(self) -> '_2403.Connector':
        """Connector: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2403.Connector.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Connector. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_datum(self) -> '_2404.Datum':
        """Datum: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2404.Datum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Datum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_external_cad_model(self) -> '_2408.ExternalCADModel':
        """ExternalCADModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2408.ExternalCADModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ExternalCADModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_fe_part(self) -> '_2409.FEPart':
        """FEPart: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2409.FEPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to FEPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_guide_dxf_model(self) -> '_2411.GuideDxfModel':
        """GuideDxfModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2411.GuideDxfModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to GuideDxfModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_mass_disc(self) -> '_2418.MassDisc':
        """MassDisc: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2418.MassDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MassDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_measurement_component(self) -> '_2419.MeasurementComponent':
        """MeasurementComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2419.MeasurementComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MeasurementComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_mountable_component(self) -> '_2420.MountableComponent':
        """MountableComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2420.MountableComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MountableComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_oil_seal(self) -> '_2422.OilSeal':
        """OilSeal: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2422.OilSeal.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to OilSeal. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_planet_carrier(self) -> '_2425.PlanetCarrier':
        """PlanetCarrier: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2425.PlanetCarrier.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PlanetCarrier. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_point_load(self) -> '_2427.PointLoad':
        """PointLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2427.PointLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PointLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_power_load(self) -> '_2428.PowerLoad':
        """PowerLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2428.PowerLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PowerLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_unbalanced_mass(self) -> '_2433.UnbalancedMass':
        """UnbalancedMass: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2433.UnbalancedMass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to UnbalancedMass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_virtual_component(self) -> '_2435.VirtualComponent':
        """VirtualComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2435.VirtualComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to VirtualComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_shaft(self) -> '_2438.Shaft':
        """Shaft: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2438.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_agma_gleason_conical_gear(self) -> '_2468.AGMAGleasonConicalGear':
        """AGMAGleasonConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2468.AGMAGleasonConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AGMAGleasonConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bevel_differential_gear(self) -> '_2470.BevelDifferentialGear':
        """BevelDifferentialGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2470.BevelDifferentialGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bevel_differential_planet_gear(self) -> '_2472.BevelDifferentialPlanetGear':
        """BevelDifferentialPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2472.BevelDifferentialPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bevel_differential_sun_gear(self) -> '_2473.BevelDifferentialSunGear':
        """BevelDifferentialSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2473.BevelDifferentialSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bevel_gear(self) -> '_2474.BevelGear':
        """BevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2474.BevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_concept_gear(self) -> '_2476.ConceptGear':
        """ConceptGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2476.ConceptGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_conical_gear(self) -> '_2478.ConicalGear':
        """ConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2478.ConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_cylindrical_gear(self) -> '_2480.CylindricalGear':
        """CylindricalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2480.CylindricalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_cylindrical_planet_gear(self) -> '_2482.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2482.CylindricalPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_face_gear(self) -> '_2483.FaceGear':
        """FaceGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2483.FaceGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to FaceGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_gear(self) -> '_2485.Gear':
        """Gear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2485.Gear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Gear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_hypoid_gear(self) -> '_2489.HypoidGear':
        """HypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2489.HypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to HypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2491.KlingelnbergCycloPalloidConicalGear':
        """KlingelnbergCycloPalloidConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2491.KlingelnbergCycloPalloidConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2493.KlingelnbergCycloPalloidHypoidGear':
        """KlingelnbergCycloPalloidHypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2493.KlingelnbergCycloPalloidHypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2495.KlingelnbergCycloPalloidSpiralBevelGear':
        """KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2495.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_spiral_bevel_gear(self) -> '_2498.SpiralBevelGear':
        """SpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2498.SpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_straight_bevel_diff_gear(self) -> '_2500.StraightBevelDiffGear':
        """StraightBevelDiffGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2500.StraightBevelDiffGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelDiffGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_straight_bevel_gear(self) -> '_2502.StraightBevelGear':
        """StraightBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2502.StraightBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_straight_bevel_planet_gear(self) -> '_2504.StraightBevelPlanetGear':
        """StraightBevelPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2504.StraightBevelPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_straight_bevel_sun_gear(self) -> '_2505.StraightBevelSunGear':
        """StraightBevelSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2505.StraightBevelSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_worm_gear(self) -> '_2506.WormGear':
        """WormGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2506.WormGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to WormGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_zerol_bevel_gear(self) -> '_2508.ZerolBevelGear':
        """ZerolBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2508.ZerolBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ZerolBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_cycloidal_disc(self) -> '_2524.CycloidalDisc':
        """CycloidalDisc: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2524.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_ring_pins(self) -> '_2525.RingPins':
        """RingPins: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2525.RingPins.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to RingPins. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_clutch_half(self) -> '_2534.ClutchHalf':
        """ClutchHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2534.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_concept_coupling_half(self) -> '_2537.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2537.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_coupling_half(self) -> '_2539.CouplingHalf':
        """CouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2539.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_cvt_pulley(self) -> '_2542.CVTPulley':
        """CVTPulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2542.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_part_to_part_shear_coupling_half(self) -> '_2544.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2544.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_pulley(self) -> '_2545.Pulley':
        """Pulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2545.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_rolling_ring(self) -> '_2551.RollingRing':
        """RollingRing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2551.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_shaft_hub_connection(self) -> '_2553.ShaftHubConnection':
        """ShaftHubConnection: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2553.ShaftHubConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ShaftHubConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_spring_damper_half(self) -> '_2556.SpringDamperHalf':
        """SpringDamperHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2556.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_synchroniser_half(self) -> '_2559.SynchroniserHalf':
        """SynchroniserHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2559.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_synchroniser_part(self) -> '_2560.SynchroniserPart':
        """SynchroniserPart: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2560.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_synchroniser_sleeve(self) -> '_2561.SynchroniserSleeve':
        """SynchroniserSleeve: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2561.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_torque_converter_pump(self) -> '_2563.TorqueConverterPump':
        """TorqueConverterPump: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2563.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_torque_converter_turbine(self) -> '_2565.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2565.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b(self) -> '_2400.Component':
        """Component: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2400.Component.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Component. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_abstract_shaft(self) -> '_2392.AbstractShaft':
        """AbstractShaft: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2392.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_abstract_shaft_or_housing(self) -> '_2393.AbstractShaftOrHousing':
        """AbstractShaftOrHousing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2393.AbstractShaftOrHousing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AbstractShaftOrHousing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bearing(self) -> '_2396.Bearing':
        """Bearing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2396.Bearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bolt(self) -> '_2398.Bolt':
        """Bolt: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2398.Bolt.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bolt. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_connector(self) -> '_2403.Connector':
        """Connector: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2403.Connector.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Connector. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_datum(self) -> '_2404.Datum':
        """Datum: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2404.Datum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Datum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_external_cad_model(self) -> '_2408.ExternalCADModel':
        """ExternalCADModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2408.ExternalCADModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ExternalCADModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_fe_part(self) -> '_2409.FEPart':
        """FEPart: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2409.FEPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to FEPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_guide_dxf_model(self) -> '_2411.GuideDxfModel':
        """GuideDxfModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2411.GuideDxfModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to GuideDxfModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_mass_disc(self) -> '_2418.MassDisc':
        """MassDisc: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2418.MassDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MassDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_measurement_component(self) -> '_2419.MeasurementComponent':
        """MeasurementComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2419.MeasurementComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MeasurementComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_mountable_component(self) -> '_2420.MountableComponent':
        """MountableComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2420.MountableComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MountableComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_oil_seal(self) -> '_2422.OilSeal':
        """OilSeal: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2422.OilSeal.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to OilSeal. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_planet_carrier(self) -> '_2425.PlanetCarrier':
        """PlanetCarrier: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2425.PlanetCarrier.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PlanetCarrier. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_point_load(self) -> '_2427.PointLoad':
        """PointLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2427.PointLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PointLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_power_load(self) -> '_2428.PowerLoad':
        """PowerLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2428.PowerLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PowerLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_unbalanced_mass(self) -> '_2433.UnbalancedMass':
        """UnbalancedMass: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2433.UnbalancedMass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to UnbalancedMass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_virtual_component(self) -> '_2435.VirtualComponent':
        """VirtualComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2435.VirtualComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to VirtualComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_shaft(self) -> '_2438.Shaft':
        """Shaft: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2438.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_agma_gleason_conical_gear(self) -> '_2468.AGMAGleasonConicalGear':
        """AGMAGleasonConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2468.AGMAGleasonConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AGMAGleasonConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bevel_differential_gear(self) -> '_2470.BevelDifferentialGear':
        """BevelDifferentialGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2470.BevelDifferentialGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bevel_differential_planet_gear(self) -> '_2472.BevelDifferentialPlanetGear':
        """BevelDifferentialPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2472.BevelDifferentialPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bevel_differential_sun_gear(self) -> '_2473.BevelDifferentialSunGear':
        """BevelDifferentialSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2473.BevelDifferentialSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bevel_gear(self) -> '_2474.BevelGear':
        """BevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2474.BevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_concept_gear(self) -> '_2476.ConceptGear':
        """ConceptGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2476.ConceptGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_conical_gear(self) -> '_2478.ConicalGear':
        """ConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2478.ConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_cylindrical_gear(self) -> '_2480.CylindricalGear':
        """CylindricalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2480.CylindricalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_cylindrical_planet_gear(self) -> '_2482.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2482.CylindricalPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_face_gear(self) -> '_2483.FaceGear':
        """FaceGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2483.FaceGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to FaceGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_gear(self) -> '_2485.Gear':
        """Gear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2485.Gear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Gear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_hypoid_gear(self) -> '_2489.HypoidGear':
        """HypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2489.HypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to HypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2491.KlingelnbergCycloPalloidConicalGear':
        """KlingelnbergCycloPalloidConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2491.KlingelnbergCycloPalloidConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2493.KlingelnbergCycloPalloidHypoidGear':
        """KlingelnbergCycloPalloidHypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2493.KlingelnbergCycloPalloidHypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2495.KlingelnbergCycloPalloidSpiralBevelGear':
        """KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2495.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_spiral_bevel_gear(self) -> '_2498.SpiralBevelGear':
        """SpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2498.SpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_straight_bevel_diff_gear(self) -> '_2500.StraightBevelDiffGear':
        """StraightBevelDiffGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2500.StraightBevelDiffGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelDiffGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_straight_bevel_gear(self) -> '_2502.StraightBevelGear':
        """StraightBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2502.StraightBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_straight_bevel_planet_gear(self) -> '_2504.StraightBevelPlanetGear':
        """StraightBevelPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2504.StraightBevelPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_straight_bevel_sun_gear(self) -> '_2505.StraightBevelSunGear':
        """StraightBevelSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2505.StraightBevelSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_worm_gear(self) -> '_2506.WormGear':
        """WormGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2506.WormGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to WormGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_zerol_bevel_gear(self) -> '_2508.ZerolBevelGear':
        """ZerolBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2508.ZerolBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ZerolBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_cycloidal_disc(self) -> '_2524.CycloidalDisc':
        """CycloidalDisc: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2524.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_ring_pins(self) -> '_2525.RingPins':
        """RingPins: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2525.RingPins.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to RingPins. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_clutch_half(self) -> '_2534.ClutchHalf':
        """ClutchHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2534.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_concept_coupling_half(self) -> '_2537.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2537.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_coupling_half(self) -> '_2539.CouplingHalf':
        """CouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2539.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_cvt_pulley(self) -> '_2542.CVTPulley':
        """CVTPulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2542.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_part_to_part_shear_coupling_half(self) -> '_2544.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2544.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_pulley(self) -> '_2545.Pulley':
        """Pulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2545.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_rolling_ring(self) -> '_2551.RollingRing':
        """RollingRing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2551.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_shaft_hub_connection(self) -> '_2553.ShaftHubConnection':
        """ShaftHubConnection: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2553.ShaftHubConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ShaftHubConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_spring_damper_half(self) -> '_2556.SpringDamperHalf':
        """SpringDamperHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2556.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_synchroniser_half(self) -> '_2559.SynchroniserHalf':
        """SynchroniserHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2559.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_synchroniser_part(self) -> '_2560.SynchroniserPart':
        """SynchroniserPart: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2560.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_synchroniser_sleeve(self) -> '_2561.SynchroniserSleeve':
        """SynchroniserSleeve: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2561.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_torque_converter_pump(self) -> '_2563.TorqueConverterPump':
        """TorqueConverterPump: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2563.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_torque_converter_turbine(self) -> '_2565.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2565.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a(self) -> '_2254.Socket':
        """Socket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2254.Socket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to Socket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_bearing_inner_socket(self) -> '_2224.BearingInnerSocket':
        """BearingInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2224.BearingInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BearingInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_bearing_outer_socket(self) -> '_2225.BearingOuterSocket':
        """BearingOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2225.BearingOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BearingOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cvt_pulley_socket(self) -> '_2232.CVTPulleySocket':
        """CVTPulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2232.CVTPulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CVTPulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cylindrical_socket(self) -> '_2234.CylindricalSocket':
        """CylindricalSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2234.CylindricalSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_electric_machine_stator_socket(self) -> '_2236.ElectricMachineStatorSocket':
        """ElectricMachineStatorSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2236.ElectricMachineStatorSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ElectricMachineStatorSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_inner_shaft_socket(self) -> '_2237.InnerShaftSocket':
        """InnerShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2237.InnerShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_inner_shaft_socket_base(self) -> '_2238.InnerShaftSocketBase':
        """InnerShaftSocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2238.InnerShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_mountable_component_inner_socket(self) -> '_2240.MountableComponentInnerSocket':
        """MountableComponentInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2240.MountableComponentInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_mountable_component_outer_socket(self) -> '_2241.MountableComponentOuterSocket':
        """MountableComponentOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2241.MountableComponentOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_mountable_component_socket(self) -> '_2242.MountableComponentSocket':
        """MountableComponentSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2242.MountableComponentSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_outer_shaft_socket(self) -> '_2243.OuterShaftSocket':
        """OuterShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2243.OuterShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_outer_shaft_socket_base(self) -> '_2244.OuterShaftSocketBase':
        """OuterShaftSocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2244.OuterShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_planetary_socket(self) -> '_2246.PlanetarySocket':
        """PlanetarySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2246.PlanetarySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PlanetarySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_planetary_socket_base(self) -> '_2247.PlanetarySocketBase':
        """PlanetarySocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2247.PlanetarySocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PlanetarySocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_pulley_socket(self) -> '_2248.PulleySocket':
        """PulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2248.PulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_rolling_ring_socket(self) -> '_2251.RollingRingSocket':
        """RollingRingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2251.RollingRingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to RollingRingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_shaft_socket(self) -> '_2252.ShaftSocket':
        """ShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2252.ShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_2258.AGMAGleasonConicalGearTeethSocket':
        """AGMAGleasonConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2258.AGMAGleasonConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_bevel_differential_gear_teeth_socket(self) -> '_2260.BevelDifferentialGearTeethSocket':
        """BevelDifferentialGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2260.BevelDifferentialGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelDifferentialGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_bevel_gear_teeth_socket(self) -> '_2262.BevelGearTeethSocket':
        """BevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2262.BevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_concept_gear_teeth_socket(self) -> '_2264.ConceptGearTeethSocket':
        """ConceptGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2264.ConceptGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_conical_gear_teeth_socket(self) -> '_2266.ConicalGearTeethSocket':
        """ConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2266.ConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cylindrical_gear_teeth_socket(self) -> '_2268.CylindricalGearTeethSocket':
        """CylindricalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2268.CylindricalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_face_gear_teeth_socket(self) -> '_2270.FaceGearTeethSocket':
        """FaceGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2270.FaceGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to FaceGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_gear_teeth_socket(self) -> '_2272.GearTeethSocket':
        """GearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2272.GearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to GearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_hypoid_gear_teeth_socket(self) -> '_2274.HypoidGearTeethSocket':
        """HypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2274.HypoidGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to HypoidGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_2275.KlingelnbergConicalGearTeethSocket':
        """KlingelnbergConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2275.KlingelnbergConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_2279.KlingelnbergHypoidGearTeethSocket':
        """KlingelnbergHypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2279.KlingelnbergHypoidGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_2280.KlingelnbergSpiralBevelGearTeethSocket':
        """KlingelnbergSpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2280.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_spiral_bevel_gear_teeth_socket(self) -> '_2282.SpiralBevelGearTeethSocket':
        """SpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2282.SpiralBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpiralBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_2284.StraightBevelDiffGearTeethSocket':
        """StraightBevelDiffGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2284.StraightBevelDiffGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_straight_bevel_gear_teeth_socket(self) -> '_2286.StraightBevelGearTeethSocket':
        """StraightBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2286.StraightBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_worm_gear_teeth_socket(self) -> '_2288.WormGearTeethSocket':
        """WormGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2288.WormGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to WormGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_zerol_bevel_gear_teeth_socket(self) -> '_2290.ZerolBevelGearTeethSocket':
        """ZerolBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2290.ZerolBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ZerolBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_axial_left_socket(self) -> '_2291.CycloidalDiscAxialLeftSocket':
        """CycloidalDiscAxialLeftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2291.CycloidalDiscAxialLeftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_axial_right_socket(self) -> '_2292.CycloidalDiscAxialRightSocket':
        """CycloidalDiscAxialRightSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2292.CycloidalDiscAxialRightSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscAxialRightSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_inner_socket(self) -> '_2294.CycloidalDiscInnerSocket':
        """CycloidalDiscInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2294.CycloidalDiscInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_outer_socket(self) -> '_2295.CycloidalDiscOuterSocket':
        """CycloidalDiscOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2295.CycloidalDiscOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2297.CycloidalDiscPlanetaryBearingSocket':
        """CycloidalDiscPlanetaryBearingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2297.CycloidalDiscPlanetaryBearingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_ring_pins_socket(self) -> '_2298.RingPinsSocket':
        """RingPinsSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2298.RingPinsSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to RingPinsSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_clutch_socket(self) -> '_2301.ClutchSocket':
        """ClutchSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2301.ClutchSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ClutchSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_concept_coupling_socket(self) -> '_2303.ConceptCouplingSocket':
        """ConceptCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2303.ConceptCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_coupling_socket(self) -> '_2305.CouplingSocket':
        """CouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2305.CouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_part_to_part_shear_coupling_socket(self) -> '_2307.PartToPartShearCouplingSocket':
        """PartToPartShearCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2307.PartToPartShearCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PartToPartShearCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_spring_damper_socket(self) -> '_2309.SpringDamperSocket':
        """SpringDamperSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2309.SpringDamperSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpringDamperSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_torque_converter_pump_socket(self) -> '_2311.TorqueConverterPumpSocket':
        """TorqueConverterPumpSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2311.TorqueConverterPumpSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterPumpSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_torque_converter_turbine_socket(self) -> '_2312.TorqueConverterTurbineSocket':
        """TorqueConverterTurbineSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2312.TorqueConverterTurbineSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterTurbineSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b(self) -> '_2254.Socket':
        """Socket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2254.Socket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to Socket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_bearing_inner_socket(self) -> '_2224.BearingInnerSocket':
        """BearingInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2224.BearingInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BearingInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_bearing_outer_socket(self) -> '_2225.BearingOuterSocket':
        """BearingOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2225.BearingOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BearingOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cvt_pulley_socket(self) -> '_2232.CVTPulleySocket':
        """CVTPulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2232.CVTPulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CVTPulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cylindrical_socket(self) -> '_2234.CylindricalSocket':
        """CylindricalSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2234.CylindricalSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_electric_machine_stator_socket(self) -> '_2236.ElectricMachineStatorSocket':
        """ElectricMachineStatorSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2236.ElectricMachineStatorSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ElectricMachineStatorSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_inner_shaft_socket(self) -> '_2237.InnerShaftSocket':
        """InnerShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2237.InnerShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_inner_shaft_socket_base(self) -> '_2238.InnerShaftSocketBase':
        """InnerShaftSocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2238.InnerShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_mountable_component_inner_socket(self) -> '_2240.MountableComponentInnerSocket':
        """MountableComponentInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2240.MountableComponentInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_mountable_component_outer_socket(self) -> '_2241.MountableComponentOuterSocket':
        """MountableComponentOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2241.MountableComponentOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_mountable_component_socket(self) -> '_2242.MountableComponentSocket':
        """MountableComponentSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2242.MountableComponentSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_outer_shaft_socket(self) -> '_2243.OuterShaftSocket':
        """OuterShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2243.OuterShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_outer_shaft_socket_base(self) -> '_2244.OuterShaftSocketBase':
        """OuterShaftSocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2244.OuterShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_planetary_socket(self) -> '_2246.PlanetarySocket':
        """PlanetarySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2246.PlanetarySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PlanetarySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_planetary_socket_base(self) -> '_2247.PlanetarySocketBase':
        """PlanetarySocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2247.PlanetarySocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PlanetarySocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_pulley_socket(self) -> '_2248.PulleySocket':
        """PulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2248.PulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_rolling_ring_socket(self) -> '_2251.RollingRingSocket':
        """RollingRingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2251.RollingRingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to RollingRingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_shaft_socket(self) -> '_2252.ShaftSocket':
        """ShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2252.ShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_2258.AGMAGleasonConicalGearTeethSocket':
        """AGMAGleasonConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2258.AGMAGleasonConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_bevel_differential_gear_teeth_socket(self) -> '_2260.BevelDifferentialGearTeethSocket':
        """BevelDifferentialGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2260.BevelDifferentialGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelDifferentialGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_bevel_gear_teeth_socket(self) -> '_2262.BevelGearTeethSocket':
        """BevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2262.BevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_concept_gear_teeth_socket(self) -> '_2264.ConceptGearTeethSocket':
        """ConceptGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2264.ConceptGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_conical_gear_teeth_socket(self) -> '_2266.ConicalGearTeethSocket':
        """ConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2266.ConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cylindrical_gear_teeth_socket(self) -> '_2268.CylindricalGearTeethSocket':
        """CylindricalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2268.CylindricalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_face_gear_teeth_socket(self) -> '_2270.FaceGearTeethSocket':
        """FaceGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2270.FaceGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to FaceGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_gear_teeth_socket(self) -> '_2272.GearTeethSocket':
        """GearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2272.GearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to GearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_hypoid_gear_teeth_socket(self) -> '_2274.HypoidGearTeethSocket':
        """HypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2274.HypoidGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to HypoidGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_2275.KlingelnbergConicalGearTeethSocket':
        """KlingelnbergConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2275.KlingelnbergConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_2279.KlingelnbergHypoidGearTeethSocket':
        """KlingelnbergHypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2279.KlingelnbergHypoidGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_2280.KlingelnbergSpiralBevelGearTeethSocket':
        """KlingelnbergSpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2280.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_spiral_bevel_gear_teeth_socket(self) -> '_2282.SpiralBevelGearTeethSocket':
        """SpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2282.SpiralBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpiralBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_2284.StraightBevelDiffGearTeethSocket':
        """StraightBevelDiffGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2284.StraightBevelDiffGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_straight_bevel_gear_teeth_socket(self) -> '_2286.StraightBevelGearTeethSocket':
        """StraightBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2286.StraightBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_worm_gear_teeth_socket(self) -> '_2288.WormGearTeethSocket':
        """WormGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2288.WormGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to WormGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_zerol_bevel_gear_teeth_socket(self) -> '_2290.ZerolBevelGearTeethSocket':
        """ZerolBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2290.ZerolBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ZerolBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_axial_left_socket(self) -> '_2291.CycloidalDiscAxialLeftSocket':
        """CycloidalDiscAxialLeftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2291.CycloidalDiscAxialLeftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_axial_right_socket(self) -> '_2292.CycloidalDiscAxialRightSocket':
        """CycloidalDiscAxialRightSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2292.CycloidalDiscAxialRightSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscAxialRightSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_inner_socket(self) -> '_2294.CycloidalDiscInnerSocket':
        """CycloidalDiscInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2294.CycloidalDiscInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_outer_socket(self) -> '_2295.CycloidalDiscOuterSocket':
        """CycloidalDiscOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2295.CycloidalDiscOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2297.CycloidalDiscPlanetaryBearingSocket':
        """CycloidalDiscPlanetaryBearingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2297.CycloidalDiscPlanetaryBearingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_ring_pins_socket(self) -> '_2298.RingPinsSocket':
        """RingPinsSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2298.RingPinsSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to RingPinsSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_clutch_socket(self) -> '_2301.ClutchSocket':
        """ClutchSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2301.ClutchSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ClutchSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_concept_coupling_socket(self) -> '_2303.ConceptCouplingSocket':
        """ConceptCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2303.ConceptCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_coupling_socket(self) -> '_2305.CouplingSocket':
        """CouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2305.CouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_part_to_part_shear_coupling_socket(self) -> '_2307.PartToPartShearCouplingSocket':
        """PartToPartShearCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2307.PartToPartShearCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PartToPartShearCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_spring_damper_socket(self) -> '_2309.SpringDamperSocket':
        """SpringDamperSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2309.SpringDamperSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpringDamperSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_torque_converter_pump_socket(self) -> '_2311.TorqueConverterPumpSocket':
        """TorqueConverterPumpSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2311.TorqueConverterPumpSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterPumpSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_torque_converter_turbine_socket(self) -> '_2312.TorqueConverterTurbineSocket':
        """TorqueConverterTurbineSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2312.TorqueConverterTurbineSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterTurbineSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def other_owner(self, component: '_2400.Component') -> '_2400.Component':
        """ 'OtherOwner' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.Component
        """

        method_result = self.wrapped.OtherOwner(component.wrapped if component else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def other_socket_for_component(self, component: '_2400.Component') -> '_2254.Socket':
        """ 'OtherSocket' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        """

        method_result = self.wrapped.OtherSocket.Overloads[_COMPONENT](component.wrapped if component else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def other_socket(self, socket: '_2254.Socket') -> '_2254.Socket':
        """ 'OtherSocket' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        """

        method_result = self.wrapped.OtherSocket.Overloads[_SOCKET](socket.wrapped if socket else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def socket_for(self, component: '_2400.Component') -> '_2254.Socket':
        """ 'SocketFor' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        """

        method_result = self.wrapped.SocketFor(component.wrapped if component else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
