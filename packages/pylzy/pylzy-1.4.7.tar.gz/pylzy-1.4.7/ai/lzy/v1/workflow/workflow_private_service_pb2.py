# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ai/lzy/v1/workflow/workflow-private-service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ai/lzy/v1/workflow/workflow-private-service.proto',
  package='ai.lzy.v1.workflow',
  syntax='proto3',
  serialized_options=b'\n\022ai.lzy.v1.workflowB\005LWFPS',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n1ai/lzy/v1/workflow/workflow-private-service.proto\x12\x12\x61i.lzy.v1.workflow\"-\n\x15\x44\x65leteWorkflowRequest\x12\x14\n\x0cworkflowName\x18\x01 \x01(\t\"\x18\n\x16\x44\x65leteWorkflowResponse\"<\n\x15\x41\x62ortExecutionRequest\x12\x13\n\x0b\x65xecutionId\x18\x01 \x01(\t\x12\x0e\n\x06reason\x18\x02 \x01(\t\"\x18\n\x16\x41\x62ortExecutionResponse2\xed\x01\n\x19LzyWorkflowPrivateService\x12g\n\x0e\x44\x65leteWorkflow\x12).ai.lzy.v1.workflow.DeleteWorkflowRequest\x1a*.ai.lzy.v1.workflow.DeleteWorkflowResponse\x12g\n\x0e\x41\x62ortExecution\x12).ai.lzy.v1.workflow.AbortExecutionRequest\x1a*.ai.lzy.v1.workflow.AbortExecutionResponseB\x1b\n\x12\x61i.lzy.v1.workflowB\x05LWFPSb\x06proto3'
)




_DELETEWORKFLOWREQUEST = _descriptor.Descriptor(
  name='DeleteWorkflowRequest',
  full_name='ai.lzy.v1.workflow.DeleteWorkflowRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='workflowName', full_name='ai.lzy.v1.workflow.DeleteWorkflowRequest.workflowName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=118,
)


_DELETEWORKFLOWRESPONSE = _descriptor.Descriptor(
  name='DeleteWorkflowResponse',
  full_name='ai.lzy.v1.workflow.DeleteWorkflowResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=120,
  serialized_end=144,
)


_ABORTEXECUTIONREQUEST = _descriptor.Descriptor(
  name='AbortExecutionRequest',
  full_name='ai.lzy.v1.workflow.AbortExecutionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='executionId', full_name='ai.lzy.v1.workflow.AbortExecutionRequest.executionId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reason', full_name='ai.lzy.v1.workflow.AbortExecutionRequest.reason', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=146,
  serialized_end=206,
)


_ABORTEXECUTIONRESPONSE = _descriptor.Descriptor(
  name='AbortExecutionResponse',
  full_name='ai.lzy.v1.workflow.AbortExecutionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=208,
  serialized_end=232,
)

DESCRIPTOR.message_types_by_name['DeleteWorkflowRequest'] = _DELETEWORKFLOWREQUEST
DESCRIPTOR.message_types_by_name['DeleteWorkflowResponse'] = _DELETEWORKFLOWRESPONSE
DESCRIPTOR.message_types_by_name['AbortExecutionRequest'] = _ABORTEXECUTIONREQUEST
DESCRIPTOR.message_types_by_name['AbortExecutionResponse'] = _ABORTEXECUTIONRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DeleteWorkflowRequest = _reflection.GeneratedProtocolMessageType('DeleteWorkflowRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEWORKFLOWREQUEST,
  '__module__' : 'ai.lzy.v1.workflow.workflow_private_service_pb2'
  # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.DeleteWorkflowRequest)
  })
_sym_db.RegisterMessage(DeleteWorkflowRequest)

DeleteWorkflowResponse = _reflection.GeneratedProtocolMessageType('DeleteWorkflowResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEWORKFLOWRESPONSE,
  '__module__' : 'ai.lzy.v1.workflow.workflow_private_service_pb2'
  # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.DeleteWorkflowResponse)
  })
_sym_db.RegisterMessage(DeleteWorkflowResponse)

AbortExecutionRequest = _reflection.GeneratedProtocolMessageType('AbortExecutionRequest', (_message.Message,), {
  'DESCRIPTOR' : _ABORTEXECUTIONREQUEST,
  '__module__' : 'ai.lzy.v1.workflow.workflow_private_service_pb2'
  # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.AbortExecutionRequest)
  })
_sym_db.RegisterMessage(AbortExecutionRequest)

AbortExecutionResponse = _reflection.GeneratedProtocolMessageType('AbortExecutionResponse', (_message.Message,), {
  'DESCRIPTOR' : _ABORTEXECUTIONRESPONSE,
  '__module__' : 'ai.lzy.v1.workflow.workflow_private_service_pb2'
  # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.AbortExecutionResponse)
  })
_sym_db.RegisterMessage(AbortExecutionResponse)


DESCRIPTOR._options = None

_LZYWORKFLOWPRIVATESERVICE = _descriptor.ServiceDescriptor(
  name='LzyWorkflowPrivateService',
  full_name='ai.lzy.v1.workflow.LzyWorkflowPrivateService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=235,
  serialized_end=472,
  methods=[
  _descriptor.MethodDescriptor(
    name='DeleteWorkflow',
    full_name='ai.lzy.v1.workflow.LzyWorkflowPrivateService.DeleteWorkflow',
    index=0,
    containing_service=None,
    input_type=_DELETEWORKFLOWREQUEST,
    output_type=_DELETEWORKFLOWRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='AbortExecution',
    full_name='ai.lzy.v1.workflow.LzyWorkflowPrivateService.AbortExecution',
    index=1,
    containing_service=None,
    input_type=_ABORTEXECUTIONREQUEST,
    output_type=_ABORTEXECUTIONRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_LZYWORKFLOWPRIVATESERVICE)

DESCRIPTOR.services_by_name['LzyWorkflowPrivateService'] = _LZYWORKFLOWPRIVATESERVICE

# @@protoc_insertion_point(module_scope)
