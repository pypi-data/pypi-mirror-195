﻿"""_2995.py

GuideDxfModelSteadyStateSynchronousResponse
"""


from mastapy.system_model.part_model import _2411
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6826
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2958
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'GuideDxfModelSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelSteadyStateSynchronousResponse',)


class GuideDxfModelSteadyStateSynchronousResponse(_2958.ComponentSteadyStateSynchronousResponse):
    """GuideDxfModelSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _GUIDE_DXF_MODEL_STEADY_STATE_SYNCHRONOUS_RESPONSE

    def __init__(self, instance_to_wrap: 'GuideDxfModelSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2411.GuideDxfModel':
        """GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6826.GuideDxfModelLoadCase':
        """GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
