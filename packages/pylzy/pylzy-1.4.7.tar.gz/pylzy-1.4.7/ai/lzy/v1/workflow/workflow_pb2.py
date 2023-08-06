# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ai/lzy/v1/workflow/workflow.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ai.lzy.v1.common import data_scheme_pb2 as ai_dot_lzy_dot_v1_dot_common_dot_data__scheme__pb2
from ai.lzy.v1.validation import validation_pb2 as ai_dot_lzy_dot_v1_dot_validation_dot_validation__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ai/lzy/v1/workflow/workflow.proto',
  package='ai.lzy.v1.workflow',
  syntax='proto3',
  serialized_options=b'\n\022ai.lzy.v1.workflowB\003LWF',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n!ai/lzy/v1/workflow/workflow.proto\x12\x12\x61i.lzy.v1.workflow\x1a\"ai/lzy/v1/common/data-scheme.proto\x1a%ai/lzy/v1/validation/validation.proto\"\xb2\x07\n\tOperation\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x16\n\x07\x63ommand\x18\x03 \x01(\tB\x05\xe8\xc4\x91M\x01\x12\x41\n\ninputSlots\x18\x04 \x03(\x0b\x32-.ai.lzy.v1.workflow.Operation.SlotDescription\x12\x42\n\x0boutputSlots\x18\x05 \x03(\x0b\x32-.ai.lzy.v1.workflow.Operation.SlotDescription\x12\x13\n\x0b\x64ockerImage\x18\x06 \x01(\t\x12J\n\x11\x64ockerCredentials\x18\n \x01(\x0b\x32/.ai.lzy.v1.workflow.Operation.DockerCredentials\x12H\n\x10\x64ockerPullPolicy\x18\x0b \x01(\x0e\x32..ai.lzy.v1.workflow.Operation.DockerPullPolicy\x12=\n\x06python\x18\x07 \x01(\x0b\x32+.ai.lzy.v1.workflow.Operation.PythonEnvSpecH\x00\x12\x14\n\x0cpoolSpecName\x18\x08 \x01(\t\x12:\n\x03\x65nv\x18\t \x03(\x0b\x32&.ai.lzy.v1.workflow.Operation.EnvEntryB\x05\xe8\xc4\x91M\x01\x1a*\n\x08\x45nvEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x33\n\x0fSlotDescription\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x12\n\nstorageUri\x18\x02 \x01(\t\x1a\x96\x01\n\rPythonEnvSpec\x12\x0c\n\x04yaml\x18\x02 \x01(\t\x12M\n\x0clocalModules\x18\x03 \x03(\x0b\x32\x37.ai.lzy.v1.workflow.Operation.PythonEnvSpec.LocalModule\x1a(\n\x0bLocalModule\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\x1aT\n\x11\x44ockerCredentials\x12\x14\n\x0cregistryName\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x17\n\x08password\x18\x03 \x01(\tB\x05\xe8\xc4\x91M\x01\"B\n\x10\x44ockerPullPolicy\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06\x41LWAYS\x10\x01\x12\x11\n\rIF_NOT_EXISTS\x10\x02\x42\x13\n\x11\x65xecution_context\"W\n\x0f\x44\x61taDescription\x12\x12\n\nstorageUri\x18\x01 \x01(\t\x12\x30\n\ndataScheme\x18\x02 \x01(\x0b\x32\x1c.ai.lzy.v1.common.DataScheme\"\xac\x01\n\x05Graph\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\rparentGraphId\x18\x02 \x01(\t\x12\x31\n\noperations\x18\x03 \x03(\x0b\x32\x1d.ai.lzy.v1.workflow.Operation\x12=\n\x10\x64\x61taDescriptions\x18\x04 \x03(\x0b\x32#.ai.lzy.v1.workflow.DataDescription\x12\x0c\n\x04zone\x18\x05 \x01(\t\"\x86\x01\n\nVmPoolSpec\x12\x14\n\x0cpoolSpecName\x18\x01 \x01(\t\x12\x0f\n\x07\x63puType\x18\x02 \x01(\t\x12\x10\n\x08\x63puCount\x18\x03 \x01(\r\x12\x0f\n\x07gpuType\x18\x04 \x01(\t\x12\x10\n\x08gpuCount\x18\x05 \x01(\r\x12\r\n\x05ramGb\x18\x06 \x01(\r\x12\r\n\x05zones\x18\x07 \x03(\t\"\xb9\x01\n\x0fWhiteboardField\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x45\n\x07\x64\x65\x66\x61ult\x18\x02 \x01(\x0b\x32\x34.ai.lzy.v1.workflow.WhiteboardField.DefaultFieldDesc\x1aQ\n\x10\x44\x65\x66\x61ultFieldDesc\x12\x0b\n\x03uri\x18\x02 \x01(\t\x12\x30\n\ndataScheme\x18\x03 \x01(\x0b\x32\x1c.ai.lzy.v1.common.DataSchemeB\x19\n\x12\x61i.lzy.v1.workflowB\x03LWFb\x06proto3'
  ,
  dependencies=[ai_dot_lzy_dot_v1_dot_common_dot_data__scheme__pb2.DESCRIPTOR,ai_dot_lzy_dot_v1_dot_validation_dot_validation__pb2.DESCRIPTOR,])



