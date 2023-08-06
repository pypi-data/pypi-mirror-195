"""_6734.py

LoadCase
"""


from typing import List

from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_results.rolling import _1930, _1935, _2031
from mastapy.system_model import _2171, _2175, _2185
from mastapy.gears import _331
from mastapy.nodal_analysis.nodal_entities import _129
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _2071
from mastapy.system_model.analyses_and_results.static_loads import (
    _6741, _6869, _6908, _6902,
    _6738, _6737, _6739, _6750,
    _6762, _6761, _6767, _6780,
    _6799, _6813, _6817, _6818,
    _6749, _6826, _6851, _6852,
    _6854, _6856, _6858, _6865,
    _6868, _6878, _6882, _6910,
    _6911, _6880, _6771, _6773,
    _6814, _6816, _6744, _6746,
    _6753, _6755, _6756, _6757,
    _6758, _6760, _6774, _6778,
    _6791, _6795, _6796, _6820,
    _6825, _6835, _6837, _6842,
    _6844, _6845, _6847, _6848,
    _6850, _6863, _6883, _6885,
    _6889, _6891, _6892, _6894,
    _6895, _6896, _6912, _6914,
    _6915, _6917, _6787, _6789,
    _6873, _6861, _6860, _6752,
    _6765, _6764, _6770, _6769,
    _6783, _6782, _6785, _6786,
    _6870, _6879, _6877, _6875,
    _6888, _6887, _6898, _6897,
    _6899, _6900, _6903, _6904,
    _6905, _6881, _6784, _6751,
    _6766, _6779, _6841, _6862,
    _6876, _6740, _6754, _6772,
    _6815, _6890, _6759, _6776,
    _6745, _6793, _6836, _6843,
    _6846, _6849, _6884, _6893,
    _6913, _6916, _6822, _6788,
    _6790, _6874, _6859, _6763,
    _6768, _6781, _6886
)
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4335
from mastapy.system_model.connections_and_sockets.couplings import (
    _2310, _2306, _2300, _2302,
    _2304, _2308
)
from mastapy.system_model.part_model import (
    _2392, _2391, _2393, _2396,
    _2398, _2399, _2400, _2403,
    _2404, _2408, _2409, _2410,
    _2390, _2411, _2418, _2419,
    _2420, _2422, _2424, _2425,
    _2427, _2428, _2430, _2432,
    _2433, _2435
)
from mastapy.system_model.part_model.shaft_model import _2438
from mastapy.system_model.part_model.gears import (
    _2476, _2477, _2483, _2484,
    _2468, _2469, _2470, _2471,
    _2472, _2473, _2474, _2475,
    _2478, _2479, _2480, _2481,
    _2482, _2485, _2487, _2489,
    _2490, _2491, _2492, _2493,
    _2494, _2495, _2496, _2497,
    _2498, _2499, _2500, _2501,
    _2502, _2503, _2504, _2505,
    _2506, _2507, _2508, _2509
)
from mastapy.system_model.part_model.cycloidal import _2523, _2524, _2525
from mastapy.system_model.part_model.couplings import (
    _2543, _2544, _2531, _2533,
    _2534, _2536, _2537, _2538,
    _2539, _2541, _2542, _2545,
    _2553, _2551, _2552, _2555,
    _2556, _2557, _2559, _2560,
    _2561, _2562, _2563, _2565
)
from mastapy.system_model.connections_and_sockets import (
    _2253, _2231, _2226, _2227,
    _2230, _2239, _2245, _2250,
    _2223
)
from mastapy.system_model.connections_and_sockets.gears import (
    _2259, _2263, _2269, _2283,
    _2261, _2265, _2257, _2267,
    _2273, _2276, _2277, _2278,
    _2281, _2285, _2287, _2289,
    _2271
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2293, _2296, _2299
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.analyses_and_results import _2605

_TORQUE_CONVERTER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterConnection')
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'PartToPartShearCouplingConnection')
_CLUTCH_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ClutchConnection')
_CONCEPT_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ConceptCouplingConnection')
_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'CouplingConnection')
_SPRING_DAMPER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperConnection')
_ABSTRACT_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaft')
_ABSTRACT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractAssembly')
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaftOrHousing')
_BEARING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bearing')
_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')
_BOLTED_JOINT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BoltedJoint')
_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')
_DATUM = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Datum')
_EXTERNAL_CAD_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ExternalCADModel')
_FE_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FEPart')
_FLEXIBLE_PIN_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FlexiblePinAssembly')
_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')
_GUIDE_DXF_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'GuideDxfModel')
_MASS_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MassDisc')
_MEASUREMENT_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MeasurementComponent')
_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')
_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')
_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Part')
_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')
_POINT_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PointLoad')
_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')
_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')
_SPECIALISED_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'SpecialisedAssembly')
_UNBALANCED_MASS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'UnbalancedMass')
_VIRTUAL_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'VirtualComponent')
_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ShaftModel', 'Shaft')
_CONCEPT_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGear')
_CONCEPT_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGearSet')
_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')
_FACE_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGearSet')
_AGMA_GLEASON_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGear')
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGearSet')
_BEVEL_DIFFERENTIAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGear')
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialPlanetGear')
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialSunGear')
_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGear')
_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGearSet')
_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGear')
_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGearSet')
_CYLINDRICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGear')
_CYLINDRICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGearSet')
_CYLINDRICAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalPlanetGear')
_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'Gear')
_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearSet')
_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGear')
_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGear')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGearSet')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGear')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGear')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearSet')
_PLANETARY_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'PlanetaryGearSet')
_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGear')
_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGearSet')
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGear')
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGearSet')
_STRAIGHT_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGear')
_STRAIGHT_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGearSet')
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelPlanetGear')
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelSunGear')
_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')
_WORM_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGearSet')
_ZEROL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGear')
_ZEROL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGearSet')
_CYCLOIDAL_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalAssembly')
_CYCLOIDAL_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalDisc')
_RING_PINS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'RingPins')
_PART_TO_PART_SHEAR_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCoupling')
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCouplingHalf')
_BELT_DRIVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'BeltDrive')
_CLUTCH = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Clutch')
_CLUTCH_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ClutchHalf')
_CONCEPT_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCoupling')
_CONCEPT_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCouplingHalf')
_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Coupling')
_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CouplingHalf')
_CVT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVT')
_CVT_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVTPulley')
_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Pulley')
_SHAFT_HUB_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ShaftHubConnection')
_ROLLING_RING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRing')
_ROLLING_RING_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRingAssembly')
_SPRING_DAMPER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamper')
_SPRING_DAMPER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamperHalf')
_SYNCHRONISER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Synchroniser')
_SYNCHRONISER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserHalf')
_SYNCHRONISER_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserPart')
_SYNCHRONISER_SLEEVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserSleeve')
_TORQUE_CONVERTER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverter')
_TORQUE_CONVERTER_PUMP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterPump')
_TORQUE_CONVERTER_TURBINE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterTurbine')
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ShaftToMountableComponentConnection')
_CVT_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CVTBeltConnection')
_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BeltConnection')
_COAXIAL_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CoaxialConnection')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InterMountableComponentConnection')
_PLANETARY_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PlanetaryConnection')
_ROLLING_RING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'RollingRingConnection')
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'AbstractShaftToMountableComponentConnection')
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearMesh')
_CONCEPT_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConceptGearMesh')
_FACE_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'FaceGearMesh')
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelDiffGearMesh')
_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearMesh')
_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConicalGearMesh')
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'AGMAGleasonConicalGearMesh')
_CYLINDRICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'CylindricalGearMesh')
_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'HypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidConicalGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidHypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearMesh')
_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'SpiralBevelGearMesh')
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelGearMesh')
_WORM_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'WormGearMesh')
_ZEROL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ZerolBevelGearMesh')
_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscCentralBearingConnection')
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscPlanetaryBearingConnection')
_RING_PINS_TO_DISC_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'RingPinsToDiscConnection')
_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'LoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadCase',)


