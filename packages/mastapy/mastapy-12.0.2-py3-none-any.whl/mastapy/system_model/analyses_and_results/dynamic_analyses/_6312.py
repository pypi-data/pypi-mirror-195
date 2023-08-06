﻿"""_6312.py

SpringDamperConnectionDynamicAnalysis
"""


from mastapy.system_model.connections_and_sockets.couplings import _2308
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6886
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6246
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'SpringDamperConnectionDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionDynamicAnalysis',)


class SpringDamperConnectionDynamicAnalysis(_6246.CouplingConnectionDynamicAnalysis):
    """SpringDamperConnectionDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_CONNECTION_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2308.SpringDamperConnection':
        """SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6886.SpringDamperConnectionLoadCase':
        """SpringDamperConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
