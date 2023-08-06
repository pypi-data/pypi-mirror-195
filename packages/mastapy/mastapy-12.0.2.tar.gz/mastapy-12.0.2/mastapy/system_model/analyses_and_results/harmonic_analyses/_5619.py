"""_5619.py

AbstractPeriodicExcitationDetail
"""


from mastapy.electric_machines.harmonic_load_data import _1348, _1346, _1351
from mastapy._internal import constructor
from mastapy.electric_machines.results import _1296
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import (
    _6777, _6794, _6801, _6802,
    _6803, _6804, _6805, _6806,
    _6824, _6867, _6909
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_PERIODIC_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'AbstractPeriodicExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractPeriodicExcitationDetail',)


class AbstractPeriodicExcitationDetail(_0.APIBase):
    """AbstractPeriodicExcitationDetail

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_PERIODIC_EXCITATION_DETAIL

    def __init__(self, instance_to_wrap: 'AbstractPeriodicExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def harmonic_load_data(self) -> '_1348.HarmonicLoadDataBase':
        """HarmonicLoadDataBase: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _1348.HarmonicLoadDataBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to HarmonicLoadDataBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_dynamic_force_results(self) -> '_1296.DynamicForceResults':
        """DynamicForceResults: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _1296.DynamicForceResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to DynamicForceResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_base(self) -> '_1346.ElectricMachineHarmonicLoadDataBase':
        """ElectricMachineHarmonicLoadDataBase: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _1346.ElectricMachineHarmonicLoadDataBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_speed_dependent_harmonic_load_data(self) -> '_1351.SpeedDependentHarmonicLoadData':
        """SpeedDependentHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _1351.SpeedDependentHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to SpeedDependentHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_conical_gear_set_harmonic_load_data(self) -> '_6777.ConicalGearSetHarmonicLoadData':
        """ConicalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6777.ConicalGearSetHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ConicalGearSetHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_cylindrical_gear_set_harmonic_load_data(self) -> '_6794.CylindricalGearSetHarmonicLoadData':
        """CylindricalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6794.CylindricalGearSetHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to CylindricalGearSetHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data(self) -> '_6801.ElectricMachineHarmonicLoadData':
        """ElectricMachineHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6801.ElectricMachineHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_excel(self) -> '_6802.ElectricMachineHarmonicLoadDataFromExcel':
        """ElectricMachineHarmonicLoadDataFromExcel: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6802.ElectricMachineHarmonicLoadDataFromExcel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromExcel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_flux(self) -> '_6803.ElectricMachineHarmonicLoadDataFromFlux':
        """ElectricMachineHarmonicLoadDataFromFlux: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6803.ElectricMachineHarmonicLoadDataFromFlux.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromFlux. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_jmag(self) -> '_6804.ElectricMachineHarmonicLoadDataFromJMAG':
        """ElectricMachineHarmonicLoadDataFromJMAG: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6804.ElectricMachineHarmonicLoadDataFromJMAG.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromJMAG. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_masta(self) -> '_6805.ElectricMachineHarmonicLoadDataFromMasta':
        """ElectricMachineHarmonicLoadDataFromMasta: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6805.ElectricMachineHarmonicLoadDataFromMasta.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromMasta. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_motor_cad(self) -> '_6806.ElectricMachineHarmonicLoadDataFromMotorCAD':
        """ElectricMachineHarmonicLoadDataFromMotorCAD: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6806.ElectricMachineHarmonicLoadDataFromMotorCAD.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromMotorCAD. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_gear_set_harmonic_load_data(self) -> '_6824.GearSetHarmonicLoadData':
        """GearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6824.GearSetHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to GearSetHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_point_load_harmonic_load_data(self) -> '_6867.PointLoadHarmonicLoadData':
        """PointLoadHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6867.PointLoadHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to PointLoadHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_unbalanced_mass_harmonic_load_data(self) -> '_6909.UnbalancedMassHarmonicLoadData':
        """UnbalancedMassHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6909.UnbalancedMassHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to UnbalancedMassHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
