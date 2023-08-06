# *************************************************************** #
#               Copyright © Hero Imaging AB 2022. 				  #
#  					  All Rights Reserved.						  #
# *************************************************************** #

from __future__ import annotations
from typing import Callable, Any, Optional
from pandas import Series
from heropytools.Serialization.Attributes import Attributes
from heropytools.Serialization.CustomSerializer import CustomSerializer
from .CustomSerializers.DataFrameColumnSerializer import DataFrameColumnSerializer

from .HeroData import HeroData
from .HeroDataType import HeroDataType


class HeroColumn(HeroData):

    def __init__(self, data):
        HeroData.__init__(self)
        self.validate_column(data)
        self._data = data

    @staticmethod
    def create(obj):
        return HeroColumn(obj)

    @staticmethod
    def validate_column(data: Series):
        if not isinstance(data, Series):
            raise Exception(f"Cannot interpret the type {type(data).__name__} as a HeroColumn.")
        if not DataFrameColumnSerializer.is_serializable(data):
            raise Exception(f"Cannot interpret a column of type {data.dtype.name} as a HeroColumn.")

    @staticmethod
    def create_from_dict(data: dict):
        return data['_data']

    def __eq__(self, other: HeroColumn):
        if not super(HeroColumn, self).__eq__(other):
            return False
        return self._data.equals(other._data)
            

    # --- Autogenerated --- #

    # Name of the type.
    _type_str = "HeroColumn"

    # Datatype attributes.
    _attributes = Attributes("HC", version=0, member_count=1)

    # Serialization.
    def serialize(self, writer_fun: Callable[[Any, str, str, Optional[CustomSerializer]], None]):
        super(HeroColumn, self).serialize(writer_fun)
        writer_fun(self._data, "DataFrameColumn", "_data", DataFrameColumnSerializer())

    # Deserialization.
    @staticmethod
    def deserialize(reader_fun: Callable[[str, Optional[CustomSerializer]], Any]):
        data = super(HeroColumn, HeroColumn).deserialize(reader_fun)
        data["_data"], _ = reader_fun("DataFrameColumn", DataFrameColumnSerializer())
        return data
