"""_2244.py

OuterShaftSocketBase
"""


from mastapy.system_model.connections_and_sockets import _2252
from mastapy._internal.python_net import python_net_import

_OUTER_SHAFT_SOCKET_BASE = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'OuterShaftSocketBase')


__docformat__ = 'restructuredtext en'
__all__ = ('OuterShaftSocketBase',)


class OuterShaftSocketBase(_2252.ShaftSocket):
    """OuterShaftSocketBase

    This is a mastapy class.
    """

    TYPE = _OUTER_SHAFT_SOCKET_BASE

    def __init__(self, instance_to_wrap: 'OuterShaftSocketBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
