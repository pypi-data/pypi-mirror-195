"""_3715.py

AbstractShaftStabilityAnalysis
"""


from mastapy.system_model.part_model import _2392
from mastapy._internal import constructor
from mastapy.system_model.part_model.shaft_model import _2438
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.cycloidal import _2524
from mastapy.system_model.analyses_and_results.stability_analyses import _3714
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'AbstractShaftStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftStabilityAnalysis',)


class AbstractShaftStabilityAnalysis(_3714.AbstractShaftOrHousingStabilityAnalysis):
    """AbstractShaftStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_SHAFT_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'AbstractShaftStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2392.AbstractShaft':
        """AbstractShaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2392.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_design_of_type_shaft(self) -> '_2438.Shaft':
        """Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2438.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_design_of_type_cycloidal_disc(self) -> '_2524.CycloidalDisc':
        """CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2524.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
