# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpc_config_api.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ..config_manage import config_file_pb2 as config__file__pb2
from ..config_manage import config_file_response_pb2 as config__file__response__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15grpc_config_api.proto\x12\x02v1\x1a\x11\x63onfig_file.proto\x1a\x1a\x63onfig_file_response.proto2\xac\x01\n\x11PolarisConfigGRPC\x12\x45\n\rGetConfigFile\x12\x18.v1.ClientConfigFileInfo\x1a\x18.v1.ConfigClientResponse\"\x00\x12P\n\x10WatchConfigFiles\x12 .v1.ClientWatchConfigFileRequest\x1a\x18.v1.ConfigClientResponse\"\x00\x42\x97\x01\n6com.tencent.polaris.specification.api.v1.config.manageB\x18PolarisConfigGRPCServiceZCgithub.com/polarismesh/specification/source/go/api/v1/config_manageb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grpc_config_api_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n6com.tencent.polaris.specification.api.v1.config.manageB\030PolarisConfigGRPCServiceZCgithub.com/polarismesh/specification/source/go/api/v1/config_manage'
  _POLARISCONFIGGRPC._serialized_start=77
  _POLARISCONFIGGRPC._serialized_end=249
# @@protoc_insertion_point(module_scope)
