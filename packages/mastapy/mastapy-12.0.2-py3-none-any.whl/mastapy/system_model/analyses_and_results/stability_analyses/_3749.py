"""_3749.py

ConnectorStabilityAnalysis
"""


from mastapy.system_model.part_model import _2403, _2396, _2422
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.couplings import _2553
from mastapy.system_model.analyses_and_results.stability_analyses import _3791
from mastapy._internal.python_net import python_net_import

_CONNECTOR_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ConnectorStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorStabilityAnalysis',)


class ConnectorStabilityAnalysis(_3791.MountableComponentStabilityAnalysis):
    """ConnectorStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CONNECTOR_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConnectorStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2403.Connector':
        """Connector: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2403.Connector.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to Connector. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_design_of_type_bearing(self) -> '_2396.Bearing':
        """Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2396.Bearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to Bearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_design_of_type_oil_seal(self) -> '_2422.OilSeal':
        """OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2422.OilSeal.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to OilSeal. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_design_of_type_shaft_hub_connection(self) -> '_2553.ShaftHubConnection':
        """ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2553.ShaftHubConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to ShaftHubConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
