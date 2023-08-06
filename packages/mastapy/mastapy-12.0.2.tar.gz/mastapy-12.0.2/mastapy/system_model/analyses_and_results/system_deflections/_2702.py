﻿"""_2702.py

ExternalCADModelSystemDeflection
"""


from mastapy.system_model.part_model import _2408
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6813
from mastapy.system_model.analyses_and_results.power_flows import _4033
from mastapy.system_model.analyses_and_results.system_deflections import _2665
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ExternalCADModelSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelSystemDeflection',)


class ExternalCADModelSystemDeflection(_2665.ComponentSystemDeflection):
    """ExternalCADModelSystemDeflection

    This is a mastapy class.
    """

    TYPE = _EXTERNAL_CAD_MODEL_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'ExternalCADModelSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2408.ExternalCADModel':
        """ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6813.ExternalCADModelLoadCase':
        """ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_4033.ExternalCADModelPowerFlow':
        """ExternalCADModelPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
