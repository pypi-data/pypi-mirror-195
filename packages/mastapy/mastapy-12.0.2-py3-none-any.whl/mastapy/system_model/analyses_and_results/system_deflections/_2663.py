"""_2663.py

ClutchSystemDeflection
"""


from mastapy.system_model.part_model.couplings import _2533
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6765
from mastapy.system_model.analyses_and_results.system_deflections import _2661, _2681
from mastapy.system_model.analyses_and_results.power_flows import _4003
from mastapy._internal.python_net import python_net_import

_CLUTCH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ClutchSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchSystemDeflection',)


class ClutchSystemDeflection(_2681.CouplingSystemDeflection):
    """ClutchSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CLUTCH_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'ClutchSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2533.Clutch':
        """Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6765.ClutchLoadCase':
        """ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def clutch_connection(self) -> '_2661.ClutchConnectionSystemDeflection':
        """ClutchConnectionSystemDeflection: 'ClutchConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClutchConnection

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_4003.ClutchPowerFlow':
        """ClutchPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
