"""_4542.py

CoaxialConnectionModalAnalysis
"""


from mastapy.system_model.connections_and_sockets import _2227
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.cycloidal import _2293
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6766, _6788
from mastapy.system_model.analyses_and_results.system_deflections import _2664, _2686
from mastapy.system_model.analyses_and_results.modal_analyses import _4624
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CoaxialConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionModalAnalysis',)


class CoaxialConnectionModalAnalysis(_4624.ShaftToMountableComponentConnectionModalAnalysis):
    """CoaxialConnectionModalAnalysis

    This is a mastapy class.
    """

    TYPE = _COAXIAL_CONNECTION_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'CoaxialConnectionModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2227.CoaxialConnection':
        """CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2227.CoaxialConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CoaxialConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6766.CoaxialConnectionLoadCase':
        """CoaxialConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        if _6766.CoaxialConnectionLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_load_case to CoaxialConnectionLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2664.CoaxialConnectionSystemDeflection':
        """CoaxialConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        if _2664.CoaxialConnectionSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CoaxialConnectionSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