_OPERATION_DOCKERPULLPOLICY = _descriptor.EnumDescriptor(
  name='DockerPullPolicy',
  full_name='ai.lzy.v1.workflow.Operation.DockerPullPolicy',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ALWAYS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='IF_NOT_EXISTS', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=992,
  serialized_end=1058,
)
_sym_db.RegisterEnumDescriptor(_OPERATION_DOCKERPULLPOLICY)


_OPERATION_ENVENTRY = _descriptor.Descriptor(
  name='EnvEntry',
  full_name='ai.lzy.v1.workflow.Operation.EnvEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ai.lzy.v1.workflow.Operation.EnvEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='ai.lzy.v1.workflow.Operation.EnvEntry.value', index=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=656,
  serialized_end=698,
)

_OPERATION_SLOTDESCRIPTION = _descriptor.Descriptor(
  name='SlotDescription',
  full_name='ai.lzy.v1.workflow.Operation.SlotDescription',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='ai.lzy.v1.workflow.Operation.SlotDescription.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='storageUri', full_name='ai.lzy.v1.workflow.Operation.SlotDescription.storageUri', index=1,
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
  serialized_start=700,
  serialized_end=751,
)

_OPERATION_PYTHONENVSPEC_LOCALMODULE = _descriptor.Descriptor(
  name='LocalModule',
  full_name='ai.lzy.v1.workflow.Operation.PythonEnvSpec.LocalModule',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='ai.lzy.v1.workflow.Operation.PythonEnvSpec.LocalModule.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='ai.lzy.v1.workflow.Operation.PythonEnvSpec.LocalModule.url', index=1,
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
  serialized_start=864,
  serialized_end=904,
)

_OPERATION_PYTHONENVSPEC = _descriptor.Descriptor(
  name='PythonEnvSpec',
  full_name='ai.lzy.v1.workflow.Operation.PythonEnvSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='yaml', full_name='ai.lzy.v1.workflow.Operation.PythonEnvSpec.yaml', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='localModules', full_name='ai.lzy.v1.workflow.Operation.PythonEnvSpec.localModules', index=1,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_OPERATION_PYTHONENVSPEC_LOCALMODULE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=754,
  serialized_end=904,
)

_OPERATION_DOCKERCREDENTIALS = _descriptor.Descriptor(
  name='DockerCredentials',
  full_name='ai.lzy.v1.workflow.Operation.DockerCredentials',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='registryName', full_name='ai.lzy.v1.workflow.Operation.DockerCredentials.registryName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='username', full_name='ai.lzy.v1.workflow.Operation.DockerCredentials.username', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='ai.lzy.v1.workflow.Operation.DockerCredentials.password', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\304\221M\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=906,
  serialized_end=990,
)

