﻿"""_7256.py

FaceGearAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.gears import _2483
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.face import _442
from mastapy.system_model.analyses_and_results.static_loads import _6814
from mastapy.system_model.analyses_and_results.system_deflections import _2706
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7261
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'FaceGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearAdvancedSystemDeflection',)


class FaceGearAdvancedSystemDeflection(_7261.GearAdvancedSystemDeflection):
    """FaceGearAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'FaceGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2483.FaceGear':
        """FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_detailed_analysis(self) -> '_442.FaceGearRating':
        """FaceGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDetailedAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6814.FaceGearLoadCase':
        """FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2706.FaceGearSystemDeflection]':
        """List[FaceGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
