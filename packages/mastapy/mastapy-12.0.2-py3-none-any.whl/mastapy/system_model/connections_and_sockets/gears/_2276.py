﻿"""_2276.py

KlingelnbergCycloPalloidConicalGearMesh
"""


from mastapy.system_model.connections_and_sockets.gears import _2265
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidConicalGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearMesh',)


class KlingelnbergCycloPalloidConicalGearMesh(_2265.ConicalGearMesh):
    """KlingelnbergCycloPalloidConicalGearMesh

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
