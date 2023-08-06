"""_2023.py

MaximumStaticContactStressDutyCycle
"""


from mastapy.bearings.bearing_results.rolling import _2024
from mastapy._internal.python_net import python_net_import

_MAXIMUM_STATIC_CONTACT_STRESS_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'MaximumStaticContactStressDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('MaximumStaticContactStressDutyCycle',)


class MaximumStaticContactStressDutyCycle(_2024.MaximumStaticContactStressResultsAbstract):
    """MaximumStaticContactStressDutyCycle

    This is a mastapy class.
    """

    TYPE = _MAXIMUM_STATIC_CONTACT_STRESS_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'MaximumStaticContactStressDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
