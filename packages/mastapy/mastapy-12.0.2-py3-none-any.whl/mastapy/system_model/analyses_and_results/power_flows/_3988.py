"""_3988.py

BearingPowerFlow
"""


from mastapy.system_model.part_model import _2396
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6750
from mastapy.bearings.bearing_results.rolling import _2033
from mastapy.system_model.analyses_and_results.power_flows import _4016
from mastapy._internal.python_net import python_net_import

_BEARING_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BearingPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingPowerFlow',)


class BearingPowerFlow(_4016.ConnectorPowerFlow):
    """BearingPowerFlow

    This is a mastapy class.
    """

    TYPE = _BEARING_POWER_FLOW

    def __init__(self, instance_to_wrap: 'BearingPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2396.Bearing':
        """Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6750.BearingLoadCase':
        """BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rolling_bearing_speed_results(self) -> '_2033.RollingBearingSpeedResults':
        """RollingBearingSpeedResults: 'RollingBearingSpeedResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollingBearingSpeedResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
