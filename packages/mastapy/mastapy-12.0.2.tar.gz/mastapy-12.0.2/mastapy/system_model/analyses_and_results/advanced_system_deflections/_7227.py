﻿"""_7227.py

ConceptCouplingAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2536
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6770
from mastapy.system_model.analyses_and_results.system_deflections import _2669
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7239
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ConceptCouplingAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingAdvancedSystemDeflection',)


class ConceptCouplingAdvancedSystemDeflection(_7239.CouplingAdvancedSystemDeflection):
    """ConceptCouplingAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'ConceptCouplingAdvancedSystemDeflection.TYPE'):
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

    @property
    def assembly_system_deflection_results(self) -> 'List[_2669.ConceptCouplingSystemDeflection]':
        """List[ConceptCouplingSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblySystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
