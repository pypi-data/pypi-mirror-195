"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import ai.lzy.v1.common.storage_pb2
import ai.lzy.v1.workflow.workflow_pb2
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class StartWorkflowRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    WORKFLOWNAME_FIELD_NUMBER: builtins.int
    SNAPSHOTSTORAGE_FIELD_NUMBER: builtins.int
    STORAGENAME_FIELD_NUMBER: builtins.int
    workflowName: builtins.str
    @property
    def snapshotStorage(self) -> ai.lzy.v1.common.storage_pb2.StorageConfig: ...
    storageName: builtins.str
    def __init__(
        self,
        *,
        workflowName: builtins.str = ...,
        snapshotStorage: ai.lzy.v1.common.storage_pb2.StorageConfig | None = ...,
        storageName: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["snapshotStorage", b"snapshotStorage"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["snapshotStorage", b"snapshotStorage", "storageName", b"storageName", "workflowName", b"workflowName"]) -> None: ...

global___StartWorkflowRequest = StartWorkflowRequest

class StartWorkflowResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EXECUTIONID_FIELD_NUMBER: builtins.int
    executionId: builtins.str
    def __init__(
        self,
        *,
        executionId: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["executionId", b"executionId"]) -> None: ...

global___StartWorkflowResponse = StartWorkflowResponse

class FinishWorkflowRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    WORKFLOWNAME_FIELD_NUMBER: builtins.int
    EXECUTIONID_FIELD_NUMBER: builtins.int
    REASON_FIELD_NUMBER: builtins.int
    workflowName: builtins.str
    executionId: builtins.str
    reason: builtins.str
    def __init__(
        self,
        *,
        workflowName: builtins.str = ...,
        executionId: builtins.str = ...,
        reason: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["executionId", b"executionId", "reason", b"reason", "workflowName", b"workflowName"]) -> None: ...

global___FinishWorkflowRequest = FinishWorkflowRequest

class FinishWorkflowResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___FinishWorkflowResponse = FinishWorkflowResponse

class AbortWorkflowRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    WORKFLOWNAME_FIELD_NUMBER: builtins.int
    EXECUTIONID_FIELD_NUMBER: builtins.int
    REASON_FIELD_NUMBER: builtins.int
    workflowName: builtins.str
    executionId: builtins.str
    reason: builtins.str
    def __init__(
        self,
        *,
        workflowName: builtins.str = ...,
        executionId: builtins.str = ...,
        reason: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["executionId", b"executionId", "reason", b"reason", "workflowName", b"workflowName"]) -> None: ...

global___AbortWorkflowRequest = AbortWorkflowRequest

class AbortWorkflowResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___AbortWorkflowResponse = AbortWorkflowResponse

class ExecuteGraphRequest(google.protobuf.message.Message):
    """==================== ExecuteGraph ====================="""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    WORKFLOWNAME_FIELD_NUMBER: builtins.int
    EXECUTIONID_FIELD_NUMBER: builtins.int
    GRAPH_FIELD_NUMBER: builtins.int
    workflowName: builtins.str
    executionId: builtins.str
    @property
    def graph(self) -> ai.lzy.v1.workflow.workflow_pb2.Graph: ...
    def __init__(
        self,
        *,
        workflowName: builtins.str = ...,
        executionId: builtins.str = ...,
        graph: ai.lzy.v1.workflow.workflow_pb2.Graph | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["graph", b"graph"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["executionId", b"executionId", "graph", b"graph", "workflowName", b"workflowName"]) -> None: ...

global___ExecuteGraphRequest = ExecuteGraphRequest

class ExecuteGraphResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GRAPHID_FIELD_NUMBER: builtins.int
    graphId: builtins.str
    def __init__(
        self,
        *,
        graphId: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["graphId", b"graphId"]) -> None: ...

global___ExecuteGraphResponse = ExecuteGraphResponse

class GraphStatusRequest(google.protobuf.message.Message):
    """==================== GraphStatus ====================="""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EXECUTIONID_FIELD_NUMBER: builtins.int
    GRAPHID_FIELD_NUMBER: builtins.int
    executionId: builtins.str
    graphId: builtins.str
    def __init__(
        self,
        *,
        executionId: builtins.str = ...,
        graphId: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["executionId", b"executionId", "graphId", b"graphId"]) -> None: ...

global___GraphStatusRequest = GraphStatusRequest

class GraphStatusResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Waiting(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    class Executing(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        OPERATIONSCOMPLETED_FIELD_NUMBER: builtins.int
        OPERATIONSEXECUTING_FIELD_NUMBER: builtins.int
        OPERATIONSWAITING_FIELD_NUMBER: builtins.int
        MESSAGE_FIELD_NUMBER: builtins.int
        @property
        def operationsCompleted(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
            """List of completed operations"""
        @property
        def operationsExecuting(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
            """List of currently executing operations"""
        @property
        def operationsWaiting(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
            """List of waiting operations"""
        message: builtins.str
        """Human-readable message to show user"""
        def __init__(
            self,
            *,
            operationsCompleted: collections.abc.Iterable[builtins.str] | None = ...,
            operationsExecuting: collections.abc.Iterable[builtins.str] | None = ...,
            operationsWaiting: collections.abc.Iterable[builtins.str] | None = ...,
            message: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["message", b"message", "operationsCompleted", b"operationsCompleted", "operationsExecuting", b"operationsExecuting", "operationsWaiting", b"operationsWaiting"]) -> None: ...

    class Completed(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    class Failed(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        DESCRIPTION_FIELD_NUMBER: builtins.int
        description: builtins.str
        def __init__(
            self,
            *,
            description: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["description", b"description"]) -> None: ...

    WAITING_FIELD_NUMBER: builtins.int
    EXECUTING_FIELD_NUMBER: builtins.int
    COMPLETED_FIELD_NUMBER: builtins.int
    FAILED_FIELD_NUMBER: builtins.int
    @property
    def waiting(self) -> global___GraphStatusResponse.Waiting: ...
    @property
    def executing(self) -> global___GraphStatusResponse.Executing: ...
    @property
    def completed(self) -> global___GraphStatusResponse.Completed: ...
    @property
    def failed(self) -> global___GraphStatusResponse.Failed: ...
    def __init__(
        self,
        *,
        waiting: global___GraphStatusResponse.Waiting | None = ...,
        executing: global___GraphStatusResponse.Executing | None = ...,
        completed: global___GraphStatusResponse.Completed | None = ...,
        failed: global___GraphStatusResponse.Failed | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["completed", b"completed", "executing", b"executing", "failed", b"failed", "status", b"status", "waiting", b"waiting"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["completed", b"completed", "executing", b"executing", "failed", b"failed", "status", b"status", "waiting", b"waiting"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["status", b"status"]) -> typing_extensions.Literal["waiting", "executing", "completed", "failed"] | None: ...

global___GraphStatusResponse = GraphStatusResponse

class StopGraphRequest(google.protobuf.message.Message):
    """==================== StopGraph ====================="""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EXECUTIONID_FIELD_NUMBER: builtins.int
    GRAPHID_FIELD_NUMBER: builtins.int
    executionId: builtins.str
    graphId: builtins.str
    def __init__(
        self,
        *,
        executionId: builtins.str = ...,
        graphId: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["executionId", b"executionId", "graphId", b"graphId"]) -> None: ...

global___StopGraphRequest = StopGraphRequest

class StopGraphResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StopGraphResponse = StopGraphResponse

class ReadStdSlotsRequest(google.protobuf.message.Message):
    """==================== ReadStdSlots ====================="""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EXECUTIONID_FIELD_NUMBER: builtins.int
    executionId: builtins.str
    def __init__(
        self,
        *,
        executionId: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["executionId", b"executionId"]) -> None: ...

global___ReadStdSlotsRequest = ReadStdSlotsRequest

class ReadStdSlotsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Data(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        DATA_FIELD_NUMBER: builtins.int
        @property
        def data(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
        def __init__(
            self,
            *,
            data: collections.abc.Iterable[builtins.str] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["data", b"data"]) -> None: ...

    STDOUT_FIELD_NUMBER: builtins.int
    STDERR_FIELD_NUMBER: builtins.int
    @property
    def stdout(self) -> global___ReadStdSlotsResponse.Data: ...
    @property
    def stderr(self) -> global___ReadStdSlotsResponse.Data: ...
    def __init__(
        self,
        *,
        stdout: global___ReadStdSlotsResponse.Data | None = ...,
        stderr: global___ReadStdSlotsResponse.Data | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["data", b"data", "stderr", b"stderr", "stdout", b"stdout"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["data", b"data", "stderr", b"stderr", "stdout", b"stdout"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["data", b"data"]) -> typing_extensions.Literal["stdout", "stderr"] | None: ...

global___ReadStdSlotsResponse = ReadStdSlotsResponse

class GetAvailablePoolsRequest(google.protobuf.message.Message):
    """==================== GetAvailablePools ====================="""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EXECUTIONID_FIELD_NUMBER: builtins.int
    executionId: builtins.str
    def __init__(
        self,
        *,
        executionId: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["executionId", b"executionId"]) -> None: ...

global___GetAvailablePoolsRequest = GetAvailablePoolsRequest

class GetAvailablePoolsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    POOLSPECS_FIELD_NUMBER: builtins.int
    @property
    def poolSpecs(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[ai.lzy.v1.workflow.workflow_pb2.VmPoolSpec]: ...
    def __init__(
        self,
        *,
        poolSpecs: collections.abc.Iterable[ai.lzy.v1.workflow.workflow_pb2.VmPoolSpec] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["poolSpecs", b"poolSpecs"]) -> None: ...

global___GetAvailablePoolsResponse = GetAvailablePoolsResponse

class GetOrCreateDefaultStorageRequest(google.protobuf.message.Message):
    """==================== GetStorage ====================="""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___GetOrCreateDefaultStorageRequest = GetOrCreateDefaultStorageRequest

class GetOrCreateDefaultStorageResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STORAGE_FIELD_NUMBER: builtins.int
    @property
    def storage(self) -> ai.lzy.v1.common.storage_pb2.StorageConfig: ...
    def __init__(
        self,
        *,
        storage: ai.lzy.v1.common.storage_pb2.StorageConfig | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["storage", b"storage"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["storage", b"storage"]) -> None: ...

global___GetOrCreateDefaultStorageResponse = GetOrCreateDefaultStorageResponse
