"""_7306.py

SpringDamperAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2555
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6888
from mastapy.system_model.analyses_and_results.system_deflections import _2762
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7239
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'SpringDamperAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperAdvancedSystemDeflection',)


class SpringDamperAdvancedSystemDeflection(_7239.CouplingAdvancedSystemDeflection):
    """SpringDamperAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'SpringDamperAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2555.SpringDamper':
        """SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6888.SpringDamperLoadCase':
        """SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2762.SpringDamperSystemDeflection]':
        """List[SpringDamperSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblySystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
