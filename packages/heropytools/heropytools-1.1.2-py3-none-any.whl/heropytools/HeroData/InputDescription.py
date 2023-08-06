# *************************************************************** #
#               Copyright © Hero Imaging AB 2022. 				  #
#  					  All Rights Reserved.						  #
# *************************************************************** #

from __future__ import annotations
from typing import Callable, Any, Optional, List
from heropytools.Serialization.Attributes import Attributes
from heropytools.Serialization.CustomSerializer import CustomSerializer
from .NodeIOType import NodeIOType
from .NodeIOUtils import NodeIOUtils
from .IODescription import IODescription


class InputDescription(IODescription):

    def __init__(self, input_types: List[NodeIOType], min_connections: int = 1, max_connections: int = 1,
                 soft_type: str = "", id_value: str = None):
        IODescription.__init__(self, id_value)
        self._input_types = input_types
        self._soft_type = soft_type
        self._min_connections = min_connections
        self._max_connections = max_connections
        
    @property
    def input_types(self):
        return self._input_types
    
    @input_types.setter
    def input_types(self, values):
        raise AttributeError("Attribute is not writable.")

    @input_types.deleter
    def input_types(self):
        raise AttributeError("Attribute is not deletable.")
    
    @property
    def type_label(self):
        return self._soft_type
    
    @type_label.setter
    def type_label(self, values):
        raise AttributeError("Attribute is not writable.")

    @type_label.deleter
    def type_label(self):
        raise AttributeError("Attribute is not deletable.")
    
    @property
    def min_connections(self):
        return self._min_connections
    
    @min_connections.setter
    def min_connections(self, values):
        raise AttributeError("Attribute is not writable.")

    @min_connections.deleter
    def min_connections(self):
        raise AttributeError("Attribute is not deletable.")
    
    @property
    def max_connections(self):
        return self._max_connections
    
    @max_connections.setter
    def max_connections(self, values):
        raise AttributeError("Attribute is not writable.")

    @max_connections.deleter
    def max_connections(self):
        raise AttributeError("Attribute is not deletable.")

    @staticmethod
    def create_from_dict(data: dict):
        input_types = [NodeIOUtils.name2enum(descr) for descr in data["_input_types_as_names"]]
        input_descriptions = InputDescription(input_types, data["_min_connections"], data["_max_connections"], 
                                              data["_soft_type"], data["_id"])
        return input_descriptions

    @property
    def _input_types_as_names(self) -> List[str]:
        return [NodeIOUtils.enum2name(s) for s in self._input_types]

    def __eq__(self, other):
        return self._compare_lists(self._input_types, other._input_types) and \
               self._soft_type == other._soft_type and \
               self._min_connections == other._min_connections and \
               self._max_connections == other._max_connections and \
               self._id == other._id

    @staticmethod
    def _compare_lists(l1: list, l2: list):
        if len(l1) != len(l2):
            return False
        for i in range(len(l1)):
            if l1[i] != l2[i]:
                return False
        return True
    
    def __repr__(self) -> str:
        
        string = ''
        for input_type in self.input_types:
            string+=f'{input_type.name}, '
        
        string = string[:-2]
        
        string += ": ["
        string +=f'min_connections: {self.min_connections}, max_connections: {self.max_connections}'

        if self.type_label:
            string += f', type_label: \'{self.type_label}\''

        string += "]"
        return string
        
    # --- Autogenerated --- #

    # Name of the type.
    _type_str = "InputDescription"

    # Datatype attributes.
    _attributes = Attributes("InputDescription", version=0, member_count=5)

    # Serialization.
    def serialize(self, writer_fun: Callable[[Any, str, str, Optional[CustomSerializer]], None]):
        super(InputDescription, self).serialize(writer_fun)
        writer_fun(self._input_types_as_names, "String{}", "IT", None)
        writer_fun(self._max_connections, "Int32", "MaxC", None)
        writer_fun(self._min_connections, "Int32", "MinC", None)
        writer_fun(self._soft_type, "String", "ST", None)

    # Deserialization.
    @staticmethod
    def deserialize(reader_fun: Callable[[str, Optional[CustomSerializer]], Any]):
        data = super(InputDescription, InputDescription).deserialize(reader_fun)
        data["_input_types_as_names"], _ = reader_fun("String{}", None)
        data["_max_connections"], _ = reader_fun("Int32", None)
        data["_min_connections"], _ = reader_fun("Int32", None)
        data["_soft_type"], _ = reader_fun("String", None)
        return data
