"""_7244.py

CVTPulleyAdvancedSystemDeflection
"""


from mastapy.system_model.part_model.couplings import _2542
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7292
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CVTPulleyAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyAdvancedSystemDeflection',)


class CVTPulleyAdvancedSystemDeflection(_7292.PulleyAdvancedSystemDeflection):
    """CVTPulleyAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CVT_PULLEY_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'CVTPulleyAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2542.CVTPulley':
        """CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
