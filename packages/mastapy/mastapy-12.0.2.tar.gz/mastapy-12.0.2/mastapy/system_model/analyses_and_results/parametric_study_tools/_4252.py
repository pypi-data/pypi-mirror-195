﻿"""_4252.py

BeltDriveParametricStudyTool
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2531, _2541
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6752, _6785
from mastapy.system_model.analyses_and_results.system_deflections import _2650
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4358
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'BeltDriveParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveParametricStudyTool',)


class BeltDriveParametricStudyTool(_4358.SpecialisedAssemblyParametricStudyTool):
    """BeltDriveParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _BELT_DRIVE_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'BeltDriveParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2531.BeltDrive':
        """BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        if _2531.BeltDrive.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to BeltDrive. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6752.BeltDriveLoadCase':
        """BeltDriveLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        if _6752.BeltDriveLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to BeltDriveLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2650.BeltDriveSystemDeflection]':
        """List[BeltDriveSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblySystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
