"""_5129.py

KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed
"""


from mastapy.system_model.part_model.gears import _2493
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6845
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5126
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed',)


class KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed(_5126.KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed):
    """KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MODAL_ANALYSIS_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2493.KlingelnbergCycloPalloidHypoidGear':
        """KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6845.KlingelnbergCycloPalloidHypoidGearLoadCase':
        """KlingelnbergCycloPalloidHypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
