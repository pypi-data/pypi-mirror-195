﻿"""_4072.py

RingPinsPowerFlow
"""


from mastapy.system_model.part_model.cycloidal import _2525
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6873
from mastapy.system_model.analyses_and_results.power_flows import _4058
from mastapy._internal.python_net import python_net_import

_RING_PINS_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'RingPinsPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsPowerFlow',)


class RingPinsPowerFlow(_4058.MountableComponentPowerFlow):
    """RingPinsPowerFlow

    This is a mastapy class.
    """

    TYPE = _RING_PINS_POWER_FLOW

    def __init__(self, instance_to_wrap: 'RingPinsPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2525.RingPins':
        """RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6873.RingPinsLoadCase':
        """RingPinsLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
