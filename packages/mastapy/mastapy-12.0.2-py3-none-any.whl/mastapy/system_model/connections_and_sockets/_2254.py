"""_2254.py

Socket
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _2400, _2392, _2393, _2396,
    _2398, _2403, _2404, _2408,
    _2409, _2411, _2418, _2419,
    _2420, _2422, _2425, _2427,
    _2428, _2433, _2435, _2401
)
from mastapy.system_model.connections_and_sockets import _2230
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
from mastapy._internal.python_net import python_net_import
from mastapy import _0

_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Socket')


__docformat__ = 'restructuredtext en'
__all__ = ('Socket',)


class Socket(_0.APIBase):
    """Socket

    This is a mastapy class.
    """

    TYPE = _SOCKET

    def __init__(self, instance_to_wrap: 'Socket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return ''

        return temp

    @property
    def connected_components(self) -> 'List[_2400.Component]':
        """List[Component]: 'ConnectedComponents' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponents

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connections(self) -> 'List[_2230.Connection]':
        """List[Connection]: 'Connections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Connections

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def owner(self) -> '_2400.Component':
        """Component: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2400.Component.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to Component. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_abstract_shaft(self) -> '_2392.AbstractShaft':
        """AbstractShaft: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2392.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_abstract_shaft_or_housing(self) -> '_2393.AbstractShaftOrHousing':
        """AbstractShaftOrHousing: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2393.AbstractShaftOrHousing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to AbstractShaftOrHousing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_bearing(self) -> '_2396.Bearing':
        """Bearing: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2396.Bearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to Bearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_bolt(self) -> '_2398.Bolt':
        """Bolt: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2398.Bolt.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to Bolt. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_connector(self) -> '_2403.Connector':
        """Connector: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2403.Connector.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to Connector. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_datum(self) -> '_2404.Datum':
        """Datum: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2404.Datum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to Datum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_external_cad_model(self) -> '_2408.ExternalCADModel':
        """ExternalCADModel: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2408.ExternalCADModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to ExternalCADModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_fe_part(self) -> '_2409.FEPart':
        """FEPart: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2409.FEPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to FEPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_guide_dxf_model(self) -> '_2411.GuideDxfModel':
        """GuideDxfModel: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2411.GuideDxfModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to GuideDxfModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_mass_disc(self) -> '_2418.MassDisc':
        """MassDisc: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2418.MassDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to MassDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_measurement_component(self) -> '_2419.MeasurementComponent':
        """MeasurementComponent: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2419.MeasurementComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to MeasurementComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_mountable_component(self) -> '_2420.MountableComponent':
        """MountableComponent: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2420.MountableComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to MountableComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_oil_seal(self) -> '_2422.OilSeal':
        """OilSeal: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2422.OilSeal.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to OilSeal. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_planet_carrier(self) -> '_2425.PlanetCarrier':
        """PlanetCarrier: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2425.PlanetCarrier.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to PlanetCarrier. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_point_load(self) -> '_2427.PointLoad':
        """PointLoad: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2427.PointLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to PointLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_power_load(self) -> '_2428.PowerLoad':
        """PowerLoad: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2428.PowerLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to PowerLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_unbalanced_mass(self) -> '_2433.UnbalancedMass':
        """UnbalancedMass: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2433.UnbalancedMass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to UnbalancedMass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_virtual_component(self) -> '_2435.VirtualComponent':
        """VirtualComponent: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2435.VirtualComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to VirtualComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_shaft(self) -> '_2438.Shaft':
        """Shaft: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2438.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_agma_gleason_conical_gear(self) -> '_2468.AGMAGleasonConicalGear':
        """AGMAGleasonConicalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2468.AGMAGleasonConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to AGMAGleasonConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_bevel_differential_gear(self) -> '_2470.BevelDifferentialGear':
        """BevelDifferentialGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2470.BevelDifferentialGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelDifferentialGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_bevel_differential_planet_gear(self) -> '_2472.BevelDifferentialPlanetGear':
        """BevelDifferentialPlanetGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2472.BevelDifferentialPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelDifferentialPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_bevel_differential_sun_gear(self) -> '_2473.BevelDifferentialSunGear':
        """BevelDifferentialSunGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2473.BevelDifferentialSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelDifferentialSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_bevel_gear(self) -> '_2474.BevelGear':
        """BevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2474.BevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_concept_gear(self) -> '_2476.ConceptGear':
        """ConceptGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2476.ConceptGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to ConceptGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_conical_gear(self) -> '_2478.ConicalGear':
        """ConicalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2478.ConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to ConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_cylindrical_gear(self) -> '_2480.CylindricalGear':
        """CylindricalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2480.CylindricalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to CylindricalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_cylindrical_planet_gear(self) -> '_2482.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2482.CylindricalPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to CylindricalPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_face_gear(self) -> '_2483.FaceGear':
        """FaceGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2483.FaceGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to FaceGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_gear(self) -> '_2485.Gear':
        """Gear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2485.Gear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to Gear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_hypoid_gear(self) -> '_2489.HypoidGear':
        """HypoidGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2489.HypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to HypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2491.KlingelnbergCycloPalloidConicalGear':
        """KlingelnbergCycloPalloidConicalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2491.KlingelnbergCycloPalloidConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2493.KlingelnbergCycloPalloidHypoidGear':
        """KlingelnbergCycloPalloidHypoidGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2493.KlingelnbergCycloPalloidHypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2495.KlingelnbergCycloPalloidSpiralBevelGear':
        """KlingelnbergCycloPalloidSpiralBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2495.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_spiral_bevel_gear(self) -> '_2498.SpiralBevelGear':
        """SpiralBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2498.SpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to SpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_straight_bevel_diff_gear(self) -> '_2500.StraightBevelDiffGear':
        """StraightBevelDiffGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2500.StraightBevelDiffGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelDiffGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_straight_bevel_gear(self) -> '_2502.StraightBevelGear':
        """StraightBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2502.StraightBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_straight_bevel_planet_gear(self) -> '_2504.StraightBevelPlanetGear':
        """StraightBevelPlanetGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2504.StraightBevelPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_straight_bevel_sun_gear(self) -> '_2505.StraightBevelSunGear':
        """StraightBevelSunGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2505.StraightBevelSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_worm_gear(self) -> '_2506.WormGear':
        """WormGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2506.WormGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to WormGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_zerol_bevel_gear(self) -> '_2508.ZerolBevelGear':
        """ZerolBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2508.ZerolBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to ZerolBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_cycloidal_disc(self) -> '_2524.CycloidalDisc':
        """CycloidalDisc: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2524.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_ring_pins(self) -> '_2525.RingPins':
        """RingPins: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2525.RingPins.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to RingPins. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_clutch_half(self) -> '_2534.ClutchHalf':
        """ClutchHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2534.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_concept_coupling_half(self) -> '_2537.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2537.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_coupling_half(self) -> '_2539.CouplingHalf':
        """CouplingHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2539.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_cvt_pulley(self) -> '_2542.CVTPulley':
        """CVTPulley: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2542.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_part_to_part_shear_coupling_half(self) -> '_2544.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2544.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_pulley(self) -> '_2545.Pulley':
        """Pulley: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2545.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_rolling_ring(self) -> '_2551.RollingRing':
        """RollingRing: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2551.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_shaft_hub_connection(self) -> '_2553.ShaftHubConnection':
        """ShaftHubConnection: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2553.ShaftHubConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to ShaftHubConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_spring_damper_half(self) -> '_2556.SpringDamperHalf':
        """SpringDamperHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2556.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_synchroniser_half(self) -> '_2559.SynchroniserHalf':
        """SynchroniserHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2559.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_synchroniser_part(self) -> '_2560.SynchroniserPart':
        """SynchroniserPart: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2560.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_synchroniser_sleeve(self) -> '_2561.SynchroniserSleeve':
        """SynchroniserSleeve: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2561.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_torque_converter_pump(self) -> '_2563.TorqueConverterPump':
        """TorqueConverterPump: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2563.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_of_type_torque_converter_turbine(self) -> '_2565.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Owner

        if temp is None:
            return None

        if _2565.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def connect_to(self, component: '_2400.Component') -> '_2401.ComponentsConnectedResult':
        """ 'ConnectTo' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        """

        method_result = self.wrapped.ConnectTo.Overloads[_COMPONENT](component.wrapped if component else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def connect_to_socket(self, socket: 'Socket') -> '_2401.ComponentsConnectedResult':
        """ 'ConnectTo' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        """

        method_result = self.wrapped.ConnectTo.Overloads[_SOCKET](socket.wrapped if socket else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def connection_to(self, socket: 'Socket') -> '_2230.Connection':
        """ 'ConnectionTo' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.connections_and_sockets.Connection
        """

        method_result = self.wrapped.ConnectionTo(socket.wrapped if socket else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def get_possible_sockets_to_connect_to(self, component_to_connect_to: '_2400.Component') -> 'List[Socket]':
        """ 'GetPossibleSocketsToConnectTo' is the original name of this method.

        Args:
            component_to_connect_to (mastapy.system_model.part_model.Component)

        Returns:
            List[mastapy.system_model.connections_and_sockets.Socket]
        """

        return conversion.pn_to_mp_objects_in_list(self.wrapped.GetPossibleSocketsToConnectTo(component_to_connect_to.wrapped if component_to_connect_to else None))
