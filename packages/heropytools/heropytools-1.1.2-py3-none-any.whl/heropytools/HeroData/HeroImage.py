# *************************************************************** #
#               Copyright © Hero Imaging AB 2022. 				  #
#  					  All Rights Reserved.						  #
# *************************************************************** #

from __future__ import annotations
from typing import Callable, Any, Optional, List, Union
import numpy as np

from heropytools.Serialization.Attributes import Attributes
from heropytools.Serialization.CustomSerializer import CustomSerializer
from .CustomSerializers.TensorSerializer import TensorSerializer
from .CustomSerializers.Matrix3Serializer import Matrix3Serializer
from .SubjectInformation import SubjectInformation
from .ScanInformation import ScanInformation
from .HeroList import HeroList
from .ImageChannelDescription import ImageChannelDescription
from .HeroData import HeroData


class HeroImage(HeroData):

    def __init__(self, array: np.ndarray,
                 name: str = "",
                 position: np.ndarray = None,
                 voxel_size: np.ndarray = None,
                 orientation: np.ndarray = None,
                 subject: SubjectInformation = None,
                 scan: ScanInformation = None,
                 metadata: list = None,
                 value_unit: str = "",
                 channel_descriptions: List[ImageChannelDescription] = None):
        
        HeroData.__init__(self)

        if not isinstance(array, np.ndarray):
            raise Exception("The data matrix must be of type ndarray.")

        self._validate_data_type(array)

        if array.ndim < 3:
            self._tensor = self._append_to_3d(array)
        else:
            self._tensor = array

        self._name = name

        if position is None:
            self._position = np.array([0, 0, 0], dtype=np.float64)
        else:
            self._position = self._validate_and_reformat_vector3(position)

        if voxel_size is None:
            self._voxel_size = np.array([1, 1, 1], dtype=np.float64)
        else:
            self._voxel_size = self._validate_and_reformat_voxel_size(voxel_size)

        if orientation is None:
            self._orientation = np.eye(3, dtype=np.float64)
        else:
            self._validate_and_reformat_orientation(orientation)
            self._orientation = orientation

        if subject is None:
            self._subject = SubjectInformation()
        else:
            if not isinstance(subject, SubjectInformation):
                raise Exception("The subject must be of type: SubjectInformation")
            self._subject = subject

        if scan is None:
            self._scan = ScanInformation()
        else:
            if not isinstance(scan, ScanInformation):
                raise Exception("The scan must be of type: ScanInformation")
            self._scan = scan

        if metadata is None:
            self._image_metadata = self._create_default_meta_data()
        else:
            self._validate_meta_data(metadata)
            self._image_metadata = metadata

        self._value_unit = value_unit

        if channel_descriptions is None:
            self._channel_descriptions = self._create_default_channel_descriptions(self.Shape)
        else:
            self._validate_channel_descriptions(channel_descriptions, self.Shape)
            self._channel_descriptions = channel_descriptions

    def __repr__(self):
        string = "HeroImage("
        string += f"name=\"{self.Name}\", "
        string += f"shape={repr(self.Shape)}, "
        string += f"voxel_size={repr(self.VoxelSize)}, "
        string += f"position={repr(self.Position)}, "
        string += f"orientation={self.Orientation.tolist()}, "
        string += f"dtype={self._tensor.dtype} "
        string += ")"

        return string
    
    def __str__(self):
        string = f'HeroImage: {self.Name}\n'
        string += f'  ----------------------------------\n'
        string += f'  Shape: {self.Shape}\n'
        string += f'  Voxel size: {self.VoxelSize}\n'
        string += f'  Position: {self.Position}\n'
        string += f'  Orientation: {self.Orientation[0:3,0]}\n'
        string += f'               {self.Orientation[0:3,1]}\n'
        string += f'               {self.Orientation[0:3,2]}\n'
        string += f'  Type: \'{self.DType}\'\n'
        string += f'  ----------------------------------\n'

        return string
    
    # Define properties, setters and deleters

    @property
    def Array(self):
        """Get the shape of the image tensor"""
        return self._tensor

    @Array.setter
    def Array(self, value):
        if self._validate_input_array(value):
            self._tensor = value

    @Array.deleter
    def Array(self):
        raise AttributeError("Attribute is not deletable.")

    @property
    def Shape(self):
        """Get the shape of the image tensor"""
        return self._tensor.shape

    @Shape.setter
    def Shape(self, value):
        raise AttributeError("Attribute is not writable.")

    @Shape.deleter
    def Shape(self):
        raise AttributeError("Attribute is not deletable.")
    
    @property
    def ChannelShape(self):
        return self.Shape[3:] if len(self.Shape) > 3 else list()
    
    @ChannelShape.setter
    def ChannelShape(self, value):
        raise AttributeError("Attribute is not writable.")

    @ChannelShape.deleter
    def ChannelShape(self):
        raise AttributeError("Attribute is not deletable.")

    @property
    def SpatialShape(self):
        return self.Shape[:3]
    
    @SpatialShape.setter
    def SpatialShape(self, value):
        raise AttributeError("Attribute is not writable.")

    @SpatialShape.deleter
    def SpatialShape(self):
        raise AttributeError("Attribute is not deletable.")
    
    @property
    def VoxelSize(self):
        return self._voxel_size

    @VoxelSize.setter
    def VoxelSize(self, value):
        self._voxel_size = self._validate_and_reformat_voxel_size(value)

    @VoxelSize.deleter
    def VoxelSize(self):
        raise AttributeError("Attribute is not deletable.")

    @property
    def Position(self):
        return self._position

    @Position.setter
    def Position(self, value):
        self._position = self._validate_and_reformat_vector3(value)

    @Position.deleter
    def Position(self):
        raise AttributeError("Attribute is not deletable.")
    
    @property
    def Orientation(self):
        return self._orientation

    @Orientation.setter
    def Orientation(self, value):
        self._orientation = self._validate_and_reformat_orientation(value)

    @Orientation.deleter
    def Orientation(self):
        raise AttributeError("Attribute is not deletable.")
        
    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, value):
        if not isinstance(str, value):
            raise ValueError("The name must be a string.")
        self._name = value

    @Name.deleter
    def Name(self):
        raise AttributeError("Attribute 'name' is not deletable.")
    
    @property
    def Metadata(self):
        return self._image_metadata

    @Metadata.setter
    def Metadata(self, value):
        if not isinstance(list, value):
            raise Exception("The metadata must be a list.")
        if not len(value) == self.NumberOfVolumes:
            raise Exception("The size of the metadata must match the number of volumes in the image.")
        if not all(isinstance(x, dict) for x in value):
            raise Exception("The metadata must be a list of dictionaries.")
        self._name = value

    @Metadata.deleter
    def Metadata(self):
        raise AttributeError("Attribute 'metadata' is not deletable.")

    @property
    def DType(self):
        return self._tensor.dtype

    @property
    def ChannelDescriptions(self):
        return self._channel_descriptions

    @ChannelDescriptions.setter
    def ChannelDescriptions(self, value):
        if not isinstance(value, list) or not all(isinstance(x, ImageChannelDescription) for x in value):
            raise ValueError("The channel descriptions must be a list of ImageChannelDescription objects.")
        if not all(x.locations.size == y.locations.size for x, y in zip(value, self._channel_descriptions)):
            raise ValueError("The channel descriptions does not match the data matrix size.")
        self._channel_descriptions = value

    @ChannelDescriptions.deleter
    def ChannelDescriptions(self):
        raise AttributeError("Attribute is not deletable.")

    @property
    def NumberOfVolumes(self):
        sh = self.ChannelShape
        n = 1
        for i in range(len(sh)):
            n *= sh[i]
        return n

    @NumberOfVolumes.setter
    def NumberOfVolumes(self, value):
        raise AttributeError("Attribute 'number_of_volumes' is not writable.")

    @NumberOfVolumes.deleter
    def NumberOfVolumes(self):
        raise AttributeError("Attribute 'number_of_volumes' is not deletable.")

    @property
    def NumberOfSpatialElements(self):
        sh = self.SpatialShape
        n = 1
        for i in range(len(sh)):
            n *= sh[i]
        return n

    @NumberOfSpatialElements.setter
    def NumberOfSpatialElements(self, value):
        raise AttributeError("Attribute 'number_of_spatial_elements' is not writable.")

    @NumberOfSpatialElements.deleter
    def NumberOfSpatialElements(self):
        raise AttributeError("Attribute 'number_of_spatial_elements' is not deletable.")

    @property
    def NumberOfElements(self):
        sh = self.Shape
        n = 1
        for i in range(len(sh)):
            n *= sh[i]
        return n

    @NumberOfElements.setter
    def NumberOfElements(self, value):
        raise AttributeError("Attribute 'number_of_elements' is not writable.")

    @NumberOfElements.deleter
    def NumberOfElements(self):
        raise AttributeError("Attribute 'number_of_elements' is not deletable.")

    @property
    def Subject(self):
        return self._subject

    @Subject.setter
    def Subject(self, value):
        if not isinstance(SubjectInformation, value):
            raise ValueError("The subject must be a SubjectInformation object.")
        self._subject = value

    @Subject.deleter
    def Subject(self):
        raise AttributeError("Attribute 'subject' is not deletable.")

    @property
    def VoxelVolume(self):
        return np.prod(self.VoxelSize)

    @VoxelVolume.setter
    def VoxelVolume(self, value):
        raise AttributeError("Attribute 'voxel_volume' is not writable.")

    @VoxelVolume.deleter
    def VoxelVolume(self):
        raise AttributeError("Attribute 'voxel_volume' is not deletable.")

    @property
    def Volume(self):
        return self.NumberOfSpatialElements * self.VoxelVolume

    @Volume.setter
    def Volume(self, value):
        raise AttributeError("Attribute 'volume' is not writable.")

    @Volume.deleter
    def Volume(self):
        raise AttributeError("Attribute 'volume' is not deletable.")

    @property
    def FieldOfView(self):
        return self.SpatialShape * self.VoxelSize

    @FieldOfView.setter
    def FieldOfView(self, value):
        raise AttributeError("Attribute 'field_of_view' is not writable.")

    @FieldOfView.deleter
    def FieldOfView(self):
        raise AttributeError("Attribute 'field_of_view' is not deletable.")

    @property
    def Scan(self):
        return self._scan

    @Scan.setter
    def Scan(self, value):
        if not isinstance(ScanInformation, value):
            raise ValueError("The scan must be a ScanInformation object.")
        self._scan = value

    @Scan.deleter
    def Scan(self):
        raise AttributeError("Attribute 'scan' is not deletable.")

    def _validate_and_reformat_voxel_size(self, value):
        value = self._validate_and_reformat_vector3(value)
        if any(i <= 0 for i in value):
            raise ValueError('All elements in input must be greater than 0')
        return np.array(value, dtype=np.double)

    @staticmethod
    def _validate_data_type(matrix):
        dtype = matrix.dtype
        if not (dtype == np.int32 or dtype == np.int64 or dtype == np.float32 or dtype == np.float64 or
                dtype == np.complex64 or dtype == np.complex128 or dtype == bool):
            raise Exception(f"The image matrix data type = '{dtype.name}' is not supported.")

    @staticmethod
    def _append_to_3d(matrix):
        n_missing_dim = 3 - matrix.ndim
        new_shape = list(matrix.shape)
        new_shape.extend([1] * n_missing_dim)
        return np.reshape(matrix, new_shape)

    @staticmethod
    def _validate_and_reformat_vector3(value):
        if not isinstance(value, (tuple, list, np.ndarray)):
            raise TypeError('Input must be a list, tuple or np.ndarray')
        if len(value) != 3:
            raise ValueError('Input must have 3 elements.')
        return np.array(value, dtype=np.float64)
    
    def _validate_input_array(self, value: np.ndarray):
        if not isinstance(value, np.ndarray):
            raise TypeError("An image array array is a numpy array")
        if self.Shape != value.shape:
            raise ValueError("The shape of the image data must not change.")
        return True
    
    @staticmethod
    def _validate_and_reformat_orientation(orientation):
        if not isinstance(orientation, np.ndarray):
            raise Exception("An orientation matrix must be a 3 x 3 numpy array with float64 elements.")
        if orientation.shape != (3, 3) or orientation.dtype != np.float64:
            raise Exception("An orientation matrix must be a 3 x 3 numpy array with float64 elements.")
        return orientation

    def _create_default_meta_data(self):
        n_channels = self._get_number_of_channels()
        return [{}] * n_channels

    def _validate_meta_data(self, metadata):
        if not isinstance(metadata, list):
            raise Exception("The metadata must be a list.")

        for e in metadata:
            if not isinstance(e, dict):
                raise Exception("The metadata must be a list of dictionaries.")

        n_channels = self._get_number_of_channels()
        if n_channels != len(metadata):
            raise Exception("The metadata size must match the total number of channel elements in the image.")

    @staticmethod
    def _create_default_channel_descriptions(shape):
        channel_descriptions = list()
        for i, dim_size in enumerate(shape[3:]):
            channel_descriptions.append(ImageChannelDescription(np.zeros(dim_size), f"Ch{i}", ""))
        return channel_descriptions

    @staticmethod
    def _validate_channel_descriptions(channel_descriptions, shape):
        if not isinstance(channel_descriptions, list):
            raise Exception("The channel descriptions must be a list of ImageChannelDescription objects.")
        n_dim = len(shape) - 3
        if n_dim != len(channel_descriptions):
            raise Exception("The number of channel descriptions must match the number of channel dimensions.")
        for d in channel_descriptions:
            if not isinstance(d, ImageChannelDescription):
                raise Exception("The channel descriptions must be a list of ImageChannelDescription objects.")

    def _get_number_of_channels(self):
        channel_shape = np.array(self.Shape[3:])
        return int(channel_shape.prod())

    @staticmethod
    def create_from_dict(data: dict):
        """Create a HeroImage from a dictionary"""
        try:
            return HeroImage(
                            data['_tensor'],
                            name=data['_name'],
                            position=data['_position'],
                            voxel_size=data['_voxel_size'],
                            orientation=data['_orientation'],
                            subject=data['_subject'],
                            scan=data['_scan'],
                            metadata=data['_image_metadata'],
                            value_unit=data['_value_unit'],
                            channel_descriptions=data['_channel_descriptions'],
            )
        except KeyError as e:
            print(f'Missing {e} key in input dict')

    def __eq__(self, other: HeroImage):
        if not super(HeroImage, self).__eq__(other):
            return False
        if (self._tensor != other._tensor).any():
            return False
        if self._name != other._name:
            return False
        if (self._position != other._position).any():
            return False
        if (self._voxel_size != other._voxel_size).any():
            return False
        if (self._orientation != other._orientation).any():
            return False
        if self._value_unit != other._value_unit:
            return False
        if not self._compare_lists(self._channel_descriptions, other._channel_descriptions):
            return False  
        if not self._equal_metadata(self._image_metadata, other._image_metadata):
            return False

        return True

    @staticmethod
    def _compare_lists(l1: Union[list, tuple], l2: Union[list, tuple]):
        if len(l1) != len(l2):
            return False
        for i in range(len(l1)):
            if l1[i] != l2[i]:
                return False
        return True

    @staticmethod
    def _equal_metadata(m1, m2):
        if isinstance(m1, list):
            m1 = HeroList(m1)
        if isinstance(m2, list):
            m2 = HeroList(m2)
        return m1 == m2

    def get_container_id(self):
        return id(self)

    # --- Autogenerated --- #

    # Name of the type.
    _type_str = "HeroImage"

    # Datatype attributes.
    _attributes = Attributes("HI", version=1, member_count=10)

    # Serialization.
    def serialize(self, writer_fun: Callable[[Any, str, str, Optional[CustomSerializer]], None]):
        super(HeroImage, self).serialize(writer_fun)
        writer_fun(self._channel_descriptions, "ImageChannelDescription[]", "_channelDescriptions", None)
        writer_fun(self._image_metadata, "HeroList", "_imageMetadata", None)
        writer_fun(self._orientation, "Matrix3", "_orientation", Matrix3Serializer())
        writer_fun(self._position, "Vector3", "_position", None)
        writer_fun(self._tensor, "Tensor", "_tensor", TensorSerializer())
        writer_fun(self._voxel_size, "Vector3", "_voxelSize", None)
        writer_fun(self._name, "String", "Name", None)
        writer_fun(self._scan, "ScanInformation", "Scan", None)
        writer_fun(self._subject, "SubjectInformation", "Subject", None)
        writer_fun(self._value_unit, "String", "ValueUnit", None)

    # Deserialization.
    @staticmethod
    def deserialize(reader_fun: Callable[[str, Optional[CustomSerializer]], Any]):
        data = super(HeroImage, HeroImage).deserialize(reader_fun)
        data["_channel_descriptions"], _ = reader_fun("ImageChannelDescription[]", None)
        data["_image_metadata"], _ = reader_fun("HeroList", None)
        data["_orientation"], _ = reader_fun("Matrix3", Matrix3Serializer())
        data["_position"], _ = reader_fun("Vector3", None)
        data["_tensor"], _ = reader_fun("Tensor", TensorSerializer())
        data["_voxel_size"], _ = reader_fun("Vector3", None)
        data["_name"], _ = reader_fun("String", None)
        data["_scan"], _ = reader_fun("ScanInformation", None)
        data["_subject"], _ = reader_fun("SubjectInformation", None)
        data["_value_unit"], _ = reader_fun("String", None)
        return data