_OPERATION = _descriptor.Descriptor(
  name='Operation',
  full_name='ai.lzy.v1.workflow.Operation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='ai.lzy.v1.workflow.Operation.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='ai.lzy.v1.workflow.Operation.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='command', full_name='ai.lzy.v1.workflow.Operation.command', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\304\221M\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='inputSlots', full_name='ai.lzy.v1.workflow.Operation.inputSlots', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='outputSlots', full_name='ai.lzy.v1.workflow.Operation.outputSlots', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dockerImage', full_name='ai.lzy.v1.workflow.Operation.dockerImage', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dockerCredentials', full_name='ai.lzy.v1.workflow.Operation.dockerCredentials', index=6,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dockerPullPolicy', full_name='ai.lzy.v1.workflow.Operation.dockerPullPolicy', index=7,
      number=11, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='python', full_name='ai.lzy.v1.workflow.Operation.python', index=8,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='poolSpecName', full_name='ai.lzy.v1.workflow.Operation.poolSpecName', index=9,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='env', full_name='ai.lzy.v1.workflow.Operation.env', index=10,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\304\221M\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_OPERATION_ENVENTRY, _OPERATION_SLOTDESCRIPTION, _OPERATION_PYTHONENVSPEC, _OPERATION_DOCKERCREDENTIALS, ],
  enum_types=[
    _OPERATION_DOCKERPULLPOLICY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='execution_context', full_name='ai.lzy.v1.workflow.Operation.execution_context',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=133,
  serialized_end=1079,
)


_DATADESCRIPTION = _descriptor.Descriptor(
  name='DataDescription',
  full_name='ai.lzy.v1.workflow.DataDescription',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='storageUri', full_name='ai.lzy.v1.workflow.DataDescription.storageUri', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dataScheme', full_name='ai.lzy.v1.workflow.DataDescription.dataScheme', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=1081,
  serialized_end=1168,
)


_GRAPH = _descriptor.Descriptor(
  name='Graph',
  full_name='ai.lzy.v1.workflow.Graph',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='ai.lzy.v1.workflow.Graph.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parentGraphId', full_name='ai.lzy.v1.workflow.Graph.parentGraphId', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='operations', full_name='ai.lzy.v1.workflow.Graph.operations', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dataDescriptions', full_name='ai.lzy.v1.workflow.Graph.dataDescriptions', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='zone', full_name='ai.lzy.v1.workflow.Graph.zone', index=4,
      number=5, type=9, cpp_type=9, label=1,
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
  serialized_start=1171,
  serialized_end=1343,
)


_VMPOOLSPEC = _descriptor.Descriptor(
  name='VmPoolSpec',
  full_name='ai.lzy.v1.workflow.VmPoolSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='poolSpecName', full_name='ai.lzy.v1.workflow.VmPoolSpec.poolSpecName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cpuType', full_name='ai.lzy.v1.workflow.VmPoolSpec.cpuType', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cpuCount', full_name='ai.lzy.v1.workflow.VmPoolSpec.cpuCount', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gpuType', full_name='ai.lzy.v1.workflow.VmPoolSpec.gpuType', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gpuCount', full_name='ai.lzy.v1.workflow.VmPoolSpec.gpuCount', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ramGb', full_name='ai.lzy.v1.workflow.VmPoolSpec.ramGb', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='zones', full_name='ai.lzy.v1.workflow.VmPoolSpec.zones', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1346,
  serialized_end=1480,
)


_WHITEBOARDFIELD_DEFAULTFIELDDESC = _descriptor.Descriptor(
  name='DefaultFieldDesc',
  full_name='ai.lzy.v1.workflow.WhiteboardField.DefaultFieldDesc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='uri', full_name='ai.lzy.v1.workflow.WhiteboardField.DefaultFieldDesc.uri', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dataScheme', full_name='ai.lzy.v1.workflow.WhiteboardField.DefaultFieldDesc.dataScheme', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=1587,
  serialized_end=1668,
)

