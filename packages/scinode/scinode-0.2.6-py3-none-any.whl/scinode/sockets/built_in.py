from scinode.core.socket import NodeSocket
from scinode.serialization.built_in import SerializeNone, SerializePickle


class SocketGeneral(NodeSocket, SerializePickle):
    """General socket."""

    identifier: str = "General"
    default_value: float = None

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)


class SocketFloat(NodeSocket, SerializeNone):
    """Float socket."""

    identifier: str = "Float"
    default_value: float = 0.0

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)


class SocketInt(NodeSocket, SerializeNone):
    """Int socket."""

    identifier: str = "Int"
    default_value: int = 0

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)


class SocketString(NodeSocket, SerializeNone):
    """String socket."""

    identifier: str = "String"
    default_value: str = ""

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)


class SocketBool(NodeSocket, SerializeNone):
    """Bool socket."""

    identifier: str = "Bool"
    default_value: bool = False

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)


socket_list = [
    SocketGeneral,
    SocketInt,
    SocketFloat,
    SocketString,
    SocketBool,
]