class LoadCase(_2605.Context):
    """LoadCase

    This is a mastapy class.
    """

    TYPE = _LOAD_CASE

    def __init__(self, instance_to_wrap: 'LoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def air_density(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'AirDensity' is the original name of this property."""

        temp = self.wrapped.AirDensity

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @air_density.setter
    def air_density(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.AirDensity = value

    @property
    def ball_bearing_contact_calculation(self) -> '_1930.BallBearingContactCalculation':
        """BallBearingContactCalculation: 'BallBearingContactCalculation' is the original name of this property."""

        temp = self.wrapped.BallBearingContactCalculation

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1930.BallBearingContactCalculation)(value) if value is not None else None

    @ball_bearing_contact_calculation.setter
    def ball_bearing_contact_calculation(self, value: '_1930.BallBearingContactCalculation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BallBearingContactCalculation = value

    @property
    def ball_bearing_friction_model_for_gyroscopic_moment(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment':
        """enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment: 'BallBearingFrictionModelForGyroscopicMoment' is the original name of this property."""

        temp = self.wrapped.BallBearingFrictionModelForGyroscopicMoment

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @ball_bearing_friction_model_for_gyroscopic_moment.setter
    def ball_bearing_friction_model_for_gyroscopic_moment(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.BallBearingFrictionModelForGyroscopicMoment = value

    @property
    def characteristic_specific_acoustic_impedance(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'CharacteristicSpecificAcousticImpedance' is the original name of this property."""

        temp = self.wrapped.CharacteristicSpecificAcousticImpedance

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @characteristic_specific_acoustic_impedance.setter
    def characteristic_specific_acoustic_impedance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.CharacteristicSpecificAcousticImpedance = value

    @property
    def energy_convergence_absolute_tolerance(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'EnergyConvergenceAbsoluteTolerance' is the original name of this property."""

        temp = self.wrapped.EnergyConvergenceAbsoluteTolerance

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @energy_convergence_absolute_tolerance.setter
    def energy_convergence_absolute_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.EnergyConvergenceAbsoluteTolerance = value

    @property
    def expand_grounded_nodes_for_thermal_effects(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'ExpandGroundedNodesForThermalEffects' is the original name of this property."""

        temp = self.wrapped.ExpandGroundedNodesForThermalEffects

        if temp is None:
            return False

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else False

    @expand_grounded_nodes_for_thermal_effects.setter
    def expand_grounded_nodes_for_thermal_effects(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.ExpandGroundedNodesForThermalEffects = value

    @property
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self) -> 'bool':
        """bool: 'ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes' is the original name of this property."""

        temp = self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes

        if temp is None:
            return False

        return temp

    @force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes.setter
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes = bool(value) if value else False

    @property
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        """float: 'GearMeshNodesPerUnitLengthToDiameterRatio' is the original name of this property."""

        temp = self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio

        if temp is None:
            return 0.0

        return temp

    @gear_mesh_nodes_per_unit_length_to_diameter_ratio.setter
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def grid_refinement_factor_contact_width(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'GridRefinementFactorContactWidth' is the original name of this property."""

        temp = self.wrapped.GridRefinementFactorContactWidth

        if temp is None:
            return 0

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else 0

    @grid_refinement_factor_contact_width.setter
    def grid_refinement_factor_contact_width(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.GridRefinementFactorContactWidth = value

    @property
    def grid_refinement_factor_rib_height(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'GridRefinementFactorRibHeight' is the original name of this property."""

        temp = self.wrapped.GridRefinementFactorRibHeight

        if temp is None:
            return 0

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else 0

    @grid_refinement_factor_rib_height.setter
    def grid_refinement_factor_rib_height(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.GridRefinementFactorRibHeight = value

    @property
    def hypoid_gear_wind_up_removal_method_for_misalignments(self) -> '_2171.HypoidWindUpRemovalMethod':
        """HypoidWindUpRemovalMethod: 'HypoidGearWindUpRemovalMethodForMisalignments' is the original name of this property."""

        temp = self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2171.HypoidWindUpRemovalMethod)(value) if value is not None else None

    @hypoid_gear_wind_up_removal_method_for_misalignments.setter
    def hypoid_gear_wind_up_removal_method_for_misalignments(self, value: '_2171.HypoidWindUpRemovalMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments = value

    @property
    def include_bearing_centrifugal_ring_expansion(self) -> 'bool':
        """bool: 'IncludeBearingCentrifugalRingExpansion' is the original name of this property."""

        temp = self.wrapped.IncludeBearingCentrifugalRingExpansion

        if temp is None:
            return False

        return temp

    @include_bearing_centrifugal_ring_expansion.setter
    def include_bearing_centrifugal_ring_expansion(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugalRingExpansion = bool(value) if value else False

    @property
    def include_bearing_centrifugal(self) -> 'bool':
        """bool: 'IncludeBearingCentrifugal' is the original name of this property."""

        temp = self.wrapped.IncludeBearingCentrifugal

        if temp is None:
            return False

        return temp

    @include_bearing_centrifugal.setter
    def include_bearing_centrifugal(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugal = bool(value) if value else False

    @property
    def include_fitting_effects(self) -> 'bool':
        """bool: 'IncludeFittingEffects' is the original name of this property."""

        temp = self.wrapped.IncludeFittingEffects

        if temp is None:
            return False

        return temp

    @include_fitting_effects.setter
    def include_fitting_effects(self, value: 'bool'):
        self.wrapped.IncludeFittingEffects = bool(value) if value else False

    @property
    def include_gear_blank_elastic_distortion(self) -> 'bool':
        """bool: 'IncludeGearBlankElasticDistortion' is the original name of this property."""

        temp = self.wrapped.IncludeGearBlankElasticDistortion

        if temp is None:
            return False

        return temp

    @include_gear_blank_elastic_distortion.setter
    def include_gear_blank_elastic_distortion(self, value: 'bool'):
        self.wrapped.IncludeGearBlankElasticDistortion = bool(value) if value else False

    @property
    def include_gravity(self) -> 'bool':
        """bool: 'IncludeGravity' is the original name of this property."""

        temp = self.wrapped.IncludeGravity

        if temp is None:
            return False

        return temp

    @include_gravity.setter
    def include_gravity(self, value: 'bool'):
        self.wrapped.IncludeGravity = bool(value) if value else False

    @property
    def include_inner_race_distortion_for_flexible_pin_spindle(self) -> 'bool':
        """bool: 'IncludeInnerRaceDistortionForFlexiblePinSpindle' is the original name of this property."""

        temp = self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle

        if temp is None:
            return False

        return temp

    @include_inner_race_distortion_for_flexible_pin_spindle.setter
    def include_inner_race_distortion_for_flexible_pin_spindle(self, value: 'bool'):
        self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle = bool(value) if value else False

    @property
    def include_planetary_centrifugal(self) -> 'bool':
        """bool: 'IncludePlanetaryCentrifugal' is the original name of this property."""

        temp = self.wrapped.IncludePlanetaryCentrifugal

        if temp is None:
            return False

        return temp

    @include_planetary_centrifugal.setter
    def include_planetary_centrifugal(self, value: 'bool'):
        self.wrapped.IncludePlanetaryCentrifugal = bool(value) if value else False

    @property
    def include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis(self) -> 'bool':
        """bool: 'IncludeProfileModificationsAndManufacturingErrorsDuringCycloidalAnalysis' is the original name of this property."""

        temp = self.wrapped.IncludeProfileModificationsAndManufacturingErrorsDuringCycloidalAnalysis

        if temp is None:
            return False

        return temp

    @include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis.setter
    def include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis(self, value: 'bool'):
        self.wrapped.IncludeProfileModificationsAndManufacturingErrorsDuringCycloidalAnalysis = bool(value) if value else False

    @property
    def include_rib_contact_analysis(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'IncludeRibContactAnalysis' is the original name of this property."""

        temp = self.wrapped.IncludeRibContactAnalysis

        if temp is None:
            return False

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else False

    @include_rib_contact_analysis.setter
    def include_rib_contact_analysis(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.IncludeRibContactAnalysis = value

    @property
    def include_ring_ovality(self) -> 'bool':
        """bool: 'IncludeRingOvality' is the original name of this property."""

        temp = self.wrapped.IncludeRingOvality

        if temp is None:
            return False

        return temp

    @include_ring_ovality.setter
    def include_ring_ovality(self, value: 'bool'):
        self.wrapped.IncludeRingOvality = bool(value) if value else False

    @property
    def include_thermal_expansion_effects(self) -> 'bool':
        """bool: 'IncludeThermalExpansionEffects' is the original name of this property."""

        temp = self.wrapped.IncludeThermalExpansionEffects

        if temp is None:
            return False

        return temp

    @include_thermal_expansion_effects.setter
    def include_thermal_expansion_effects(self, value: 'bool'):
        self.wrapped.IncludeThermalExpansionEffects = bool(value) if value else False

    @property
    def include_tilt_stiffness_for_bevel_hypoid_gears(self) -> 'bool':
        """bool: 'IncludeTiltStiffnessForBevelHypoidGears' is the original name of this property."""

        temp = self.wrapped.IncludeTiltStiffnessForBevelHypoidGears

        if temp is None:
            return False

        return temp

    @include_tilt_stiffness_for_bevel_hypoid_gears.setter
    def include_tilt_stiffness_for_bevel_hypoid_gears(self, value: 'bool'):
        self.wrapped.IncludeTiltStiffnessForBevelHypoidGears = bool(value) if value else False

    @property
    def maximum_shaft_section_cross_sectional_area_ratio(self) -> 'float':
        """float: 'MaximumShaftSectionCrossSectionalAreaRatio' is the original name of this property."""

        temp = self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio

        if temp is None:
            return 0.0

        return temp

    @maximum_shaft_section_cross_sectional_area_ratio.setter
    def maximum_shaft_section_cross_sectional_area_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_length_to_diameter_ratio(self) -> 'float':
        """float: 'MaximumShaftSectionLengthToDiameterRatio' is the original name of this property."""

        temp = self.wrapped.MaximumShaftSectionLengthToDiameterRatio

        if temp is None:
            return 0.0

        return temp

    @maximum_shaft_section_length_to_diameter_ratio.setter
    def maximum_shaft_section_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self) -> 'float':
        """float: 'MaximumShaftSectionPolarAreaMomentOfInertiaRatio' is the original name of this property."""

        temp = self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio

        if temp is None:
            return 0.0

        return temp

    @maximum_shaft_section_polar_area_moment_of_inertia_ratio.setter
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio = float(value) if value else 0.0

    @property
    def mesh_stiffness_model(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel':
        """enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel: 'MeshStiffnessModel' is the original name of this property."""

        temp = self.wrapped.MeshStiffnessModel

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @mesh_stiffness_model.setter
    def mesh_stiffness_model(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.MeshStiffnessModel = value

    @property
    def micro_geometry_model_in_system_deflection(self) -> 'overridable.Overridable_MicroGeometryModel':
        """overridable.Overridable_MicroGeometryModel: 'MicroGeometryModelInSystemDeflection' is the original name of this property."""

        temp = self.wrapped.MicroGeometryModelInSystemDeflection

        if temp is None:
            return None

        value = overridable.Overridable_MicroGeometryModel.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @micro_geometry_model_in_system_deflection.setter
    def micro_geometry_model_in_system_deflection(self, value: 'overridable.Overridable_MicroGeometryModel.implicit_type()'):
        wrapper_type = overridable.Overridable_MicroGeometryModel.wrapper_type()
        enclosed_type = overridable.Overridable_MicroGeometryModel.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.MicroGeometryModelInSystemDeflection = value

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumForceForBearingToBeConsideredLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumForceForBearingToBeConsideredLoaded

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    def minimum_force_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumForceForBearingToBeConsideredLoaded = value

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumMomentForBearingToBeConsideredLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumMomentForBearingToBeConsideredLoaded

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    def minimum_moment_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumMomentForBearingToBeConsideredLoaded = value

    @property
    def minimum_number_of_gear_mesh_nodes(self) -> 'int':
        """int: 'MinimumNumberOfGearMeshNodes' is the original name of this property."""

        temp = self.wrapped.MinimumNumberOfGearMeshNodes

        if temp is None:
            return 0

        return temp

    @minimum_number_of_gear_mesh_nodes.setter
    def minimum_number_of_gear_mesh_nodes(self, value: 'int'):
        self.wrapped.MinimumNumberOfGearMeshNodes = int(value) if value else 0

    @property
    def minimum_power_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumPowerForGearMeshToBeLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumPowerForGearMeshToBeLoaded

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @minimum_power_for_gear_mesh_to_be_loaded.setter
    def minimum_power_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumPowerForGearMeshToBeLoaded = value

    @property
    def minimum_torque_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumTorqueForGearMeshToBeLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumTorqueForGearMeshToBeLoaded

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @minimum_torque_for_gear_mesh_to_be_loaded.setter
    def minimum_torque_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumTorqueForGearMeshToBeLoaded = value

    @property
    def model_bearing_mounting_clearances_automatically(self) -> 'bool':
        """bool: 'ModelBearingMountingClearancesAutomatically' is the original name of this property."""

        temp = self.wrapped.ModelBearingMountingClearancesAutomatically

        if temp is None:
            return False

        return temp

    @model_bearing_mounting_clearances_automatically.setter
    def model_bearing_mounting_clearances_automatically(self, value: 'bool'):
        self.wrapped.ModelBearingMountingClearancesAutomatically = bool(value) if value else False

    @property
    def number_of_grid_points_across_rib_contact_width(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfGridPointsAcrossRibContactWidth' is the original name of this property."""

        temp = self.wrapped.NumberOfGridPointsAcrossRibContactWidth

        if temp is None:
            return 0

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else 0

    @number_of_grid_points_across_rib_contact_width.setter
    def number_of_grid_points_across_rib_contact_width(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfGridPointsAcrossRibContactWidth = value

    @property
    def number_of_grid_points_across_rib_height(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfGridPointsAcrossRibHeight' is the original name of this property."""

        temp = self.wrapped.NumberOfGridPointsAcrossRibHeight

        if temp is None:
            return 0

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else 0

    @number_of_grid_points_across_rib_height.setter
    def number_of_grid_points_across_rib_height(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfGridPointsAcrossRibHeight = value

    @property
    def number_of_strips_for_roller_calculation(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfStripsForRollerCalculation' is the original name of this property."""

        temp = self.wrapped.NumberOfStripsForRollerCalculation

        if temp is None:
            return 0

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else 0

    @number_of_strips_for_roller_calculation.setter
    def number_of_strips_for_roller_calculation(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfStripsForRollerCalculation = value

    @property
    def peak_load_factor_for_shafts(self) -> 'float':
        """float: 'PeakLoadFactorForShafts' is the original name of this property."""

        temp = self.wrapped.PeakLoadFactorForShafts

        if temp is None:
            return 0.0

        return temp

    @peak_load_factor_for_shafts.setter
    def peak_load_factor_for_shafts(self, value: 'float'):
        self.wrapped.PeakLoadFactorForShafts = float(value) if value else 0.0

    @property
    def refine_grid_around_contact_point(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'RefineGridAroundContactPoint' is the original name of this property."""

        temp = self.wrapped.RefineGridAroundContactPoint

        if temp is None:
            return False

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else False

    @refine_grid_around_contact_point.setter
    def refine_grid_around_contact_point(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.RefineGridAroundContactPoint = value

    @property
    def relative_tolerance_for_convergence(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RelativeToleranceForConvergence' is the original name of this property."""

        temp = self.wrapped.RelativeToleranceForConvergence

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @relative_tolerance_for_convergence.setter
    def relative_tolerance_for_convergence(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RelativeToleranceForConvergence = value

    @property
    def ring_ovality_scaling(self) -> 'float':
        """float: 'RingOvalityScaling' is the original name of this property."""

        temp = self.wrapped.RingOvalityScaling

        if temp is None:
            return 0.0

        return temp

    @ring_ovality_scaling.setter
    def ring_ovality_scaling(self, value: 'float'):
        self.wrapped.RingOvalityScaling = float(value) if value else 0.0

    @property
    def roller_analysis_method(self) -> '_2031.RollerAnalysisMethod':
        """RollerAnalysisMethod: 'RollerAnalysisMethod' is the original name of this property."""

        temp = self.wrapped.RollerAnalysisMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2031.RollerAnalysisMethod)(value) if value is not None else None

    @roller_analysis_method.setter
    def roller_analysis_method(self, value: '_2031.RollerAnalysisMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RollerAnalysisMethod = value

    @property
    def shear_area_factor_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ShearAreaFactorMethod':
        """enum_with_selected_value.EnumWithSelectedValue_ShearAreaFactorMethod: 'ShearAreaFactorMethod' is the original name of this property."""

        temp = self.wrapped.ShearAreaFactorMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ShearAreaFactorMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @shear_area_factor_method.setter
    def shear_area_factor_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ShearAreaFactorMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ShearAreaFactorMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ShearAreaFactorMethod = value

    @property
    def speed_of_sound(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SpeedOfSound' is the original name of this property."""

        temp = self.wrapped.SpeedOfSound

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @speed_of_sound.setter
    def speed_of_sound(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SpeedOfSound = value

    @property
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        """float: 'SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio' is the original name of this property."""

        temp = self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio

        if temp is None:
            return 0.0

        return temp

    @spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio.setter
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def stress_concentration_method_for_rating(self) -> 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod':
        """enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod: 'StressConcentrationMethodForRating' is the original name of this property."""

        temp = self.wrapped.StressConcentrationMethodForRating

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @stress_concentration_method_for_rating.setter
    def stress_concentration_method_for_rating(self, value: 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.StressConcentrationMethodForRating = value

    @property
    def tolerance_factor_for_axial_internal_clearances(self) -> 'float':
        """float: 'ToleranceFactorForAxialInternalClearances' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForAxialInternalClearances

        if temp is None:
            return 0.0

        return temp

    @tolerance_factor_for_axial_internal_clearances.setter
    def tolerance_factor_for_axial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForAxialInternalClearances = float(value) if value else 0.0

    @property
    def tolerance_factor_for_inner_fit(self) -> 'float':
        """float: 'ToleranceFactorForInnerFit' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForInnerFit

        if temp is None:
            return 0.0

        return temp

    @tolerance_factor_for_inner_fit.setter
    def tolerance_factor_for_inner_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForInnerFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_inner_mounting_sleeve_bore(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForInnerMountingSleeveBore' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForInnerMountingSleeveBore

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @tolerance_factor_for_inner_mounting_sleeve_bore.setter
    def tolerance_factor_for_inner_mounting_sleeve_bore(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerMountingSleeveBore = value

    @property
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForInnerMountingSleeveOuterDiameter' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @tolerance_factor_for_inner_mounting_sleeve_outer_diameter.setter
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter = value

    @property
    def tolerance_factor_for_inner_ring(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForInnerRing' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForInnerRing

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @tolerance_factor_for_inner_ring.setter
    def tolerance_factor_for_inner_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerRing = value

    @property
    def tolerance_factor_for_inner_support(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForInnerSupport' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForInnerSupport

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @tolerance_factor_for_inner_support.setter
    def tolerance_factor_for_inner_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerSupport = value

    @property
    def tolerance_factor_for_outer_fit(self) -> 'float':
        """float: 'ToleranceFactorForOuterFit' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForOuterFit

        if temp is None:
            return 0.0

        return temp

    @tolerance_factor_for_outer_fit.setter
    def tolerance_factor_for_outer_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForOuterFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_outer_mounting_sleeve_bore(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForOuterMountingSleeveBore' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForOuterMountingSleeveBore

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @tolerance_factor_for_outer_mounting_sleeve_bore.setter
    def tolerance_factor_for_outer_mounting_sleeve_bore(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterMountingSleeveBore = value

    @property
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForOuterMountingSleeveOuterDiameter' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @tolerance_factor_for_outer_mounting_sleeve_outer_diameter.setter
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter = value

    @property
    def tolerance_factor_for_outer_ring(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForOuterRing' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForOuterRing

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @tolerance_factor_for_outer_ring.setter
    def tolerance_factor_for_outer_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterRing = value

    @property
    def tolerance_factor_for_outer_support(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForOuterSupport' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForOuterSupport

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @tolerance_factor_for_outer_support.setter
    def tolerance_factor_for_outer_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterSupport = value

    @property
    def tolerance_factor_for_radial_internal_clearances(self) -> 'float':
        """float: 'ToleranceFactorForRadialInternalClearances' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForRadialInternalClearances

        if temp is None:
            return 0.0

        return temp

    @tolerance_factor_for_radial_internal_clearances.setter
    def tolerance_factor_for_radial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForRadialInternalClearances = float(value) if value else 0.0

    @property
    def use_default_temperatures(self) -> 'bool':
        """bool: 'UseDefaultTemperatures' is the original name of this property."""

        temp = self.wrapped.UseDefaultTemperatures

        if temp is None:
            return False

        return temp

    @use_default_temperatures.setter
    def use_default_temperatures(self, value: 'bool'):
        self.wrapped.UseDefaultTemperatures = bool(value) if value else False

    @property
    def use_node_per_bearing_row_inner(self) -> 'bool':
        """bool: 'UseNodePerBearingRowInner' is the original name of this property."""

        temp = self.wrapped.UseNodePerBearingRowInner

        if temp is None:
            return False

        return temp

    @use_node_per_bearing_row_inner.setter
    def use_node_per_bearing_row_inner(self, value: 'bool'):
        self.wrapped.UseNodePerBearingRowInner = bool(value) if value else False

    @property
    def use_node_per_bearing_row_outer(self) -> 'bool':
        """bool: 'UseNodePerBearingRowOuter' is the original name of this property."""

        temp = self.wrapped.UseNodePerBearingRowOuter

        if temp is None:
            return False

        return temp

    @use_node_per_bearing_row_outer.setter
    def use_node_per_bearing_row_outer(self, value: 'bool'):
        self.wrapped.UseNodePerBearingRowOuter = bool(value) if value else False

    @property
    def use_single_node_for_cylindrical_gear_meshes(self) -> 'bool':
        """bool: 'UseSingleNodeForCylindricalGearMeshes' is the original name of this property."""

        temp = self.wrapped.UseSingleNodeForCylindricalGearMeshes

        if temp is None:
            return False

        return temp

    @use_single_node_for_cylindrical_gear_meshes.setter
    def use_single_node_for_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.UseSingleNodeForCylindricalGearMeshes = bool(value) if value else False

    @property
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self) -> 'bool':
        """bool: 'UseSingleNodeForSplineRigidBondDetailedConnectionConnections' is the original name of this property."""

        temp = self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections

        if temp is None:
            return False

        return temp

    @use_single_node_for_spline_rigid_bond_detailed_connection_connections.setter
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self, value: 'bool'):
        self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections = bool(value) if value else False

    @property
    def additional_acceleration(self) -> '_6741.AdditionalAccelerationOptions':
        """AdditionalAccelerationOptions: 'AdditionalAcceleration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdditionalAcceleration

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def input_power_load(self) -> '_6869.PowerLoadLoadCase':
        """PowerLoadLoadCase: 'InputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InputPowerLoad

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def output_power_load(self) -> '_6869.PowerLoadLoadCase':
        """PowerLoadLoadCase: 'OutputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OutputPowerLoad

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def parametric_study_tool_options(self) -> '_4335.ParametricStudyToolOptions':
        """ParametricStudyToolOptions: 'ParametricStudyToolOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParametricStudyToolOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def temperatures(self) -> '_2185.TransmissionTemperatureSet':
        """TransmissionTemperatureSet: 'Temperatures' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Temperatures

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def transmission_efficiency_settings(self) -> '_6908.TransmissionEfficiencySettings':
        """TransmissionEfficiencySettings: 'TransmissionEfficiencySettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransmissionEfficiencySettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_loads(self) -> 'List[_6869.PowerLoadLoadCase]':
        """List[PowerLoadLoadCase]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def delete(self):
        """ 'Delete' is the original name of this method."""

        self.wrapped.Delete()

    def inputs_for_torque_converter_connection(self, design_entity: '_2310.TorqueConverterConnection') -> '_6902.TorqueConverterConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_abstract_shaft(self, design_entity: '_2392.AbstractShaft') -> '_6738.AbstractShaftLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_SHAFT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_abstract_assembly(self, design_entity: '_2391.AbstractAssembly') -> '_6737.AbstractAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_abstract_shaft_or_housing(self, design_entity: '_2393.AbstractShaftOrHousing') -> '_6739.AbstractShaftOrHousingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_SHAFT_OR_HOUSING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bearing(self, design_entity: '_2396.Bearing') -> '_6750.BearingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEARING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bolt(self, design_entity: '_2398.Bolt') -> '_6762.BoltLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BOLT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bolted_joint(self, design_entity: '_2399.BoltedJoint') -> '_6761.BoltedJointLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BOLTED_JOINT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_component(self, design_entity: '_2400.Component') -> '_6767.ComponentLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_COMPONENT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_connector(self, design_entity: '_2403.Connector') -> '_6780.ConnectorLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONNECTOR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_datum(self, design_entity: '_2404.Datum') -> '_6799.DatumLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_DATUM](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_external_cad_model(self, design_entity: '_2408.ExternalCADModel') -> '_6813.ExternalCADModelLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_EXTERNAL_CAD_MODEL](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_fe_part(self, design_entity: '_2409.FEPart') -> '_6817.FEPartLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_FE_PART](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_flexible_pin_assembly(self, design_entity: '_2410.FlexiblePinAssembly') -> '_6818.FlexiblePinAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_FLEXIBLE_PIN_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_assembly(self, design_entity: '_2390.Assembly') -> '_6749.AssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_guide_dxf_model(self, design_entity: '_2411.GuideDxfModel') -> '_6826.GuideDxfModelLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_GUIDE_DXF_MODEL](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_mass_disc(self, design_entity: '_2418.MassDisc') -> '_6851.MassDiscLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_MASS_DISC](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_measurement_component(self, design_entity: '_2419.MeasurementComponent') -> '_6852.MeasurementComponentLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_MEASUREMENT_COMPONENT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_mountable_component(self, design_entity: '_2420.MountableComponent') -> '_6854.MountableComponentLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_MOUNTABLE_COMPONENT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_oil_seal(self, design_entity: '_2422.OilSeal') -> '_6856.OilSealLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_OIL_SEAL](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_part(self, design_entity: '_2424.Part') -> '_6858.PartLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PART](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_planet_carrier(self, design_entity: '_2425.PlanetCarrier') -> '_6865.PlanetCarrierLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PLANET_CARRIER](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_point_load(self, design_entity: '_2427.PointLoad') -> '_6868.PointLoadLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_POINT_LOAD](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_power_load(self, design_entity: '_2428.PowerLoad') -> '_6869.PowerLoadLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_POWER_LOAD](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_root_assembly(self, design_entity: '_2430.RootAssembly') -> '_6878.RootAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ROOT_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_specialised_assembly(self, design_entity: '_2432.SpecialisedAssembly') -> '_6882.SpecialisedAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPECIALISED_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_unbalanced_mass(self, design_entity: '_2433.UnbalancedMass') -> '_6910.UnbalancedMassLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_UNBALANCED_MASS](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_virtual_component(self, design_entity: '_2435.VirtualComponent') -> '_6911.VirtualComponentLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_VIRTUAL_COMPONENT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_shaft(self, design_entity: '_2438.Shaft') -> '_6880.ShaftLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_gear(self, design_entity: '_2476.ConceptGear') -> '_6771.ConceptGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_gear_set(self, design_entity: '_2477.ConceptGearSet') -> '_6773.ConceptGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_face_gear(self, design_entity: '_2483.FaceGear') -> '_6814.FaceGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_face_gear_set(self, design_entity: '_2484.FaceGearSet') -> '_6816.FaceGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_agma_gleason_conical_gear(self, design_entity: '_2468.AGMAGleasonConicalGear') -> '_6744.AGMAGleasonConicalGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_agma_gleason_conical_gear_set(self, design_entity: '_2469.AGMAGleasonConicalGearSet') -> '_6746.AGMAGleasonConicalGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_gear(self, design_entity: '_2470.BevelDifferentialGear') -> '_6753.BevelDifferentialGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_gear_set(self, design_entity: '_2471.BevelDifferentialGearSet') -> '_6755.BevelDifferentialGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_planet_gear(self, design_entity: '_2472.BevelDifferentialPlanetGear') -> '_6756.BevelDifferentialPlanetGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_sun_gear(self, design_entity: '_2473.BevelDifferentialSunGear') -> '_6757.BevelDifferentialSunGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_SUN_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_gear(self, design_entity: '_2474.BevelGear') -> '_6758.BevelGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_gear_set(self, design_entity: '_2475.BevelGearSet') -> '_6760.BevelGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_conical_gear(self, design_entity: '_2478.ConicalGear') -> '_6774.ConicalGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_conical_gear_set(self, design_entity: '_2479.ConicalGearSet') -> '_6778.ConicalGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_gear(self, design_entity: '_2480.CylindricalGear') -> '_6791.CylindricalGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_gear_set(self, design_entity: '_2481.CylindricalGearSet') -> '_6795.CylindricalGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_planet_gear(self, design_entity: '_2482.CylindricalPlanetGear') -> '_6796.CylindricalPlanetGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_gear(self, design_entity: '_2485.Gear') -> '_6820.GearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_gear_set(self, design_entity: '_2487.GearSet') -> '_6825.GearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_hypoid_gear(self, design_entity: '_2489.HypoidGear') -> '_6835.HypoidGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_hypoid_gear_set(self, design_entity: '_2490.HypoidGearSet') -> '_6837.HypoidGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2491.KlingelnbergCycloPalloidConicalGear') -> '_6842.KlingelnbergCycloPalloidConicalGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2492.KlingelnbergCycloPalloidConicalGearSet') -> '_6844.KlingelnbergCycloPalloidConicalGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2493.KlingelnbergCycloPalloidHypoidGear') -> '_6845.KlingelnbergCycloPalloidHypoidGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2494.KlingelnbergCycloPalloidHypoidGearSet') -> '_6847.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2495.KlingelnbergCycloPalloidSpiralBevelGear') -> '_6848.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2496.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_6850.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_planetary_gear_set(self, design_entity: '_2497.PlanetaryGearSet') -> '_6863.PlanetaryGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PLANETARY_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spiral_bevel_gear(self, design_entity: '_2498.SpiralBevelGear') -> '_6883.SpiralBevelGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spiral_bevel_gear_set(self, design_entity: '_2499.SpiralBevelGearSet') -> '_6885.SpiralBevelGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_diff_gear(self, design_entity: '_2500.StraightBevelDiffGear') -> '_6889.StraightBevelDiffGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_diff_gear_set(self, design_entity: '_2501.StraightBevelDiffGearSet') -> '_6891.StraightBevelDiffGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_gear(self, design_entity: '_2502.StraightBevelGear') -> '_6892.StraightBevelGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_gear_set(self, design_entity: '_2503.StraightBevelGearSet') -> '_6894.StraightBevelGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_planet_gear(self, design_entity: '_2504.StraightBevelPlanetGear') -> '_6895.StraightBevelPlanetGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_sun_gear(self, design_entity: '_2505.StraightBevelSunGear') -> '_6896.StraightBevelSunGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_SUN_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_worm_gear(self, design_entity: '_2506.WormGear') -> '_6912.WormGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_worm_gear_set(self, design_entity: '_2507.WormGearSet') -> '_6914.WormGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_zerol_bevel_gear(self, design_entity: '_2508.ZerolBevelGear') -> '_6915.ZerolBevelGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_zerol_bevel_gear_set(self, design_entity: '_2509.ZerolBevelGearSet') -> '_6917.ZerolBevelGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_assembly(self, design_entity: '_2523.CycloidalAssembly') -> '_6787.CycloidalAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_disc(self, design_entity: '_2524.CycloidalDisc') -> '_6789.CycloidalDiscLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_DISC](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_ring_pins(self, design_entity: '_2525.RingPins') -> '_6873.RingPinsLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RingPinsLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_RING_PINS](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_part_to_part_shear_coupling(self, design_entity: '_2543.PartToPartShearCoupling') -> '_6861.PartToPartShearCouplingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_part_to_part_shear_coupling_half(self, design_entity: '_2544.PartToPartShearCouplingHalf') -> '_6860.PartToPartShearCouplingHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_belt_drive(self, design_entity: '_2531.BeltDrive') -> '_6752.BeltDriveLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BELT_DRIVE](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_clutch(self, design_entity: '_2533.Clutch') -> '_6765.ClutchLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_clutch_half(self, design_entity: '_2534.ClutchHalf') -> '_6764.ClutchHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_coupling(self, design_entity: '_2536.ConceptCoupling') -> '_6770.ConceptCouplingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_coupling_half(self, design_entity: '_2537.ConceptCouplingHalf') -> '_6769.ConceptCouplingHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_coupling(self, design_entity: '_2538.Coupling') -> '_6783.CouplingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_coupling_half(self, design_entity: '_2539.CouplingHalf') -> '_6782.CouplingHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cvt(self, design_entity: '_2541.CVT') -> '_6785.CVTLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CVT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cvt_pulley(self, design_entity: '_2542.CVTPulley') -> '_6786.CVTPulleyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CVT_PULLEY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_pulley(self, design_entity: '_2545.Pulley') -> '_6870.PulleyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PULLEY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_shaft_hub_connection(self, design_entity: '_2553.ShaftHubConnection') -> '_6879.ShaftHubConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT_HUB_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_rolling_ring(self, design_entity: '_2551.RollingRing') -> '_6877.RollingRingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_rolling_ring_assembly(self, design_entity: '_2552.RollingRingAssembly') -> '_6875.RollingRingAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spring_damper(self, design_entity: '_2555.SpringDamper') -> '_6888.SpringDamperLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spring_damper_half(self, design_entity: '_2556.SpringDamperHalf') -> '_6887.SpringDamperHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_synchroniser(self, design_entity: '_2557.Synchroniser') -> '_6898.SynchroniserLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_synchroniser_half(self, design_entity: '_2559.SynchroniserHalf') -> '_6897.SynchroniserHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_synchroniser_part(self, design_entity: '_2560.SynchroniserPart') -> '_6899.SynchroniserPartLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_PART](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_synchroniser_sleeve(self, design_entity: '_2561.SynchroniserSleeve') -> '_6900.SynchroniserSleeveLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_SLEEVE](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_torque_converter(self, design_entity: '_2562.TorqueConverter') -> '_6903.TorqueConverterLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_torque_converter_pump(self, design_entity: '_2563.TorqueConverterPump') -> '_6904.TorqueConverterPumpLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_PUMP](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_torque_converter_turbine(self, design_entity: '_2565.TorqueConverterTurbine') -> '_6905.TorqueConverterTurbineLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_TURBINE](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_shaft_to_mountable_component_connection(self, design_entity: '_2253.ShaftToMountableComponentConnection') -> '_6881.ShaftToMountableComponentConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cvt_belt_connection(self, design_entity: '_2231.CVTBeltConnection') -> '_6784.CVTBeltConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CVT_BELT_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_belt_connection(self, design_entity: '_2226.BeltConnection') -> '_6751.BeltConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BELT_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_coaxial_connection(self, design_entity: '_2227.CoaxialConnection') -> '_6766.CoaxialConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_COAXIAL_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_connection(self, design_entity: '_2230.Connection') -> '_6779.ConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_inter_mountable_component_connection(self, design_entity: '_2239.InterMountableComponentConnection') -> '_6841.InterMountableComponentConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_INTER_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_planetary_connection(self, design_entity: '_2245.PlanetaryConnection') -> '_6862.PlanetaryConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PLANETARY_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_rolling_ring_connection(self, design_entity: '_2250.RollingRingConnection') -> '_6876.RollingRingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_abstract_shaft_to_mountable_component_connection(self, design_entity: '_2223.AbstractShaftToMountableComponentConnection') -> '_6740.AbstractShaftToMountableComponentConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftToMountableComponentConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_gear_mesh(self, design_entity: '_2259.BevelDifferentialGearMesh') -> '_6754.BevelDifferentialGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_gear_mesh(self, design_entity: '_2263.ConceptGearMesh') -> '_6772.ConceptGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_face_gear_mesh(self, design_entity: '_2269.FaceGearMesh') -> '_6815.FaceGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_diff_gear_mesh(self, design_entity: '_2283.StraightBevelDiffGearMesh') -> '_6890.StraightBevelDiffGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_gear_mesh(self, design_entity: '_2261.BevelGearMesh') -> '_6759.BevelGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_conical_gear_mesh(self, design_entity: '_2265.ConicalGearMesh') -> '_6776.ConicalGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_agma_gleason_conical_gear_mesh(self, design_entity: '_2257.AGMAGleasonConicalGearMesh') -> '_6745.AGMAGleasonConicalGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_gear_mesh(self, design_entity: '_2267.CylindricalGearMesh') -> '_6793.CylindricalGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_hypoid_gear_mesh(self, design_entity: '_2273.HypoidGearMesh') -> '_6836.HypoidGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_2276.KlingelnbergCycloPalloidConicalGearMesh') -> '_6843.KlingelnbergCycloPalloidConicalGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_2277.KlingelnbergCycloPalloidHypoidGearMesh') -> '_6846.KlingelnbergCycloPalloidHypoidGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_2278.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_6849.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spiral_bevel_gear_mesh(self, design_entity: '_2281.SpiralBevelGearMesh') -> '_6884.SpiralBevelGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_gear_mesh(self, design_entity: '_2285.StraightBevelGearMesh') -> '_6893.StraightBevelGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_worm_gear_mesh(self, design_entity: '_2287.WormGearMesh') -> '_6913.WormGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_zerol_bevel_gear_mesh(self, design_entity: '_2289.ZerolBevelGearMesh') -> '_6916.ZerolBevelGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_gear_mesh(self, design_entity: '_2271.GearMesh') -> '_6822.GearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_disc_central_bearing_connection(self, design_entity: '_2293.CycloidalDiscCentralBearingConnection') -> '_6788.CycloidalDiscCentralBearingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscCentralBearingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_disc_planetary_bearing_connection(self, design_entity: '_2296.CycloidalDiscPlanetaryBearingConnection') -> '_6790.CycloidalDiscPlanetaryBearingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscPlanetaryBearingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_ring_pins_to_disc_connection(self, design_entity: '_2299.RingPinsToDiscConnection') -> '_6874.RingPinsToDiscConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RingPinsToDiscConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_RING_PINS_TO_DISC_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_part_to_part_shear_coupling_connection(self, design_entity: '_2306.PartToPartShearCouplingConnection') -> '_6859.PartToPartShearCouplingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_clutch_connection(self, design_entity: '_2300.ClutchConnection') -> '_6763.ClutchConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_coupling_connection(self, design_entity: '_2302.ConceptCouplingConnection') -> '_6768.ConceptCouplingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_coupling_connection(self, design_entity: '_2304.CouplingConnection') -> '_6781.CouplingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spring_damper_connection(self, design_entity: '_2308.SpringDamperConnection') -> '_6886.SpringDamperConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