_WHITEBOARDFIELD = _descriptor.Descriptor(
  name='WhiteboardField',
  full_name='ai.lzy.v1.workflow.WhiteboardField',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='ai.lzy.v1.workflow.WhiteboardField.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='default', full_name='ai.lzy.v1.workflow.WhiteboardField.default', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_WHITEBOARDFIELD_DEFAULTFIELDDESC, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1483,
  serialized_end=1668,
)

_OPERATION_ENVENTRY.containing_type = _OPERATION
_OPERATION_SLOTDESCRIPTION.containing_type = _OPERATION
_OPERATION_PYTHONENVSPEC_LOCALMODULE.containing_type = _OPERATION_PYTHONENVSPEC
_OPERATION_PYTHONENVSPEC.fields_by_name['localModules'].message_type = _OPERATION_PYTHONENVSPEC_LOCALMODULE
_OPERATION_PYTHONENVSPEC.containing_type = _OPERATION
_OPERATION_DOCKERCREDENTIALS.containing_type = _OPERATION
_OPERATION.fields_by_name['inputSlots'].message_type = _OPERATION_SLOTDESCRIPTION
_OPERATION.fields_by_name['outputSlots'].message_type = _OPERATION_SLOTDESCRIPTION
_OPERATION.fields_by_name['dockerCredentials'].message_type = _OPERATION_DOCKERCREDENTIALS
_OPERATION.fields_by_name['dockerPullPolicy'].enum_type = _OPERATION_DOCKERPULLPOLICY
_OPERATION.fields_by_name['python'].message_type = _OPERATION_PYTHONENVSPEC
_OPERATION.fields_by_name['env'].message_type = _OPERATION_ENVENTRY
_OPERATION_DOCKERPULLPOLICY.containing_type = _OPERATION
_OPERATION.oneofs_by_name['execution_context'].fields.append(
  _OPERATION.fields_by_name['python'])
_OPERATION.fields_by_name['python'].containing_oneof = _OPERATION.oneofs_by_name['execution_context']
_DATADESCRIPTION.fields_by_name['dataScheme'].message_type = ai_dot_lzy_dot_v1_dot_common_dot_data__scheme__pb2._DATASCHEME
_GRAPH.fields_by_name['operations'].message_type = _OPERATION
_GRAPH.fields_by_name['dataDescriptions'].message_type = _DATADESCRIPTION
_WHITEBOARDFIELD_DEFAULTFIELDDESC.fields_by_name['dataScheme'].message_type = ai_dot_lzy_dot_v1_dot_common_dot_data__scheme__pb2._DATASCHEME
_WHITEBOARDFIELD_DEFAULTFIELDDESC.containing_type = _WHITEBOARDFIELD
_WHITEBOARDFIELD.fields_by_name['default'].message_type = _WHITEBOARDFIELD_DEFAULTFIELDDESC
DESCRIPTOR.message_types_by_name['Operation'] = _OPERATION
DESCRIPTOR.message_types_by_name['DataDescription'] = _DATADESCRIPTION
DESCRIPTOR.message_types_by_name['Graph'] = _GRAPH
DESCRIPTOR.message_types_by_name['VmPoolSpec'] = _VMPOOLSPEC
DESCRIPTOR.message_types_by_name['WhiteboardField'] = _WHITEBOARDFIELD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Operation = _reflection.GeneratedProtocolMessageType('Operation', (_message.Message,), {

  'EnvEntry' : _reflection.GeneratedProtocolMessageType('EnvEntry', (_message.Message,), {
    'DESCRIPTOR' : _OPERATION_ENVENTRY,
    '__module__' : 'ai.lzy.v1.workflow.workflow_pb2'
    # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.Operation.EnvEntry)
    })
  ,

  'SlotDescription' : _reflection.GeneratedProtocolMessageType('SlotDescription', (_message.Message,), {
    'DESCRIPTOR' : _OPERATION_SLOTDESCRIPTION,
    '__module__' : 'ai.lzy.v1.workflow.workflow_pb2'
    # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.Operation.SlotDescription)
    })
  ,

  'PythonEnvSpec' : _reflection.GeneratedProtocolMessageType('PythonEnvSpec', (_message.Message,), {

    'LocalModule' : _reflection.GeneratedProtocolMessageType('LocalModule', (_message.Message,), {
      'DESCRIPTOR' : _OPERATION_PYTHONENVSPEC_LOCALMODULE,
      '__module__' : 'ai.lzy.v1.workflow.workflow_pb2'
      # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.Operation.PythonEnvSpec.LocalModule)
      })
    ,
    'DESCRIPTOR' : _OPERATION_PYTHONENVSPEC,
    '__module__' : 'ai.lzy.v1.workflow.workflow_pb2'
    # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.Operation.PythonEnvSpec)
    })
  ,

  'DockerCredentials' : _reflection.GeneratedProtocolMessageType('DockerCredentials', (_message.Message,), {
    'DESCRIPTOR' : _OPERATION_DOCKERCREDENTIALS,
    '__module__' : 'ai.lzy.v1.workflow.workflow_pb2'
    # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.Operation.DockerCredentials)
    })
  ,
  'DESCRIPTOR' : _OPERATION,
  '__module__' : 'ai.lzy.v1.workflow.workflow_pb2'
  # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.Operation)
  })
