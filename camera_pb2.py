# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: camera.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'camera.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x63\x61mera.proto\"\x07\n\x05\x45mpty\"-\n\tFrameData\x12\r\n\x05\x66rame\x18\x01 \x01(\x0c\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x32\x35\n\rCameraService\x12$\n\x0cStreamFrames\x12\x06.Empty\x1a\n.FrameData0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'camera_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTY']._serialized_start=16
  _globals['_EMPTY']._serialized_end=23
  _globals['_FRAMEDATA']._serialized_start=25
  _globals['_FRAMEDATA']._serialized_end=70
  _globals['_CAMERASERVICE']._serialized_start=72
  _globals['_CAMERASERVICE']._serialized_end=125
# @@protoc_insertion_point(module_scope)
