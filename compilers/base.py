# coding: utf8

import os
import re
# for sub class
from protodef.element import *

class Compiler:
  '''所有编译Compiler的基类'''
  def __init__(self, loader, writer, type_resolver):
    self.loader = loader
    self.writer = writer
    self.type_resolver = type_resolver
    self.outputed = set()
    self.skip_files = []

  def addSkip(self, files):
    for f in files:
      f = f.replace('*', '[^/]*')
      p = re.compile(f)
      self.skip_files.append(p)

  def skipFile(self, filepath):
    relpath = os.path.relpath(filepath, self.loader.proto_dir)
    for p in self.skip_files:
      if p.match(relpath):
        return True
      # if not os.path.exists(f):
      #   continue
      # if filepath.startswith(f + '/'):
      #   return True
      # if filepath == f:
      #   return True
    return False

  def addLine(self, line):
    if line:
      self.output = self.output + line
    self.output += '\n'

  def compile(self, arr):
    for path in arr:
      if os.path.isdir(path):
        self.compileDir(path)
      else:
        self.compileFile(path)

  def compileDir(self, dirpath):
    arr = []
    for f in os.listdir(dirpath):
      if f.startswith('.'):
        continue
      path = os.path.join(dirpath, f)
      arr.append(path)
    self.compile(arr)

  def compileFile(self, filepath):
    if self.skipFile(filepath):
      print '! skip %s' % filepath
      return
    proto = self.loader.loadAbspath(filepath)
    for import_proto in proto.import_protos:
      self.compileProto(import_proto)
    self.compileProto(proto)

  def compileProto(self, proto):
    filepath = os.path.join(proto.proto_dir, proto.proto_file)
    if filepath in self.outputed:
      return
    if self.skipProto(proto):
      return
    self.writer.beforeProto(proto, self)
    self.compileMsgs(proto.messages)
    self.compileEnums(proto.enums)
    self.writer.afterProto(proto, self)
    self.outputed.add(filepath)
    print '. compile %s' % filepath

  def skipProto(self, proto):
    # default not skip any proto
    return False

  def compileMsgs(self, messages):
    self.beforeMsgs(messages)
    for msg in messages:
      if msg.isDeprecated() or msg.ignored():
        continue
      self.writer.beforeDataDef(msg)
      self.compileMsg(msg, self.__filterValidFields(msg))
      self.writer.afterDataDef(msg)
    self.afterMsgs(messages)

  def beforeMsgs(self, messages):
    pass

  def afterMsgs(self, messages):
    pass

  def compileEnums(self, enums):
    self.beforeEnums(enums)
    for enum in enums:
      if enum.isDeprecated() or enum.ignored():
        continue
      self.writer.beforeDataDef(enum)
      self.compileEnum(enum, self.__filterValidFields(enum))
      self.writer.afterDataDef(enum)
    self.afterEnums(enums)

  def beforeEnums(self, enums):
    pass

  def afterEnums(self, enums):
    pass

  def __filterValidFields(self, data_def):
    fields = []
    for field in data_def.fields:
      if field.isDeprecated() or field.ignored():
        continue
      fields.append(field)
    return fields

  def compileMsg(self, msg, fields):
    pass

  def compileEnum(self, enum, fields):
    pass

class Writer:
  def __init__(self, out_dir, file_ext):
    self.out_dir = out_dir
    self.file_ext = file_ext
    self.outf = None

  def beforeProto(self, proto, compiler):
    pass

  def afterProto(self, proto, compiler):
    pass

  def beforeDataDef(self, data_def):
    pass

  def afterDataDef(self, data_def):
    pass

  def done(self):
    self.close()
    pass

  def _prepare(self, path, proto):
    self.close()
    d = os.path.dirname(path)
    if not os.path.exists(d):
      os.makedirs(d)
    self.outf = file(path, 'w')
    self._writeHeader(proto)

  def _writeHeader(self, proto):
    if not proto:
      return
    self.outf.write('// generated from %s by py-protoc, NEVER CHANGE!!\n\n' % proto.proto_file)

  def writeline(self, line=None):
    if line:
      self.outf.write(line)
    self.outf.write('\n')

  def close(self):
    if self.outf:
      self.outf.close()

class TypeResolver:
  '''处理type的映射和默认值'''

  def resolveField(self, field):
    '''处理field的type，返回`(type_text, default_value_text)`'''
    pass

  def resolveBaseType(self, base_type):
    '''处理protobuf中的base type，返回`(type_text, default_value_text)`'''
    pass