_sym_db.RegisterMessage(Operation)
_sym_db.RegisterMessage(Operation.EnvEntry)
_sym_db.RegisterMessage(Operation.SlotDescription)
_sym_db.RegisterMessage(Operation.PythonEnvSpec)
_sym_db.RegisterMessage(Operation.PythonEnvSpec.LocalModule)
_sym_db.RegisterMessage(Operation.DockerCredentials)

DataDescription = _reflection.GeneratedProtocolMessageType('DataDescription', (_message.Message,), {
  'DESCRIPTOR' : _DATADESCRIPTION,
  '__module__' : 'ai.lzy.v1.workflow.workflow_pb2'
  # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.DataDescription)
  })
_sym_db.RegisterMessage(DataDescription)

Graph = _reflection.GeneratedProtocolMessageType('Graph', (_message.Message,), {
  'DESCRIPTOR' : _GRAPH,
  '__module__' : 'ai.lzy.v1.workflow.workflow_pb2'
  # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.Graph)
  })
_sym_db.RegisterMessage(Graph)

VmPoolSpec = _reflection.GeneratedProtocolMessageType('VmPoolSpec', (_message.Message,), {
  'DESCRIPTOR' : _VMPOOLSPEC,
  '__module__' : 'ai.lzy.v1.workflow.workflow_pb2'
  # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.VmPoolSpec)
  })
_sym_db.RegisterMessage(VmPoolSpec)

WhiteboardField = _reflection.GeneratedProtocolMessageType('WhiteboardField', (_message.Message,), {

  'DefaultFieldDesc' : _reflection.GeneratedProtocolMessageType('DefaultFieldDesc', (_message.Message,), {
    'DESCRIPTOR' : _WHITEBOARDFIELD_DEFAULTFIELDDESC,
    '__module__' : 'ai.lzy.v1.workflow.workflow_pb2'
    # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.WhiteboardField.DefaultFieldDesc)
    })
  ,
  'DESCRIPTOR' : _WHITEBOARDFIELD,
  '__module__' : 'ai.lzy.v1.workflow.workflow_pb2'
  # @@protoc_insertion_point(class_scope:ai.lzy.v1.workflow.WhiteboardField)
  })
_sym_db.RegisterMessage(WhiteboardField)
_sym_db.RegisterMessage(WhiteboardField.DefaultFieldDesc)


DESCRIPTOR._options = None
_OPERATION_ENVENTRY._options = None
_OPERATION_DOCKERCREDENTIALS.fields_by_name['password']._options = None
_OPERATION.fields_by_name['command']._options = None
_OPERATION.fields_by_name['env']._options = None
# @@protoc_insertion_point(module_scope)
