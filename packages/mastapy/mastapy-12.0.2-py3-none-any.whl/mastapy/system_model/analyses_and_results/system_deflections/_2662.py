﻿"""_2662.py

ClutchHalfSystemDeflection
"""


from mastapy.system_model.part_model.couplings import _2534
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6764
from mastapy.system_model.analyses_and_results.power_flows import _4002
from mastapy.system_model.analyses_and_results.system_deflections import _2680
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ClutchHalfSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfSystemDeflection',)


class ClutchHalfSystemDeflection(_2680.CouplingHalfSystemDeflection):
    """ClutchHalfSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CLUTCH_HALF_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'ClutchHalfSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2534.ClutchHalf':
        """ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6764.ClutchHalfLoadCase':
        """ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_4002.ClutchHalfPowerFlow':
        """ClutchHalfPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
