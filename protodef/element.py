# coding: utf8
'''protobuf各个元素定义'''

class HeaderKind(object):
  """header类型"""
  SYNTAX = 'syntax'
  PACKAGE = 'package'
  IMPORT = 'import'
  OPTION = 'option'

class Header:
  def __init__(self, header_type, header_name, header_value):
    self.type = header_type
    self.name = header_name
    self.value = header_value

  def __str__(self):
    return '%s: %s=%s' % (self.type, self.name, self.value)

class Field:
  '''field基类'''

  def __init__(self, name, number):
    self.name = name
    self.number = number
    self.comment = None
    self.index = None

  def isDeprecated(self):
    return self.comment != None and self.comment.find('@deprecated') >= 0

  def __str__(self):
    return '%d: %s=%d #%s' % (self.index, self.name, self.number, self.comment)

class TypeKind:
  '''field type的类型'''

  BASE = 1 # protobuf基本类型
  REF = 2 # 自定义的引用类型
  MAP = 3 # map

class FieldType:
  '''field的type'''

  def __init__(self, type_kind, type_pkg, type_name, key_type=None, value_type=None):
    self.kind = type_kind
    self.pkg = type_pkg
    self.name = type_name

    self.key_type = None
    self.value_type = None

  def __str__(self):
    if self.pkg:
      return '%s[%s]' % (self.name, self.kind)
    else:
      return '%s.%s[%s]' % (self.pkg, self.name, self.kind)

class MessageField(Field):
  '''message中的field定义'''

  def __init__(self, field_type, field_name, field_number):
    Field.__init__(self, field_name, field_number)
    self.type = field_type
    self.decorations = set()

  def addDecoration(self, decoration):
    self.decorations.add(decoration)

  def isRepeated(self):
    return 'repeated' in self.decorations

  def __str__(self):
    s = self.index + ':'
    if len(self.decorations) > 0:
      s = s + (' %s' % self.decorations)
    s = s + (' %s %s=%d' % (self.type, self.name, self.number))
    if self.comment:
      s = s + (' # %s' % self.comment)
    return s

class EnumField(Field):
  '''enum中的field定义'''

  pass

class DataDef:
  '''数据结构基类'''
  def __init__(self, name):
    self.proto = None
    self.name = name
    self.fields = []
    self.comment = None

  def addField(self, field):
    self.fields.append(field)

  def isDeprecated(self):
    return self.comment != None and self.comment.find('@deprecated') >= 0

  def __str__(self):
    s = '%s %s {' % (type(self), self.name)
    first = True
    for field in self.fields:
      if first:
        first = False
      else:
        s = s + ', '
      s = s + field.__str__()
    s = s + '}'
    if self.comment:
      s = s + (' # %s' % self.comment)
    return s

class Message(DataDef):
  '''protobuf中的message'''
  pass

class Enum(DataDef):
  '''protobuf中的enum'''
  pass

class Protobuf:
  '''proto文件'''
  def __init__(self):
    self.filepath = None
    self.headers = {}
    self.imports = {}
    self.options = {}

    self.messages = []
    self.enums = []
    self.datadefs = {}

  def addHeader(self, header):
    if header.type == HeaderKind.IMPORT:
      self.imports[header.name] = header
    elif header.type == HeaderKind.OPTION:
      self.options[header.name] = header
    else:
      self.headers[header.name] = header

  def getHeader(self, header_name):
    return self.headers[header_name]

  def getOption(self, option_name):
    return self.options[option_name]

  def addDataDef(self, data_def):
    self.datadefs[data_def.name] = data_def
    pkg = self.getHeader(HeaderKind.PACKAGE)
    if isinstance(data_def, Message):
      for field in data_def.fields:
        if not field.type.pkg:
          field.type.pkg = pkg
      self.messages.append(data_def)
    else:
      self.enums.append(data_def)

  def getDataDef(self, data_name):
    return self.datadefs[data_name]

  def __str__(self):
    s = self.filepath
    if len(self.headers) > 0:
      s = '%s Header%s' % (s, self.__arr2str(self.headers))
    if len(self.imports) > 0:
      s = '%s Import%s' % (s, self.__arr2str(self.imports))
    if len(self.options) > 0:
      s = '%s Option%s' % (s, self.__arr2str(self.options))
    if len(self.messages) > 0:
      s = '%s Message%s' % (s, self.__arr2str(self.messages))
    if len(self.enums) > 0:
      s = '%s Enum%s' % (s, self.__arr2str(self.enums))
    return s

  def __arr2str(self, arr):
    s = '['
    first = True
    for item in arr:
      if first:
        first = False
      else:
        s = s + ', '
      s = s + item.__str__()
    s = s + ']'
