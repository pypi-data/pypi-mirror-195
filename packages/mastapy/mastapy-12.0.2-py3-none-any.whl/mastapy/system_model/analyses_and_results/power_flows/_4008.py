﻿"""_4008.py

ConceptCouplingPowerFlow
"""


from mastapy.system_model.part_model.couplings import _2536
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6770
from mastapy.system_model.analyses_and_results.power_flows import _4019
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ConceptCouplingPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingPowerFlow',)


class ConceptCouplingPowerFlow(_4019.CouplingPowerFlow):
    """ConceptCouplingPowerFlow

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_POWER_FLOW

    def __init__(self, instance_to_wrap: 'ConceptCouplingPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2536.ConceptCoupling':
        """ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6770.ConceptCouplingLoadCase':
        """ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
