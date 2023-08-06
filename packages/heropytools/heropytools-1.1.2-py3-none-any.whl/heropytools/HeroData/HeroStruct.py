# *************************************************************** #
#               Copyright © Hero Imaging AB 2022. 				  #
#  					  All Rights Reserved.						  #
# *************************************************************** #

from __future__ import annotations
from typing import Callable, Any, Optional
import re
from heropytools.Serialization.Attributes import Attributes
from heropytools.Serialization.CustomSerializer import CustomSerializer
from .CustomSerializers.DictionarySerializer import DictionarySerializer

from .HeroData import HeroData
from .HeroDataType import HeroDataType


class HeroStruct(HeroData):

    def __init__(self, data: dict = None):
        
        HeroData.__init__(self)
        if data is None:
            self._data = dict()
        else:
            self._validate_data(data)
            self._data = data
    
    def __len__(self):
        return len(self._data)

    @staticmethod
    def _validate_data(data):
        for key in data.keys():
            HeroStruct._validate_key(key)
            HeroStruct._validate_value(data[key])

    @staticmethod
    def _validate_key(key):
        if not isinstance(key, str):
            raise Exception(f"Cannot interpret the dictionary as a HeroStruct. A key must be a string.")
        if len(key) < 1:
            raise Exception(f"Cannot interpret the dictionary as a HeroStruct. A key cannot be empty.")

        if not (key[0].isalpha or key[0] == '_'):
            raise Exception(f"Cannot interpret the dictionary as a HeroStruct. A key must start with a letter or a '_'.")

        if not re.match(r'^[A-Za-z0-9_]+$', key):
            raise Exception(f"Cannot interpret the dictionary as a HeroStruct. A key must only contain alpha-numeric or '_' letters.")

        if len(key) > 1:
            if key[1] == '_':
                raise Exception(f"Cannot interpret the dictionary as a HeroStruct. A key must not start with double underscore.")
    
    @staticmethod
    def _validate_value(value):
        if not (type(value).__name__ in HeroStruct._type2element_data_type):
            raise Exception(f"Cannot interpret the dictionary as a HeroStruct. A value type {type(value).__name__} is not supported.")

    @staticmethod
    def create(obj):
        return HeroStruct(obj)

    def __eq__(self, other: HeroStruct):
        if not super(HeroStruct, self).__eq__(other):
            return False
        if len(self) != len(other):
            return False
        for k in self._data.keys():
            if not self._cmp_elements(self._data[k], other._data[k]):
                return False
        return True

    @staticmethod
    def _cmp_elements(v1, v2):
        if not isinstance(v1, HeroData):
            v1 = HeroData.create(v1)
        if not isinstance(v2, HeroData):
            v2 = HeroData.create(v2)
        return v1 == v2

    @staticmethod
    def create_from_dict(data: dict):
        return data['_data']

    # --- Autogenerated --- #

    # Name of the type.
    _type_str = "HeroStruct"

    # Datatype attributes.
    _attributes = Attributes("HSt", version=0, member_count=1)

    # Serialization.
    def serialize(self, writer_fun: Callable[[Any, str, str, Optional[CustomSerializer]], None]):
        super(HeroStruct, self).serialize(writer_fun)
        writer_fun(self._data, "Dictionary`2", "_data", DictionarySerializer("String", "HeroData"))

    # Deserialization.
    @staticmethod
    def deserialize(reader_fun: Callable[[str, Optional[CustomSerializer]], Any]):
        data = super(HeroStruct, HeroStruct).deserialize(reader_fun)
        data["_data"], _ = reader_fun("Dictionary`2", DictionarySerializer("String", "HeroData"))
        return data
