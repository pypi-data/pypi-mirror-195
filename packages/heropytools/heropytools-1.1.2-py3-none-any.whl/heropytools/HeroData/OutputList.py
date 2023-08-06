# *************************************************************** #
#               Copyright © Hero Imaging AB 2022. 				  #
#  					  All Rights Reserved.						  #
# *************************************************************** #

from __future__ import annotations
from typing import Callable, Any, Optional
from heropytools.Serialization.Attributes import Attributes
from heropytools.Serialization.CustomSerializer import CustomSerializer
from .CustomSerializers.OrderedDictSerializer import OrderedDictSerializer
from .NodeIOType import NodeIOType
from .NodeIOUtils import NodeIOUtils
from .IODescription import IODescription
from .OutputDescription import OutputDescription
from collections import OrderedDict


from uuid import uuid4


class OutputList:

    def __init__(self, outputs: OrderedDict = None):
        if outputs is None:
            self._values = OrderedDict()
        else:
            self._values = outputs

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        self._values[key] = value

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self):
        return self._values

    def keys(self):
        return self._values.keys()
    
    @property
    def values(self):
        return self._values
    
    @values.setter
    def values(self, values):
        raise AttributeError("Attribute is not writable.")

    @values.deleter
    def values(self):
        raise AttributeError("Attribute is not deletable.")


    @staticmethod
    def create_from_dict(data: dict):
        return OutputList(data["_values"])

    def __eq__(self, other):
        if isinstance(other, OutputList):
            if len(self._values) != len(other):
                return False
            for key in self._values:
                if not self._values[key] == other[key]:
                    return False
        else:
            return False
        return True
    
    def __repr__(self) -> str:
        string = "OutputList({"
        for key, value in self._values.items():
            string+= f"\'{key}\': {value.output_type.name}, "
        return string[:-2] + "})"
        
    def get_container_id(self):
        pass
    
    # --- Autogenerated --- #

    # Name of the type.
    _type_str = "OutputList"

    # Datatype attributes.
    _attributes = Attributes("OutputList", version=0, member_count=1)

    # Serialization.
    def serialize(self, writer_fun: Callable[[Any, str, str, Optional[CustomSerializer]], None]):
        writer_fun(self._values, "OrderedDictionary", "V", OrderedDictSerializer("String", "IODescription"))

    # Deserialization.
    @staticmethod
    def deserialize(reader_fun: Callable[[str, Optional[CustomSerializer]], Any]):
        data = dict()
        data["_values"], _ = reader_fun("OrderedDictionary", OrderedDictSerializer("String", "IODescription"))
        return data
