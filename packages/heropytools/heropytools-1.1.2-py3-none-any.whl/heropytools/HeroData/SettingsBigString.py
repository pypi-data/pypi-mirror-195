# *************************************************************** #
#               Copyright © Hero Imaging AB 2022. 				  #
#  					  All Rights Reserved.						  #
# *************************************************************** #

from __future__ import annotations
from typing import Callable, Any, Optional
from heropytools.Serialization.Attributes import Attributes
from heropytools.Serialization.CustomSerializer import CustomSerializer

from .SettingsValue import SettingsValue


class SettingsBigString(SettingsValue):

    def __init__(self, value = "", min_length = 0, max_length = 2048, read_only=False, visible=True, description="", can_be_input=False, is_input=False, full_input_name=True):

        SettingsValue.__init__(self, read_only, visible, description, can_be_input, is_input, full_input_name)
        self._value = value
        self._min_length = min_length
        self._max_length = max_length

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        raise AttributeError("Attribute is not writable.")

    @value.deleter
    def value(self):
        raise AttributeError("Attribute is not deletable.")
    
    @property
    def min_length(self):
        return self._min_length
    
    @min_length.setter
    def min_length(self, value):
        raise AttributeError("Attribute is not writable.")

    @min_length.deleter
    def min_length(self):
        raise AttributeError("Attribute is not deletable.")
    
    @property
    def max_length(self):
        return self._max_length
    
    @max_length.setter
    def max_length(self, value):
        raise AttributeError("Attribute is not writable.")

    @max_length.deleter
    def max_length(self):
        raise AttributeError("Attribute is not deletable.")
    
    
    @staticmethod
    def create_from_dict(data: dict):
        s = SettingsBigString(data["_value"], data["_min_length"], data["_max_length"], data["_read_only"], data["_visible"], data["_description"], data["_can_be_input"], data["_is_input"], data["_full_input_name"])
        s._id = data["_id"]
        return s

    def __eq__(self, other):
        return super(SettingsBigString, self).__eq__(other) and self._value == other._value and self._min_length == other._min_length and self._max_length == other._max_length

    def __repr__(self) -> str:
        return  f'BigString: [value: \'{self.value}\', min_value: {self.min_length}, max_value: {self.max_length}, ' + super().__repr__()

    # --- Autogenerated --- #

    # Name of the type.
    _type_str = "SettingsBigString"

    # Datatype attributes.
    _attributes = Attributes("SettingsBigString", version=0, member_count=10)

    # Serialization.
    def serialize(self, writer_fun: Callable[[Any, str, str, Optional[CustomSerializer]], None]):
        super(SettingsBigString, self).serialize(writer_fun)
        writer_fun(self._min_length, "Int32", "MiL", None)
        writer_fun(self._max_length, "Int32", "ML", None)
        writer_fun(self._value, "String", "V", None)

    # Deserialization.
    @staticmethod
    def deserialize(reader_fun: Callable[[str, Optional[CustomSerializer]], Any]):
        data = super(SettingsBigString, SettingsBigString).deserialize(reader_fun)
        data["_min_length"], _ = reader_fun("Int32", None)
        data["_max_length"], _ = reader_fun("Int32", None)
        data["_value"], _ = reader_fun("String", None)
        return data
