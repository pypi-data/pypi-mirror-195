"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import ai.lzy.v1.common.data_scheme_pb2
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class Whiteboard(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Status:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _StatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Whiteboard._Status.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        WHITEBOARD_STATUS_UNSPECIFIED: Whiteboard._Status.ValueType  # 0
        CREATED: Whiteboard._Status.ValueType  # 1
        FINALIZED: Whiteboard._Status.ValueType  # 2

    class Status(_Status, metaclass=_StatusEnumTypeWrapper): ...
    WHITEBOARD_STATUS_UNSPECIFIED: Whiteboard.Status.ValueType  # 0
    CREATED: Whiteboard.Status.ValueType  # 1
    FINALIZED: Whiteboard.Status.ValueType  # 2

    ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    FIELDS_FIELD_NUMBER: builtins.int
    STORAGE_FIELD_NUMBER: builtins.int
    NAMESPACE_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    CREATEDAT_FIELD_NUMBER: builtins.int
    id: builtins.str
    name: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def fields(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___WhiteboardField]: ...
    @property
    def storage(self) -> global___Storage: ...
    namespace: builtins.str
    status: global___Whiteboard.Status.ValueType
    @property
    def createdAt(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        name: builtins.str = ...,
        tags: collections.abc.Iterable[builtins.str] | None = ...,
        fields: collections.abc.Iterable[global___WhiteboardField] | None = ...,
        storage: global___Storage | None = ...,
        namespace: builtins.str = ...,
        status: global___Whiteboard.Status.ValueType = ...,
        createdAt: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["createdAt", b"createdAt", "storage", b"storage"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["createdAt", b"createdAt", "fields", b"fields", "id", b"id", "name", b"name", "namespace", b"namespace", "status", b"status", "storage", b"storage", "tags", b"tags"]) -> None: ...

global___Whiteboard = Whiteboard

class WhiteboardField(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    SCHEME_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def scheme(self) -> ai.lzy.v1.common.data_scheme_pb2.DataScheme: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        scheme: ai.lzy.v1.common.data_scheme_pb2.DataScheme | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["scheme", b"scheme"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "scheme", b"scheme"]) -> None: ...

global___WhiteboardField = WhiteboardField

class Storage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    URI_FIELD_NUMBER: builtins.int
    name: builtins.str
    description: builtins.str
    uri: builtins.str
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        description: builtins.str = ...,
        uri: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "name", b"name", "uri", b"uri"]) -> None: ...

global___Storage = Storage

class TimeBounds(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FROM__FIELD_NUMBER: builtins.int
    TO_FIELD_NUMBER: builtins.int
    @property
    def from_(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """from_ because of python 'from' keyword"""
    @property
    def to(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    def __init__(
        self,
        *,
        from_: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        to: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["from_", b"from_", "to", b"to"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["from_", b"from_", "to", b"to"]) -> None: ...

global___TimeBounds = TimeBounds
