"""_1810.py

MASTAGUI
"""


from typing import List, Dict

from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy.system_model import _2161, _2164
from mastapy._math.color import Color
from mastapy.utility.operation_modes import _1757
from mastapy._math.vector_3d import Vector3D
from mastapy.system_model.connections_and_sockets import (
    _2223, _2226, _2227, _2230,
    _2231, _2239, _2245, _2250,
    _2253
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _2257, _2259, _2261, _2263,
    _2265, _2267, _2269, _2271,
    _2273, _2276, _2277, _2278,
    _2281, _2283, _2285, _2287,
    _2289
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2293, _2296, _2299
from mastapy.system_model.connections_and_sockets.couplings import (
    _2300, _2302, _2304, _2306,
    _2308, _2310
)
from mastapy.system_model.part_model import (
    _2390, _2391, _2392, _2393,
    _2396, _2398, _2399, _2400,
    _2403, _2404, _2408, _2409,
    _2410, _2411, _2418, _2419,
    _2420, _2422, _2424, _2425,
    _2427, _2428, _2430, _2432,
    _2433, _2435
)
from mastapy.system_model.part_model.shaft_model import _2438
from mastapy.system_model.part_model.gears import (
    _2468, _2469, _2470, _2471,
    _2472, _2473, _2474, _2475,
    _2476, _2477, _2478, _2479,
    _2480, _2481, _2482, _2483,
    _2484, _2485, _2487, _2489,
    _2490, _2491, _2492, _2493,
    _2494, _2495, _2496, _2497,
    _2498, _2499, _2500, _2501,
    _2502, _2503, _2504, _2505,
    _2506, _2507, _2508, _2509
)
from mastapy.system_model.part_model.cycloidal import _2523, _2524, _2525
from mastapy.system_model.part_model.couplings import (
    _2531, _2533, _2534, _2536,
    _2537, _2538, _2539, _2541,
    _2542, _2543, _2544, _2545,
    _2551, _2552, _2553, _2555,
    _2556, _2557, _2559, _2560,
    _2561, _2562, _2563, _2565
)
from mastapy.geometry.two_d import _305
from mastapy.nodal_analysis.geometry_modeller_link import (
    _154, _155, _161, _162
)
from mastapy.math_utility import _1476, _1459
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MASTAGUI = python_net_import('SMT.MastaAPI.SystemModelGUI', 'MASTAGUI')


__docformat__ = 'restructuredtext en'
__all__ = ('MASTAGUI',)


class MASTAGUI(_0.APIBase):
    """MASTAGUI

    This is a mastapy class.
    """

    TYPE = _MASTAGUI

    def __init__(self, instance_to_wrap: 'MASTAGUI.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_initialised(self) -> 'bool':
        """bool: 'IsInitialised' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsInitialised

        if temp is None:
            return False

        return temp

    @property
    def is_paused(self) -> 'bool':
        """bool: 'IsPaused' is the original name of this property."""

        temp = self.wrapped.IsPaused

        if temp is None:
            return False

        return temp

    @is_paused.setter
    def is_paused(self, value: 'bool'):
        self.wrapped.IsPaused = bool(value) if value else False

    @property
    def is_remoting(self) -> 'bool':
        """bool: 'IsRemoting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsRemoting

        if temp is None:
            return False

        return temp

    @property
    def active_design(self) -> '_2161.Design':
        """Design: 'ActiveDesign' is the original name of this property."""

        temp = self.wrapped.ActiveDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @active_design.setter
    def active_design(self, value: '_2161.Design'):
        value = value.wrapped if value else None
        self.wrapped.ActiveDesign = value

    @property
    def color_of_new_problem_node_group(self) -> 'Color':
        """Color: 'ColorOfNewProblemNodeGroup' is the original name of this property."""

        temp = self.wrapped.ColorOfNewProblemNodeGroup

        if temp is None:
            return None

        value = conversion.pn_to_mp_color(temp)
        return value

    @color_of_new_problem_node_group.setter
    def color_of_new_problem_node_group(self, value: 'Color'):
        value = value if value else None
        value = conversion.mp_to_pn_color(value)
        self.wrapped.ColorOfNewProblemNodeGroup = value

    @property
    def geometry_modeller_file_path_to_open(self) -> 'str':
        """str: 'GeometryModellerFilePathToOpen' is the original name of this property."""

        temp = self.wrapped.GeometryModellerFilePathToOpen

        if temp is None:
            return ''

        return temp

    @geometry_modeller_file_path_to_open.setter
    def geometry_modeller_file_path_to_open(self, value: 'str'):
        self.wrapped.GeometryModellerFilePathToOpen = str(value) if value else ''

    @property
    def geometry_modeller_process_id(self) -> 'int':
        """int: 'GeometryModellerProcessID' is the original name of this property."""

        temp = self.wrapped.GeometryModellerProcessID

        if temp is None:
            return 0

        return temp

    @geometry_modeller_process_id.setter
    def geometry_modeller_process_id(self, value: 'int'):
        self.wrapped.GeometryModellerProcessID = int(value) if value else 0

    @property
    def is_connected_to_geometry_modeller(self) -> 'bool':
        """bool: 'IsConnectedToGeometryModeller' is the original name of this property."""

        temp = self.wrapped.IsConnectedToGeometryModeller

        if temp is None:
            return False

        return temp

    @is_connected_to_geometry_modeller.setter
    def is_connected_to_geometry_modeller(self, value: 'bool'):
        self.wrapped.IsConnectedToGeometryModeller = bool(value) if value else False

    @property
    def name_of_new_problem_node_group(self) -> 'str':
        """str: 'NameOfNewProblemNodeGroup' is the original name of this property."""

        temp = self.wrapped.NameOfNewProblemNodeGroup

        if temp is None:
            return ''

        return temp

    @name_of_new_problem_node_group.setter
    def name_of_new_problem_node_group(self, value: 'str'):
        self.wrapped.NameOfNewProblemNodeGroup = str(value) if value else ''

    @property
    def open_designs(self) -> 'List[_2161.Design]':
        """List[Design]: 'OpenDesigns' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OpenDesigns

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def operation_mode(self) -> '_1757.OperationMode':
        """OperationMode: 'OperationMode' is the original name of this property."""

        temp = self.wrapped.OperationMode

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1757.OperationMode)(value) if value is not None else None

    @operation_mode.setter
    def operation_mode(self, value: '_1757.OperationMode'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OperationMode = value

    @property
    def positions_of_problem_node_group(self) -> 'List[Vector3D]':
        """List[Vector3D]: 'PositionsOfProblemNodeGroup' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PositionsOfProblemNodeGroup

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def process_id(self) -> 'int':
        """int: 'ProcessId' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProcessId

        if temp is None:
            return 0

        return temp

    @property
    def restart_geometry_modeller_flag(self) -> 'bool':
        """bool: 'RestartGeometryModellerFlag' is the original name of this property."""

        temp = self.wrapped.RestartGeometryModellerFlag

        if temp is None:
            return False

        return temp

    @restart_geometry_modeller_flag.setter
    def restart_geometry_modeller_flag(self, value: 'bool'):
        self.wrapped.RestartGeometryModellerFlag = bool(value) if value else False

    @property
    def restart_geometry_modeller_save_file(self) -> 'str':
        """str: 'RestartGeometryModellerSaveFile' is the original name of this property."""

        temp = self.wrapped.RestartGeometryModellerSaveFile

        if temp is None:
            return ''

        return temp

    @restart_geometry_modeller_save_file.setter
    def restart_geometry_modeller_save_file(self, value: 'str'):
        self.wrapped.RestartGeometryModellerSaveFile = str(value) if value else ''

    @property
    def selected_design_entity(self) -> '_2164.DesignEntity':
        """DesignEntity: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2164.DesignEntity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to DesignEntity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity.setter
    def selected_design_entity(self, value: '_2164.DesignEntity'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_2223.AbstractShaftToMountableComponentConnection':
        """AbstractShaftToMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2223.AbstractShaftToMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection.setter
    def selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection(self, value: '_2223.AbstractShaftToMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_belt_connection(self) -> '_2226.BeltConnection':
        """BeltConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2226.BeltConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BeltConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_belt_connection.setter
    def selected_design_entity_of_type_belt_connection(self, value: '_2226.BeltConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coaxial_connection(self) -> '_2227.CoaxialConnection':
        """CoaxialConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2227.CoaxialConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CoaxialConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_coaxial_connection.setter
    def selected_design_entity_of_type_coaxial_connection(self, value: '_2227.CoaxialConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_connection(self) -> '_2230.Connection':
        """Connection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2230.Connection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Connection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_connection.setter
    def selected_design_entity_of_type_connection(self, value: '_2230.Connection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt_belt_connection(self) -> '_2231.CVTBeltConnection':
        """CVTBeltConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2231.CVTBeltConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVTBeltConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cvt_belt_connection.setter
    def selected_design_entity_of_type_cvt_belt_connection(self, value: '_2231.CVTBeltConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_inter_mountable_component_connection(self) -> '_2239.InterMountableComponentConnection':
        """InterMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2239.InterMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to InterMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_inter_mountable_component_connection.setter
    def selected_design_entity_of_type_inter_mountable_component_connection(self, value: '_2239.InterMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planetary_connection(self) -> '_2245.PlanetaryConnection':
        """PlanetaryConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2245.PlanetaryConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetaryConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_planetary_connection.setter
    def selected_design_entity_of_type_planetary_connection(self, value: '_2245.PlanetaryConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring_connection(self) -> '_2250.RollingRingConnection':
        """RollingRingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2250.RollingRingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_rolling_ring_connection.setter
    def selected_design_entity_of_type_rolling_ring_connection(self, value: '_2250.RollingRingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft_to_mountable_component_connection(self) -> '_2253.ShaftToMountableComponentConnection':
        """ShaftToMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2253.ShaftToMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ShaftToMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_shaft_to_mountable_component_connection.setter
    def selected_design_entity_of_type_shaft_to_mountable_component_connection(self, value: '_2253.ShaftToMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear_mesh(self) -> '_2257.AGMAGleasonConicalGearMesh':
        """AGMAGleasonConicalGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2257.AGMAGleasonConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_agma_gleason_conical_gear_mesh.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear_mesh(self, value: '_2257.AGMAGleasonConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear_mesh(self) -> '_2259.BevelDifferentialGearMesh':
        """BevelDifferentialGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2259.BevelDifferentialGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_differential_gear_mesh.setter
    def selected_design_entity_of_type_bevel_differential_gear_mesh(self, value: '_2259.BevelDifferentialGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear_mesh(self) -> '_2261.BevelGearMesh':
        """BevelGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2261.BevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_gear_mesh.setter
    def selected_design_entity_of_type_bevel_gear_mesh(self, value: '_2261.BevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear_mesh(self) -> '_2263.ConceptGearMesh':
        """ConceptGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2263.ConceptGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_gear_mesh.setter
    def selected_design_entity_of_type_concept_gear_mesh(self, value: '_2263.ConceptGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear_mesh(self) -> '_2265.ConicalGearMesh':
        """ConicalGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2265.ConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_conical_gear_mesh.setter
    def selected_design_entity_of_type_conical_gear_mesh(self, value: '_2265.ConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear_mesh(self) -> '_2267.CylindricalGearMesh':
        """CylindricalGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2267.CylindricalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cylindrical_gear_mesh.setter
    def selected_design_entity_of_type_cylindrical_gear_mesh(self, value: '_2267.CylindricalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear_mesh(self) -> '_2269.FaceGearMesh':
        """FaceGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2269.FaceGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_face_gear_mesh.setter
    def selected_design_entity_of_type_face_gear_mesh(self, value: '_2269.FaceGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear_mesh(self) -> '_2271.GearMesh':
        """GearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2271.GearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_gear_mesh.setter
    def selected_design_entity_of_type_gear_mesh(self, value: '_2271.GearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear_mesh(self) -> '_2273.HypoidGearMesh':
        """HypoidGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2273.HypoidGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_hypoid_gear_mesh.setter
    def selected_design_entity_of_type_hypoid_gear_mesh(self, value: '_2273.HypoidGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_2276.KlingelnbergCycloPalloidConicalGearMesh':
        """KlingelnbergCycloPalloidConicalGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2276.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self, value: '_2276.KlingelnbergCycloPalloidConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2277.KlingelnbergCycloPalloidHypoidGearMesh':
        """KlingelnbergCycloPalloidHypoidGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2277.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, value: '_2277.KlingelnbergCycloPalloidHypoidGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2278.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        """KlingelnbergCycloPalloidSpiralBevelGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2278.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, value: '_2278.KlingelnbergCycloPalloidSpiralBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear_mesh(self) -> '_2281.SpiralBevelGearMesh':
        """SpiralBevelGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2281.SpiralBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spiral_bevel_gear_mesh.setter
    def selected_design_entity_of_type_spiral_bevel_gear_mesh(self, value: '_2281.SpiralBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear_mesh(self) -> '_2283.StraightBevelDiffGearMesh':
        """StraightBevelDiffGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2283.StraightBevelDiffGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_diff_gear_mesh.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear_mesh(self, value: '_2283.StraightBevelDiffGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear_mesh(self) -> '_2285.StraightBevelGearMesh':
        """StraightBevelGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2285.StraightBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_gear_mesh.setter
    def selected_design_entity_of_type_straight_bevel_gear_mesh(self, value: '_2285.StraightBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear_mesh(self) -> '_2287.WormGearMesh':
        """WormGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2287.WormGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_worm_gear_mesh.setter
    def selected_design_entity_of_type_worm_gear_mesh(self, value: '_2287.WormGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear_mesh(self) -> '_2289.ZerolBevelGearMesh':
        """ZerolBevelGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2289.ZerolBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_zerol_bevel_gear_mesh.setter
    def selected_design_entity_of_type_zerol_bevel_gear_mesh(self, value: '_2289.ZerolBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2293.CycloidalDiscCentralBearingConnection':
        """CycloidalDiscCentralBearingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2293.CycloidalDiscCentralBearingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cycloidal_disc_central_bearing_connection.setter
    def selected_design_entity_of_type_cycloidal_disc_central_bearing_connection(self, value: '_2293.CycloidalDiscCentralBearingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2296.CycloidalDiscPlanetaryBearingConnection':
        """CycloidalDiscPlanetaryBearingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2296.CycloidalDiscPlanetaryBearingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection.setter
    def selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection(self, value: '_2296.CycloidalDiscPlanetaryBearingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_ring_pins_to_disc_connection(self) -> '_2299.RingPinsToDiscConnection':
        """RingPinsToDiscConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2299.RingPinsToDiscConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RingPinsToDiscConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_ring_pins_to_disc_connection.setter
    def selected_design_entity_of_type_ring_pins_to_disc_connection(self, value: '_2299.RingPinsToDiscConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch_connection(self) -> '_2300.ClutchConnection':
        """ClutchConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2300.ClutchConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ClutchConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_clutch_connection.setter
    def selected_design_entity_of_type_clutch_connection(self, value: '_2300.ClutchConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling_connection(self) -> '_2302.ConceptCouplingConnection':
        """ConceptCouplingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2302.ConceptCouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_coupling_connection.setter
    def selected_design_entity_of_type_concept_coupling_connection(self, value: '_2302.ConceptCouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling_connection(self) -> '_2304.CouplingConnection':
        """CouplingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2304.CouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_coupling_connection.setter
    def selected_design_entity_of_type_coupling_connection(self, value: '_2304.CouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling_connection(self) -> '_2306.PartToPartShearCouplingConnection':
        """PartToPartShearCouplingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2306.PartToPartShearCouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_part_to_part_shear_coupling_connection.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling_connection(self, value: '_2306.PartToPartShearCouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper_connection(self) -> '_2308.SpringDamperConnection':
        """SpringDamperConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2308.SpringDamperConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamperConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spring_damper_connection.setter
    def selected_design_entity_of_type_spring_damper_connection(self, value: '_2308.SpringDamperConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_connection(self) -> '_2310.TorqueConverterConnection':
        """TorqueConverterConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2310.TorqueConverterConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_torque_converter_connection.setter
    def selected_design_entity_of_type_torque_converter_connection(self, value: '_2310.TorqueConverterConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_assembly(self) -> '_2390.Assembly':
        """Assembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2390.Assembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Assembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_assembly.setter
    def selected_design_entity_of_type_assembly(self, value: '_2390.Assembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_assembly(self) -> '_2391.AbstractAssembly':
        """AbstractAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2391.AbstractAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_abstract_assembly.setter
    def selected_design_entity_of_type_abstract_assembly(self, value: '_2391.AbstractAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft(self) -> '_2392.AbstractShaft':
        """AbstractShaft: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2392.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_abstract_shaft.setter
    def selected_design_entity_of_type_abstract_shaft(self, value: '_2392.AbstractShaft'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft_or_housing(self) -> '_2393.AbstractShaftOrHousing':
        """AbstractShaftOrHousing: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2393.AbstractShaftOrHousing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaftOrHousing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_abstract_shaft_or_housing.setter
    def selected_design_entity_of_type_abstract_shaft_or_housing(self, value: '_2393.AbstractShaftOrHousing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bearing(self) -> '_2396.Bearing':
        """Bearing: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2396.Bearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Bearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bearing.setter
    def selected_design_entity_of_type_bearing(self, value: '_2396.Bearing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bolt(self) -> '_2398.Bolt':
        """Bolt: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2398.Bolt.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Bolt. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bolt.setter
    def selected_design_entity_of_type_bolt(self, value: '_2398.Bolt'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bolted_joint(self) -> '_2399.BoltedJoint':
        """BoltedJoint: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2399.BoltedJoint.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BoltedJoint. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bolted_joint.setter
    def selected_design_entity_of_type_bolted_joint(self, value: '_2399.BoltedJoint'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_component(self) -> '_2400.Component':
        """Component: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2400.Component.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Component. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_component.setter
    def selected_design_entity_of_type_component(self, value: '_2400.Component'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_connector(self) -> '_2403.Connector':
        """Connector: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2403.Connector.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Connector. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_connector.setter
    def selected_design_entity_of_type_connector(self, value: '_2403.Connector'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_datum(self) -> '_2404.Datum':
        """Datum: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2404.Datum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Datum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_datum.setter
    def selected_design_entity_of_type_datum(self, value: '_2404.Datum'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_external_cad_model(self) -> '_2408.ExternalCADModel':
        """ExternalCADModel: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2408.ExternalCADModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ExternalCADModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_external_cad_model.setter
    def selected_design_entity_of_type_external_cad_model(self, value: '_2408.ExternalCADModel'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_fe_part(self) -> '_2409.FEPart':
        """FEPart: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2409.FEPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FEPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_fe_part.setter
    def selected_design_entity_of_type_fe_part(self, value: '_2409.FEPart'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_flexible_pin_assembly(self) -> '_2410.FlexiblePinAssembly':
        """FlexiblePinAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2410.FlexiblePinAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FlexiblePinAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_flexible_pin_assembly.setter
    def selected_design_entity_of_type_flexible_pin_assembly(self, value: '_2410.FlexiblePinAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_guide_dxf_model(self) -> '_2411.GuideDxfModel':
        """GuideDxfModel: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2411.GuideDxfModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GuideDxfModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_guide_dxf_model.setter
    def selected_design_entity_of_type_guide_dxf_model(self, value: '_2411.GuideDxfModel'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_mass_disc(self) -> '_2418.MassDisc':
        """MassDisc: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2418.MassDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MassDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_mass_disc.setter
    def selected_design_entity_of_type_mass_disc(self, value: '_2418.MassDisc'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_measurement_component(self) -> '_2419.MeasurementComponent':
        """MeasurementComponent: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2419.MeasurementComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MeasurementComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_measurement_component.setter
    def selected_design_entity_of_type_measurement_component(self, value: '_2419.MeasurementComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_mountable_component(self) -> '_2420.MountableComponent':
        """MountableComponent: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2420.MountableComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MountableComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_mountable_component.setter
    def selected_design_entity_of_type_mountable_component(self, value: '_2420.MountableComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_oil_seal(self) -> '_2422.OilSeal':
        """OilSeal: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2422.OilSeal.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to OilSeal. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_oil_seal.setter
    def selected_design_entity_of_type_oil_seal(self, value: '_2422.OilSeal'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part(self) -> '_2424.Part':
        """Part: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2424.Part.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Part. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_part.setter
    def selected_design_entity_of_type_part(self, value: '_2424.Part'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planet_carrier(self) -> '_2425.PlanetCarrier':
        """PlanetCarrier: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2425.PlanetCarrier.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetCarrier. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_planet_carrier.setter
    def selected_design_entity_of_type_planet_carrier(self, value: '_2425.PlanetCarrier'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_point_load(self) -> '_2427.PointLoad':
        """PointLoad: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2427.PointLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PointLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_point_load.setter
    def selected_design_entity_of_type_point_load(self, value: '_2427.PointLoad'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_power_load(self) -> '_2428.PowerLoad':
        """PowerLoad: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2428.PowerLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PowerLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_power_load.setter
    def selected_design_entity_of_type_power_load(self, value: '_2428.PowerLoad'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_root_assembly(self) -> '_2430.RootAssembly':
        """RootAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2430.RootAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RootAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_root_assembly.setter
    def selected_design_entity_of_type_root_assembly(self, value: '_2430.RootAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_specialised_assembly(self) -> '_2432.SpecialisedAssembly':
        """SpecialisedAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2432.SpecialisedAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpecialisedAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_specialised_assembly.setter
    def selected_design_entity_of_type_specialised_assembly(self, value: '_2432.SpecialisedAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_unbalanced_mass(self) -> '_2433.UnbalancedMass':
        """UnbalancedMass: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2433.UnbalancedMass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to UnbalancedMass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_unbalanced_mass.setter
    def selected_design_entity_of_type_unbalanced_mass(self, value: '_2433.UnbalancedMass'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_virtual_component(self) -> '_2435.VirtualComponent':
        """VirtualComponent: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2435.VirtualComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to VirtualComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_virtual_component.setter
    def selected_design_entity_of_type_virtual_component(self, value: '_2435.VirtualComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft(self) -> '_2438.Shaft':
        """Shaft: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2438.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_shaft.setter
    def selected_design_entity_of_type_shaft(self, value: '_2438.Shaft'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear(self) -> '_2468.AGMAGleasonConicalGear':
        """AGMAGleasonConicalGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2468.AGMAGleasonConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_agma_gleason_conical_gear.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear(self, value: '_2468.AGMAGleasonConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear_set(self) -> '_2469.AGMAGleasonConicalGearSet':
        """AGMAGleasonConicalGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2469.AGMAGleasonConicalGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_agma_gleason_conical_gear_set.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear_set(self, value: '_2469.AGMAGleasonConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear(self) -> '_2470.BevelDifferentialGear':
        """BevelDifferentialGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2470.BevelDifferentialGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_differential_gear.setter
    def selected_design_entity_of_type_bevel_differential_gear(self, value: '_2470.BevelDifferentialGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear_set(self) -> '_2471.BevelDifferentialGearSet':
        """BevelDifferentialGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2471.BevelDifferentialGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_differential_gear_set.setter
    def selected_design_entity_of_type_bevel_differential_gear_set(self, value: '_2471.BevelDifferentialGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_planet_gear(self) -> '_2472.BevelDifferentialPlanetGear':
        """BevelDifferentialPlanetGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2472.BevelDifferentialPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_differential_planet_gear.setter
    def selected_design_entity_of_type_bevel_differential_planet_gear(self, value: '_2472.BevelDifferentialPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_sun_gear(self) -> '_2473.BevelDifferentialSunGear':
        """BevelDifferentialSunGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2473.BevelDifferentialSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_differential_sun_gear.setter
    def selected_design_entity_of_type_bevel_differential_sun_gear(self, value: '_2473.BevelDifferentialSunGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear(self) -> '_2474.BevelGear':
        """BevelGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2474.BevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_gear.setter
    def selected_design_entity_of_type_bevel_gear(self, value: '_2474.BevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear_set(self) -> '_2475.BevelGearSet':
        """BevelGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2475.BevelGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_gear_set.setter
    def selected_design_entity_of_type_bevel_gear_set(self, value: '_2475.BevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear(self) -> '_2476.ConceptGear':
        """ConceptGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2476.ConceptGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_gear.setter
    def selected_design_entity_of_type_concept_gear(self, value: '_2476.ConceptGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear_set(self) -> '_2477.ConceptGearSet':
        """ConceptGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2477.ConceptGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_gear_set.setter
    def selected_design_entity_of_type_concept_gear_set(self, value: '_2477.ConceptGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear(self) -> '_2478.ConicalGear':
        """ConicalGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2478.ConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_conical_gear.setter
    def selected_design_entity_of_type_conical_gear(self, value: '_2478.ConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear_set(self) -> '_2479.ConicalGearSet':
        """ConicalGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2479.ConicalGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_conical_gear_set.setter
    def selected_design_entity_of_type_conical_gear_set(self, value: '_2479.ConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear(self) -> '_2480.CylindricalGear':
        """CylindricalGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2480.CylindricalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cylindrical_gear.setter
    def selected_design_entity_of_type_cylindrical_gear(self, value: '_2480.CylindricalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear_set(self) -> '_2481.CylindricalGearSet':
        """CylindricalGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2481.CylindricalGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cylindrical_gear_set.setter
    def selected_design_entity_of_type_cylindrical_gear_set(self, value: '_2481.CylindricalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_planet_gear(self) -> '_2482.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2482.CylindricalPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cylindrical_planet_gear.setter
    def selected_design_entity_of_type_cylindrical_planet_gear(self, value: '_2482.CylindricalPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear(self) -> '_2483.FaceGear':
        """FaceGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2483.FaceGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_face_gear.setter
    def selected_design_entity_of_type_face_gear(self, value: '_2483.FaceGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear_set(self) -> '_2484.FaceGearSet':
        """FaceGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2484.FaceGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_face_gear_set.setter
    def selected_design_entity_of_type_face_gear_set(self, value: '_2484.FaceGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear(self) -> '_2485.Gear':
        """Gear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2485.Gear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Gear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_gear.setter
    def selected_design_entity_of_type_gear(self, value: '_2485.Gear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear_set(self) -> '_2487.GearSet':
        """GearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2487.GearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_gear_set.setter
    def selected_design_entity_of_type_gear_set(self, value: '_2487.GearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear(self) -> '_2489.HypoidGear':
        """HypoidGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2489.HypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_hypoid_gear.setter
    def selected_design_entity_of_type_hypoid_gear(self, value: '_2489.HypoidGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear_set(self) -> '_2490.HypoidGearSet':
        """HypoidGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2490.HypoidGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_hypoid_gear_set.setter
    def selected_design_entity_of_type_hypoid_gear_set(self, value: '_2490.HypoidGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2491.KlingelnbergCycloPalloidConicalGear':
        """KlingelnbergCycloPalloidConicalGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2491.KlingelnbergCycloPalloidConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear(self, value: '_2491.KlingelnbergCycloPalloidConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2492.KlingelnbergCycloPalloidConicalGearSet':
        """KlingelnbergCycloPalloidConicalGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2492.KlingelnbergCycloPalloidConicalGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self, value: '_2492.KlingelnbergCycloPalloidConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2493.KlingelnbergCycloPalloidHypoidGear':
        """KlingelnbergCycloPalloidHypoidGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2493.KlingelnbergCycloPalloidHypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self, value: '_2493.KlingelnbergCycloPalloidHypoidGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2494.KlingelnbergCycloPalloidHypoidGearSet':
        """KlingelnbergCycloPalloidHypoidGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2494.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self, value: '_2494.KlingelnbergCycloPalloidHypoidGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2495.KlingelnbergCycloPalloidSpiralBevelGear':
        """KlingelnbergCycloPalloidSpiralBevelGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2495.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, value: '_2495.KlingelnbergCycloPalloidSpiralBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2496.KlingelnbergCycloPalloidSpiralBevelGearSet':
        """KlingelnbergCycloPalloidSpiralBevelGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2496.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, value: '_2496.KlingelnbergCycloPalloidSpiralBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planetary_gear_set(self) -> '_2497.PlanetaryGearSet':
        """PlanetaryGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2497.PlanetaryGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetaryGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_planetary_gear_set.setter
    def selected_design_entity_of_type_planetary_gear_set(self, value: '_2497.PlanetaryGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear(self) -> '_2498.SpiralBevelGear':
        """SpiralBevelGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2498.SpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spiral_bevel_gear.setter
    def selected_design_entity_of_type_spiral_bevel_gear(self, value: '_2498.SpiralBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear_set(self) -> '_2499.SpiralBevelGearSet':
        """SpiralBevelGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2499.SpiralBevelGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spiral_bevel_gear_set.setter
    def selected_design_entity_of_type_spiral_bevel_gear_set(self, value: '_2499.SpiralBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear(self) -> '_2500.StraightBevelDiffGear':
        """StraightBevelDiffGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2500.StraightBevelDiffGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_diff_gear.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear(self, value: '_2500.StraightBevelDiffGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear_set(self) -> '_2501.StraightBevelDiffGearSet':
        """StraightBevelDiffGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2501.StraightBevelDiffGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_diff_gear_set.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear_set(self, value: '_2501.StraightBevelDiffGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear(self) -> '_2502.StraightBevelGear':
        """StraightBevelGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2502.StraightBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_gear.setter
    def selected_design_entity_of_type_straight_bevel_gear(self, value: '_2502.StraightBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear_set(self) -> '_2503.StraightBevelGearSet':
        """StraightBevelGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2503.StraightBevelGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_gear_set.setter
    def selected_design_entity_of_type_straight_bevel_gear_set(self, value: '_2503.StraightBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_planet_gear(self) -> '_2504.StraightBevelPlanetGear':
        """StraightBevelPlanetGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2504.StraightBevelPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_planet_gear.setter
    def selected_design_entity_of_type_straight_bevel_planet_gear(self, value: '_2504.StraightBevelPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_sun_gear(self) -> '_2505.StraightBevelSunGear':
        """StraightBevelSunGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2505.StraightBevelSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_sun_gear.setter
    def selected_design_entity_of_type_straight_bevel_sun_gear(self, value: '_2505.StraightBevelSunGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear(self) -> '_2506.WormGear':
        """WormGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2506.WormGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_worm_gear.setter
    def selected_design_entity_of_type_worm_gear(self, value: '_2506.WormGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear_set(self) -> '_2507.WormGearSet':
        """WormGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2507.WormGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_worm_gear_set.setter
    def selected_design_entity_of_type_worm_gear_set(self, value: '_2507.WormGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear(self) -> '_2508.ZerolBevelGear':
        """ZerolBevelGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2508.ZerolBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_zerol_bevel_gear.setter
    def selected_design_entity_of_type_zerol_bevel_gear(self, value: '_2508.ZerolBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear_set(self) -> '_2509.ZerolBevelGearSet':
        """ZerolBevelGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2509.ZerolBevelGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_zerol_bevel_gear_set.setter
    def selected_design_entity_of_type_zerol_bevel_gear_set(self, value: '_2509.ZerolBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_assembly(self) -> '_2523.CycloidalAssembly':
        """CycloidalAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2523.CycloidalAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cycloidal_assembly.setter
    def selected_design_entity_of_type_cycloidal_assembly(self, value: '_2523.CycloidalAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc(self) -> '_2524.CycloidalDisc':
        """CycloidalDisc: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2524.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cycloidal_disc.setter
    def selected_design_entity_of_type_cycloidal_disc(self, value: '_2524.CycloidalDisc'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_ring_pins(self) -> '_2525.RingPins':
        """RingPins: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2525.RingPins.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RingPins. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_ring_pins.setter
    def selected_design_entity_of_type_ring_pins(self, value: '_2525.RingPins'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_belt_drive(self) -> '_2531.BeltDrive':
        """BeltDrive: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2531.BeltDrive.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BeltDrive. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_belt_drive.setter
    def selected_design_entity_of_type_belt_drive(self, value: '_2531.BeltDrive'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch(self) -> '_2533.Clutch':
        """Clutch: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2533.Clutch.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Clutch. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_clutch.setter
    def selected_design_entity_of_type_clutch(self, value: '_2533.Clutch'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch_half(self) -> '_2534.ClutchHalf':
        """ClutchHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2534.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_clutch_half.setter
    def selected_design_entity_of_type_clutch_half(self, value: '_2534.ClutchHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling(self) -> '_2536.ConceptCoupling':
        """ConceptCoupling: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2536.ConceptCoupling.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCoupling. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_coupling.setter
    def selected_design_entity_of_type_concept_coupling(self, value: '_2536.ConceptCoupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling_half(self) -> '_2537.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2537.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_coupling_half.setter
    def selected_design_entity_of_type_concept_coupling_half(self, value: '_2537.ConceptCouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling(self) -> '_2538.Coupling':
        """Coupling: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2538.Coupling.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Coupling. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_coupling.setter
    def selected_design_entity_of_type_coupling(self, value: '_2538.Coupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling_half(self) -> '_2539.CouplingHalf':
        """CouplingHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2539.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_coupling_half.setter
    def selected_design_entity_of_type_coupling_half(self, value: '_2539.CouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt(self) -> '_2541.CVT':
        """CVT: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2541.CVT.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVT. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cvt.setter
    def selected_design_entity_of_type_cvt(self, value: '_2541.CVT'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt_pulley(self) -> '_2542.CVTPulley':
        """CVTPulley: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2542.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cvt_pulley.setter
    def selected_design_entity_of_type_cvt_pulley(self, value: '_2542.CVTPulley'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling(self) -> '_2543.PartToPartShearCoupling':
        """PartToPartShearCoupling: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2543.PartToPartShearCoupling.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCoupling. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_part_to_part_shear_coupling.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling(self, value: '_2543.PartToPartShearCoupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling_half(self) -> '_2544.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2544.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_part_to_part_shear_coupling_half.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling_half(self, value: '_2544.PartToPartShearCouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_pulley(self) -> '_2545.Pulley':
        """Pulley: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2545.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_pulley.setter
    def selected_design_entity_of_type_pulley(self, value: '_2545.Pulley'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring(self) -> '_2551.RollingRing':
        """RollingRing: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2551.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_rolling_ring.setter
    def selected_design_entity_of_type_rolling_ring(self, value: '_2551.RollingRing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring_assembly(self) -> '_2552.RollingRingAssembly':
        """RollingRingAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2552.RollingRingAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRingAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_rolling_ring_assembly.setter
    def selected_design_entity_of_type_rolling_ring_assembly(self, value: '_2552.RollingRingAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft_hub_connection(self) -> '_2553.ShaftHubConnection':
        """ShaftHubConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2553.ShaftHubConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ShaftHubConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_shaft_hub_connection.setter
    def selected_design_entity_of_type_shaft_hub_connection(self, value: '_2553.ShaftHubConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper(self) -> '_2555.SpringDamper':
        """SpringDamper: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2555.SpringDamper.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamper. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spring_damper.setter
    def selected_design_entity_of_type_spring_damper(self, value: '_2555.SpringDamper'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper_half(self) -> '_2556.SpringDamperHalf':
        """SpringDamperHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2556.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spring_damper_half.setter
    def selected_design_entity_of_type_spring_damper_half(self, value: '_2556.SpringDamperHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser(self) -> '_2557.Synchroniser':
        """Synchroniser: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2557.Synchroniser.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Synchroniser. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_synchroniser.setter
    def selected_design_entity_of_type_synchroniser(self, value: '_2557.Synchroniser'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_half(self) -> '_2559.SynchroniserHalf':
        """SynchroniserHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2559.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_synchroniser_half.setter
    def selected_design_entity_of_type_synchroniser_half(self, value: '_2559.SynchroniserHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_part(self) -> '_2560.SynchroniserPart':
        """SynchroniserPart: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2560.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_synchroniser_part.setter
    def selected_design_entity_of_type_synchroniser_part(self, value: '_2560.SynchroniserPart'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_sleeve(self) -> '_2561.SynchroniserSleeve':
        """SynchroniserSleeve: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2561.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_synchroniser_sleeve.setter
    def selected_design_entity_of_type_synchroniser_sleeve(self, value: '_2561.SynchroniserSleeve'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter(self) -> '_2562.TorqueConverter':
        """TorqueConverter: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2562.TorqueConverter.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverter. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_torque_converter.setter
    def selected_design_entity_of_type_torque_converter(self, value: '_2562.TorqueConverter'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_pump(self) -> '_2563.TorqueConverterPump':
        """TorqueConverterPump: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2563.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_torque_converter_pump.setter
    def selected_design_entity_of_type_torque_converter_pump(self, value: '_2563.TorqueConverterPump'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_turbine(self) -> '_2565.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2565.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_torque_converter_turbine.setter
    def selected_design_entity_of_type_torque_converter_turbine(self, value: '_2565.TorqueConverterTurbine'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def report_names(self) -> 'List[str]':
        """List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    @staticmethod
    def get_mastagui(process_id: 'int') -> 'MASTAGUI':
        """ 'GetMASTAGUI' is the original name of this method.

        Args:
            process_id (int)

        Returns:
            mastapy.system_model_gui.MASTAGUI
        """

        process_id = int(process_id)
        method_result = MASTAGUI.TYPE.GetMASTAGUI(process_id if process_id else 0)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def pause(self):
        """ 'Pause' is the original name of this method."""

        self.wrapped.Pause()

    def resume(self):
        """ 'Resume' is the original name of this method."""

        self.wrapped.Resume()

    def start_remoting(self):
        """ 'StartRemoting' is the original name of this method."""

        self.wrapped.StartRemoting()

    def stop_remoting(self):
        """ 'StopRemoting' is the original name of this method."""

        self.wrapped.StopRemoting()

    def aborted(self):
        """ 'Aborted' is the original name of this method."""

        self.wrapped.Aborted()

    def add_electric_machine_from_cad_face_group(self, cad_face_group: '_305.CADFaceGroup', geometry_modeller_design_information: '_154.GeometryModellerDesignInformation', dimensions: 'Dict[str, _155.GeometryModellerDimension]'):
        """ 'AddElectricMachineFromCADFaceGroup' is the original name of this method.

        Args:
            cad_face_group (mastapy.geometry.two_d.CADFaceGroup)
            geometry_modeller_design_information (mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
        """

        self.wrapped.AddElectricMachineFromCADFaceGroup(cad_face_group.wrapped if cad_face_group else None, geometry_modeller_design_information.wrapped if geometry_modeller_design_information else None, dimensions)

    def add_fe_substructure_from_data(self, vertices_and_facets: '_1476.FacetedBody', geometry_modeller_design_information: '_154.GeometryModellerDesignInformation', dimensions: 'Dict[str, _155.GeometryModellerDimension]', body_moniker: 'str'):
        """ 'AddFESubstructureFromData' is the original name of this method.

        Args:
            vertices_and_facets (mastapy.math_utility.FacetedBody)
            geometry_modeller_design_information (mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
            body_moniker (str)
        """

        body_moniker = str(body_moniker)
        self.wrapped.AddFESubstructureFromData(vertices_and_facets.wrapped if vertices_and_facets else None, geometry_modeller_design_information.wrapped if geometry_modeller_design_information else None, dimensions, body_moniker if body_moniker else '')

    def add_fe_substructure_from_file(self, length_scale: 'float', stl_file_name: 'str', dimensions: 'Dict[str, _155.GeometryModellerDimension]'):
        """ 'AddFESubstructureFromFile' is the original name of this method.

        Args:
            length_scale (float)
            stl_file_name (str)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
        """

        length_scale = float(length_scale)
        stl_file_name = str(stl_file_name)
        self.wrapped.AddFESubstructureFromFile(length_scale if length_scale else 0.0, stl_file_name if stl_file_name else '', dimensions)

    def add_line_from_geometry_modeller(self, circles_on_axis: '_1459.CirclesOnAxis'):
        """ 'AddLineFromGeometryModeller' is the original name of this method.

        Args:
            circles_on_axis (mastapy.math_utility.CirclesOnAxis)
        """

        self.wrapped.AddLineFromGeometryModeller(circles_on_axis.wrapped if circles_on_axis else None)

    def are_new_input_available(self) -> '_161.MeshRequest':
        """ 'AreNewInputAvailable' is the original name of this method.

        Returns:
            mastapy.nodal_analysis.geometry_modeller_link.MeshRequest
        """

        method_result = self.wrapped.AreNewInputAvailable()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def circle_pairs_from_geometry_modeller(self, preselection_circles: '_1459.CirclesOnAxis', selected_circles: 'List[_1459.CirclesOnAxis]'):
        """ 'CirclePairsFromGeometryModeller' is the original name of this method.

        Args:
            preselection_circles (mastapy.math_utility.CirclesOnAxis)
            selected_circles (List[mastapy.math_utility.CirclesOnAxis])
        """

        selected_circles = conversion.mp_to_pn_objects_in_list(selected_circles)
        self.wrapped.CirclePairsFromGeometryModeller(preselection_circles.wrapped if preselection_circles else None, selected_circles)

    def create_geometry_modeller_design_information(self, file_name: 'str', main_part_moniker: 'str', tab_name: 'str') -> '_154.GeometryModellerDesignInformation':
        """ 'CreateGeometryModellerDesignInformation' is the original name of this method.

        Args:
            file_name (str)
            main_part_moniker (str)
            tab_name (str)

        Returns:
            mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation
        """

        file_name = str(file_name)
        main_part_moniker = str(main_part_moniker)
        tab_name = str(tab_name)
        method_result = self.wrapped.CreateGeometryModellerDesignInformation(file_name if file_name else '', main_part_moniker if main_part_moniker else '', tab_name if tab_name else '')
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_geometry_modeller_dimension(self) -> '_155.GeometryModellerDimension':
        """ 'CreateGeometryModellerDimension' is the original name of this method.

        Returns:
            mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension
        """

        method_result = self.wrapped.CreateGeometryModellerDimension()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_mesh_request_result(self) -> '_162.MeshRequestResult':
        """ 'CreateMeshRequestResult' is the original name of this method.

        Returns:
            mastapy.nodal_analysis.geometry_modeller_link.MeshRequestResult
        """

        method_result = self.wrapped.CreateMeshRequestResult()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_new_cad_face_group(self) -> '_305.CADFaceGroup':
        """ 'CreateNewCADFaceGroup' is the original name of this method.

        Returns:
            mastapy.geometry.two_d.CADFaceGroup
        """

        method_result = self.wrapped.CreateNewCADFaceGroup()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_new_circles_on_axis(self) -> '_1459.CirclesOnAxis':
        """ 'CreateNewCirclesOnAxis' is the original name of this method.

        Returns:
            mastapy.math_utility.CirclesOnAxis
        """

        method_result = self.wrapped.CreateNewCirclesOnAxis()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_new_faceted_body(self) -> '_1476.FacetedBody':
        """ 'CreateNewFacetedBody' is the original name of this method.

        Returns:
            mastapy.math_utility.FacetedBody
        """

        method_result = self.wrapped.CreateNewFacetedBody()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def flag_message_received(self):
        """ 'FlagMessageReceived' is the original name of this method."""

        self.wrapped.FlagMessageReceived()

    def geometry_modeller_document_loaded(self):
        """ 'GeometryModellerDocumentLoaded' is the original name of this method."""

        self.wrapped.GeometryModellerDocumentLoaded()

    def move_selected_component(self, origin: 'Vector3D', axis: 'Vector3D'):
        """ 'MoveSelectedComponent' is the original name of this method.

        Args:
            origin (Vector3D)
            axis (Vector3D)
        """

        origin = conversion.mp_to_pn_vector3d(origin)
        axis = conversion.mp_to_pn_vector3d(axis)
        self.wrapped.MoveSelectedComponent(origin, axis)

    def open_design_in_new_tab(self, design: '_2161.Design'):
        """ 'OpenDesignInNewTab' is the original name of this method.

        Args:
            design (mastapy.system_model.Design)
        """

        self.wrapped.OpenDesignInNewTab(design.wrapped if design else None)

    def run_command(self, command: 'str'):
        """ 'RunCommand' is the original name of this method.

        Args:
            command (str)
        """

        command = str(command)
        self.wrapped.RunCommand(command if command else '')

    def select_tab(self, tab_text: 'str'):
        """ 'SelectTab' is the original name of this method.

        Args:
            tab_text (str)
        """

        tab_text = str(tab_text)
        self.wrapped.SelectTab(tab_text if tab_text else '')

    def set_error(self, error: 'str'):
        """ 'SetError' is the original name of this method.

        Args:
            error (str)
        """

        error = str(error)
        self.wrapped.SetError(error if error else '')

    def set_mesh_request_result(self, mesh_request_result: '_162.MeshRequestResult'):
        """ 'SetMeshRequestResult' is the original name of this method.

        Args:
            mesh_request_result (mastapy.nodal_analysis.geometry_modeller_link.MeshRequestResult)
        """

        self.wrapped.SetMeshRequestResult(mesh_request_result.wrapped if mesh_request_result else None)

    def show_boxes(self, small_box: 'List[Vector3D]', big_box: 'List[Vector3D]'):
        """ 'ShowBoxes' is the original name of this method.

        Args:
            small_box (List[Vector3D])
            big_box (List[Vector3D])
        """

        small_box = conversion.mp_to_pn_objects_in_list(small_box)
        big_box = conversion.mp_to_pn_objects_in_list(big_box)
        self.wrapped.ShowBoxes(small_box, big_box)

    def output_default_report_to(self, file_path: 'str'):
        """ 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        """ 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        """ 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        """ 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        """ 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        """ 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        """

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
