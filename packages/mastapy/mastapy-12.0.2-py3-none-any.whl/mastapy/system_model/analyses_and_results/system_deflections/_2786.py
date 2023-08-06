"""_2786.py

WormGearMeshSystemDeflection
"""


from mastapy.gears.rating.worm import _367
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.gears import _2287
from mastapy.system_model.analyses_and_results.static_loads import _6913
from mastapy.system_model.analyses_and_results.power_flows import _4107
from mastapy.system_model.analyses_and_results.system_deflections import _2709
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'WormGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshSystemDeflection',)


class WormGearMeshSystemDeflection(_2709.GearMeshSystemDeflection):
    """WormGearMeshSystemDeflection

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_MESH_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'WormGearMeshSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rating(self) -> '_367.WormGearMeshRating':
        """WormGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_detailed_analysis(self) -> '_367.WormGearMeshRating':
        """WormGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDetailedAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2287.WormGearMesh':
        """WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6913.WormGearMeshLoadCase':
        """WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_4107.WormGearMeshPowerFlow':
        """WormGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
