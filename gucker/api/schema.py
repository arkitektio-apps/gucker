from mikro.scalars import AffineMatrix, Parquet, AssignationID, Store, MetricValue, File
from mikro.rath import MikroRath
from mikro.traits import (
    Vectorizable,
    ROI,
    Omero,
    PhysicalSize,
    Stage,
    Position,
    Representation,
    Table,
)
from typing import Dict, Optional, Literal, Tuple
from rath.scalars import ID
from mikro.funcs import execute, aexecute
from datetime import datetime
from pydantic import Field, BaseModel
from enum import Enum


class CommentableModels(str, Enum):
    GRUNNLAG_USERMETA = "GRUNNLAG_USERMETA"
    GRUNNLAG_ANTIBODY = "GRUNNLAG_ANTIBODY"
    GRUNNLAG_OBJECTIVE = "GRUNNLAG_OBJECTIVE"
    GRUNNLAG_CAMERA = "GRUNNLAG_CAMERA"
    GRUNNLAG_INSTRUMENT = "GRUNNLAG_INSTRUMENT"
    GRUNNLAG_DATASET = "GRUNNLAG_DATASET"
    GRUNNLAG_EXPERIMENT = "GRUNNLAG_EXPERIMENT"
    GRUNNLAG_CONTEXT = "GRUNNLAG_CONTEXT"
    GRUNNLAG_RELATION = "GRUNNLAG_RELATION"
    GRUNNLAG_DATALINK = "GRUNNLAG_DATALINK"
    GRUNNLAG_EXPERIMENTALGROUP = "GRUNNLAG_EXPERIMENTALGROUP"
    GRUNNLAG_ANIMAL = "GRUNNLAG_ANIMAL"
    GRUNNLAG_OMEROFILE = "GRUNNLAG_OMEROFILE"
    GRUNNLAG_MODEL = "GRUNNLAG_MODEL"
    GRUNNLAG_SAMPLE = "GRUNNLAG_SAMPLE"
    GRUNNLAG_STAGE = "GRUNNLAG_STAGE"
    GRUNNLAG_CHANNEL = "GRUNNLAG_CHANNEL"
    GRUNNLAG_POSITION = "GRUNNLAG_POSITION"
    GRUNNLAG_ERA = "GRUNNLAG_ERA"
    GRUNNLAG_TIMEPOINT = "GRUNNLAG_TIMEPOINT"
    GRUNNLAG_REPRESENTATION = "GRUNNLAG_REPRESENTATION"
    GRUNNLAG_OMERO = "GRUNNLAG_OMERO"
    GRUNNLAG_DIMENSIONMAP = "GRUNNLAG_DIMENSIONMAP"
    GRUNNLAG_VIEW = "GRUNNLAG_VIEW"
    GRUNNLAG_METRIC = "GRUNNLAG_METRIC"
    GRUNNLAG_THUMBNAIL = "GRUNNLAG_THUMBNAIL"
    GRUNNLAG_VIDEO = "GRUNNLAG_VIDEO"
    GRUNNLAG_ROI = "GRUNNLAG_ROI"
    GRUNNLAG_LABEL = "GRUNNLAG_LABEL"
    GRUNNLAG_FEATURE = "GRUNNLAG_FEATURE"
    BORD_TABLE = "BORD_TABLE"
    BORD_GRAPH = "BORD_GRAPH"


class SharableModels(str, Enum):
    """Sharable Models are models that can be shared amongst users and groups. They representent the models of the DB"""

    GRUNNLAG_USERMETA = "GRUNNLAG_USERMETA"
    GRUNNLAG_ANTIBODY = "GRUNNLAG_ANTIBODY"
    GRUNNLAG_OBJECTIVE = "GRUNNLAG_OBJECTIVE"
    GRUNNLAG_CAMERA = "GRUNNLAG_CAMERA"
    GRUNNLAG_INSTRUMENT = "GRUNNLAG_INSTRUMENT"
    GRUNNLAG_DATASET = "GRUNNLAG_DATASET"
    GRUNNLAG_EXPERIMENT = "GRUNNLAG_EXPERIMENT"
    GRUNNLAG_CONTEXT = "GRUNNLAG_CONTEXT"
    GRUNNLAG_RELATION = "GRUNNLAG_RELATION"
    GRUNNLAG_DATALINK = "GRUNNLAG_DATALINK"
    GRUNNLAG_EXPERIMENTALGROUP = "GRUNNLAG_EXPERIMENTALGROUP"
    GRUNNLAG_ANIMAL = "GRUNNLAG_ANIMAL"
    GRUNNLAG_OMEROFILE = "GRUNNLAG_OMEROFILE"
    GRUNNLAG_MODEL = "GRUNNLAG_MODEL"
    GRUNNLAG_SAMPLE = "GRUNNLAG_SAMPLE"
    GRUNNLAG_STAGE = "GRUNNLAG_STAGE"
    GRUNNLAG_CHANNEL = "GRUNNLAG_CHANNEL"
    GRUNNLAG_POSITION = "GRUNNLAG_POSITION"
    GRUNNLAG_ERA = "GRUNNLAG_ERA"
    GRUNNLAG_TIMEPOINT = "GRUNNLAG_TIMEPOINT"
    GRUNNLAG_REPRESENTATION = "GRUNNLAG_REPRESENTATION"
    GRUNNLAG_OMERO = "GRUNNLAG_OMERO"
    GRUNNLAG_DIMENSIONMAP = "GRUNNLAG_DIMENSIONMAP"
    GRUNNLAG_VIEW = "GRUNNLAG_VIEW"
    GRUNNLAG_METRIC = "GRUNNLAG_METRIC"
    GRUNNLAG_THUMBNAIL = "GRUNNLAG_THUMBNAIL"
    GRUNNLAG_VIDEO = "GRUNNLAG_VIDEO"
    GRUNNLAG_ROI = "GRUNNLAG_ROI"
    GRUNNLAG_LABEL = "GRUNNLAG_LABEL"
    GRUNNLAG_FEATURE = "GRUNNLAG_FEATURE"
    BORD_TABLE = "BORD_TABLE"
    BORD_GRAPH = "BORD_GRAPH"


class LokClientGrantType(str, Enum):
    """An enumeration."""

    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"
    "Backend (Client Credentials)"
    IMPLICIT = "IMPLICIT"
    "Implicit Grant"
    AUTHORIZATION_CODE = "AUTHORIZATION_CODE"
    "Authorization Code"
    PASSWORD = "PASSWORD"
    "Password"
    SESSION = "SESSION"
    "Django Session"


class LinkableModels(str, Enum):
    """LinkableModels Models are models that can be shared amongst users and groups. They representent the models of the DB"""

    ADMIN_LOGENTRY = "ADMIN_LOGENTRY"
    AUTH_PERMISSION = "AUTH_PERMISSION"
    AUTH_GROUP = "AUTH_GROUP"
    CONTENTTYPES_CONTENTTYPE = "CONTENTTYPES_CONTENTTYPE"
    SESSIONS_SESSION = "SESSIONS_SESSION"
    TAGGIT_TAG = "TAGGIT_TAG"
    TAGGIT_TAGGEDITEM = "TAGGIT_TAGGEDITEM"
    KOMMENT_COMMENT = "KOMMENT_COMMENT"
    DB_TESTMODEL = "DB_TESTMODEL"
    LOK_LOKUSER = "LOK_LOKUSER"
    LOK_LOKAPP = "LOK_LOKAPP"
    LOK_LOKCLIENT = "LOK_LOKCLIENT"
    GUARDIAN_USEROBJECTPERMISSION = "GUARDIAN_USEROBJECTPERMISSION"
    GUARDIAN_GROUPOBJECTPERMISSION = "GUARDIAN_GROUPOBJECTPERMISSION"
    GRUNNLAG_USERMETA = "GRUNNLAG_USERMETA"
    GRUNNLAG_ANTIBODY = "GRUNNLAG_ANTIBODY"
    GRUNNLAG_OBJECTIVE = "GRUNNLAG_OBJECTIVE"
    GRUNNLAG_CAMERA = "GRUNNLAG_CAMERA"
    GRUNNLAG_INSTRUMENT = "GRUNNLAG_INSTRUMENT"
    GRUNNLAG_DATASET = "GRUNNLAG_DATASET"
    GRUNNLAG_EXPERIMENT = "GRUNNLAG_EXPERIMENT"
    GRUNNLAG_CONTEXT = "GRUNNLAG_CONTEXT"
    GRUNNLAG_RELATION = "GRUNNLAG_RELATION"
    GRUNNLAG_DATALINK = "GRUNNLAG_DATALINK"
    GRUNNLAG_EXPERIMENTALGROUP = "GRUNNLAG_EXPERIMENTALGROUP"
    GRUNNLAG_ANIMAL = "GRUNNLAG_ANIMAL"
    GRUNNLAG_OMEROFILE = "GRUNNLAG_OMEROFILE"
    GRUNNLAG_MODEL = "GRUNNLAG_MODEL"
    GRUNNLAG_SAMPLE = "GRUNNLAG_SAMPLE"
    GRUNNLAG_STAGE = "GRUNNLAG_STAGE"
    GRUNNLAG_CHANNEL = "GRUNNLAG_CHANNEL"
    GRUNNLAG_POSITION = "GRUNNLAG_POSITION"
    GRUNNLAG_ERA = "GRUNNLAG_ERA"
    GRUNNLAG_TIMEPOINT = "GRUNNLAG_TIMEPOINT"
    GRUNNLAG_REPRESENTATION = "GRUNNLAG_REPRESENTATION"
    GRUNNLAG_OMERO = "GRUNNLAG_OMERO"
    GRUNNLAG_DIMENSIONMAP = "GRUNNLAG_DIMENSIONMAP"
    GRUNNLAG_VIEW = "GRUNNLAG_VIEW"
    GRUNNLAG_METRIC = "GRUNNLAG_METRIC"
    GRUNNLAG_THUMBNAIL = "GRUNNLAG_THUMBNAIL"
    GRUNNLAG_VIDEO = "GRUNNLAG_VIDEO"
    GRUNNLAG_ROI = "GRUNNLAG_ROI"
    GRUNNLAG_LABEL = "GRUNNLAG_LABEL"
    GRUNNLAG_FEATURE = "GRUNNLAG_FEATURE"
    BORD_TABLE = "BORD_TABLE"
    BORD_GRAPH = "BORD_GRAPH"
    PLOTQL_PLOT = "PLOTQL_PLOT"


class OmeroFileType(str, Enum):
    """An enumeration."""

    TIFF = "TIFF"
    "Tiff"
    JPEG = "JPEG"
    "Jpeg"
    MSR = "MSR"
    "MSR File"
    CZI = "CZI"
    "Zeiss Microscopy File"
    UNKNOWN = "UNKNOWN"
    "Unwknon File Format"


class RepresentationVarietyInput(str, Enum):
    """Variety expresses the Type of Representation we are dealing with"""

    MASK = "MASK"
    "Mask (Value represent Labels)"
    VOXEL = "VOXEL"
    "Voxel (Value represent Intensity)"
    RGB = "RGB"
    "RGB (First three channel represent RGB)"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class PandasDType(str, Enum):
    OBJECT = "OBJECT"
    INT64 = "INT64"
    FLOAT64 = "FLOAT64"
    BOOL = "BOOL"
    CATEGORY = "CATEGORY"
    DATETIME65 = "DATETIME65"
    TIMEDELTA = "TIMEDELTA"
    UNICODE = "UNICODE"
    DATETIME = "DATETIME"
    DATETIMEZ = "DATETIMEZ"
    DATETIMETZ = "DATETIMETZ"
    DATETIME64 = "DATETIME64"
    DATETIME64TZ = "DATETIME64TZ"
    DATETIME64NS = "DATETIME64NS"
    DATETIME64NSUTC = "DATETIME64NSUTC"
    DATETIME64NSZ = "DATETIME64NSZ"
    DATETIME64NSZUTC = "DATETIME64NSZUTC"


class ROIType(str, Enum):
    """An enumeration."""

    ELLIPSE = "ELLIPSE"
    "Ellipse"
    POLYGON = "POLYGON"
    "POLYGON"
    LINE = "LINE"
    "Line"
    RECTANGLE = "RECTANGLE"
    "Rectangle"
    PATH = "PATH"
    "Path"
    UNKNOWN = "UNKNOWN"
    "Unknown"
    FRAME = "FRAME"
    "Frame"
    SLICE = "SLICE"
    "Slice"
    POINT = "POINT"
    "Point"


class Dimension(str, Enum):
    """The dimension of the data"""

    X = "X"
    Y = "Y"
    Z = "Z"
    T = "T"
    C = "C"


class Medium(str, Enum):
    """The medium of the imaging environment

    Important for the objective settings"""

    AIR = "AIR"
    GLYCEROL = "GLYCEROL"
    OIL = "OIL"
    OTHER = "OTHER"
    WATER = "WATER"


class RoiTypeInput(str, Enum):
    """An enumeration."""

    ELLIPSIS = "ELLIPSIS"
    "Ellipse"
    POLYGON = "POLYGON"
    "POLYGON"
    LINE = "LINE"
    "Line"
    RECTANGLE = "RECTANGLE"
    "Rectangle"
    PATH = "PATH"
    "Path"
    UNKNOWN = "UNKNOWN"
    "Unknown"
    FRAME = "FRAME"
    "Frame"
    SLICE = "SLICE"
    "Slice"
    POINT = "POINT"
    "Point"


class RepresentationVariety(str, Enum):
    """An enumeration."""

    MASK = "MASK"
    "Mask (Value represent Labels)"
    VOXEL = "VOXEL"
    "Voxel (Value represent Intensity)"
    RGB = "RGB"
    "RGB (First three channel represent RGB)"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class ModelKind(str, Enum):
    """What format is the model in?"""

    ONNX = "ONNX"
    TENSORFLOW = "TENSORFLOW"
    PYTORCH = "PYTORCH"
    UNKNOWN = "UNKNOWN"


class AcquisitionKind(str, Enum):
    """What do the multiple positions in this acquistion represent?"""

    POSTION_IS_SAMPLE = "POSTION_IS_SAMPLE"
    POSITION_IS_ROI = "POSITION_IS_ROI"
    UNKNOWN = "UNKNOWN"


class DescendendInput(BaseModel):
    children: Optional[Tuple[Optional["DescendendInput"], ...]]
    typename: Optional[str]
    "The type of the descendent"
    user: Optional[str]
    "The user that is mentioned"
    bold: Optional[bool]
    "Is this a bold leaf?"
    italic: Optional[bool]
    "Is this a italic leaf?"
    code: Optional[bool]
    "Is this a code leaf?"
    text: Optional[str]
    "The text of the leaf"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class GroupAssignmentInput(BaseModel):
    permissions: Tuple[Optional[str], ...]
    group: ID

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class UserAssignmentInput(BaseModel):
    permissions: Tuple[Optional[str], ...]
    user: str
    "The user id"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class OmeroRepresentationInput(BaseModel):
    """The Omero Meta Data of an Image

    Follows closely the omexml model. With a few alterations:
    - The data model of the datasets and experimenters is
    part of the mikro datamodel and are not accessed here.
    - Some parameters are ommited as they are not really used"""

    planes: Optional[Tuple[Optional["PlaneInput"], ...]]
    maps: Optional[Tuple[Optional[ID], ...]]
    timepoints: Optional[Tuple[Optional[ID], ...]]
    channels: Optional[Tuple[Optional["ChannelInput"], ...]]
    physical_size: Optional["PhysicalSizeInput"] = Field(alias="physicalSize")
    affine_transformation: Optional[AffineMatrix] = Field(alias="affineTransformation")
    scale: Optional[Tuple[Optional[float], ...]]
    positions: Optional[Tuple[Optional[ID], ...]]
    cameras: Optional[Tuple[Optional[ID], ...]]
    acquisition_date: Optional[datetime] = Field(alias="acquisitionDate")
    objective_settings: Optional["ObjectiveSettingsInput"] = Field(
        alias="objectiveSettings"
    )
    imaging_environment: Optional["ImagingEnvironmentInput"] = Field(
        alias="imagingEnvironment"
    )
    instrument: Optional[ID]
    objective: Optional[ID]

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class PlaneInput(BaseModel):
    """ " A plane in an image

    Plane follows the convention of the OME model, where the first index is the
    Z axis, the second is the Y axis, the third is the X axis, the fourth is the
    C axis, and the fifth is the T axis.

    It attached the image at the indicated index to the image and gives information
    about the plane (e.g. exposure time, delta t to the origin, etc.)"""

    z: Optional[int]
    "Z index of the plane"
    y: Optional[int]
    "Y index of the plane"
    x: Optional[int]
    "X index of the plane"
    c: Optional[int]
    "C index of the plane"
    t: Optional[int]
    "Z index of the plane"
    position_x: Optional[float] = Field(alias="positionX")
    "The planes X position on the stage of the microscope"
    position_y: Optional[float] = Field(alias="positionY")
    "The planes Y position on the stage of the microscope"
    position_z: Optional[float] = Field(alias="positionZ")
    "The planes Z position on the stage of the microscope"
    exposure_time: Optional[float] = Field(alias="exposureTime")
    "The exposure time of the plane (e.g. Laser exposure)"
    delta_t: Optional[float] = Field(alias="deltaT")
    "The Delta T to the origin of the image acqusition"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class ChannelInput(BaseModel):
    """A channel in an image

    Channels can be highly variable in their properties. This class is a
    representation of the most common properties of a channel."""

    name: Optional[str]
    "The name of the channel"
    emmission_wavelength: Optional[float] = Field(alias="emmissionWavelength")
    "The emmission wavelength of the fluorophore in nm"
    excitation_wavelength: Optional[float] = Field(alias="excitationWavelength")
    "The excitation wavelength of the fluorophore in nm"
    acquisition_mode: Optional[str] = Field(alias="acquisitionMode")
    "The acquisition mode of the channel"
    color: Optional[str]
    "The default color for the channel (might be ommited by the rendered)"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class PhysicalSizeInput(BaseModel):
    """Physical size of the image

    Each dimensions of the image has a physical size. This is the size of the
    pixel in the image. The physical size is given in micrometers on a PIXEL
    basis. This means that the physical size of the image is the size of the
    pixel in the image * the number of pixels in the image. For example, if
    the image is 1000x1000 pixels and the physical size of the image is 3 (x params) x 3 (y params),
    micrometer, the physical size of the image is 3000x3000 micrometer. If the image

    The t dimension is given in ms, since the time is given in ms.
    The C dimension is given in nm, since the wavelength is given in nm."""

    x: Optional[float]
    "Physical size of *one* Pixel in the x dimension (in µm)"
    y: Optional[float]
    "Physical size of *one* Pixel in the t dimension (in µm)"
    z: Optional[float]
    "Physical size of *one* Pixel in the z dimension (in µm)"
    t: Optional[float]
    "Physical size of *one* Pixel in the t dimension (in ms)"
    c: Optional[float]
    "Physical size of *one* Pixel in the c dimension (in nm)"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class ObjectiveSettingsInput(BaseModel):
    """Settings of the objective used to acquire the image

    Follows the OME model for objective settings"""

    correction_collar: Optional[float] = Field(alias="correctionCollar")
    "The correction collar of the objective"
    medium: Optional[Medium]
    "The medium of the objective"
    numerical_aperture: Optional[float] = Field(alias="numericalAperture")
    "The numerical aperture of the objective"
    working_distance: Optional[float] = Field(alias="workingDistance")
    "The working distance of the objective"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class ImagingEnvironmentInput(BaseModel):
    """The imaging environment during the acquisition

    Follows the OME model for imaging environment"""

    air_pressure: Optional[float] = Field(alias="airPressure")
    "The air pressure during the acquisition"
    co2_percent: Optional[float] = Field(alias="co2Percent")
    "The CO2 percentage in the environment"
    humidity: Optional[float]
    "The humidity of the imaging environment"
    temperature: Optional[float]
    "The temperature of the imaging environment"
    map: Optional[Dict]
    "A map of the imaging environment. Key value based"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class RepresentationViewInput(BaseModel):
    z_min: Optional[int] = Field(alias="zMin")
    "The x coord of the position (relative to origin)"
    z_max: Optional[int] = Field(alias="zMax")
    "The x coord of the position (relative to origin)"
    t_min: Optional[int] = Field(alias="tMin")
    "The x coord of the position (relative to origin)"
    t_max: Optional[int] = Field(alias="tMax")
    "The x coord of the position (relative to origin)"
    c_min: Optional[int] = Field(alias="cMin")
    "The x coord of the position (relative to origin)"
    c_max: Optional[int] = Field(alias="cMax")
    "The x coord of the position (relative to origin)"
    x_min: Optional[int] = Field(alias="xMin")
    "The x coord of the position (relative to origin)"
    x_max: Optional[int] = Field(alias="xMax")
    "The x coord of the position (relative to origin)"
    y_min: Optional[int] = Field(alias="yMin")
    "The x coord of the position (relative to origin)"
    y_max: Optional[int] = Field(alias="yMax")
    "The x coord of the position (relative to origin)"
    channel: Optional[ID]
    "The channel you want to associate with this map"
    position: Optional[ID]
    "The position you want to associate with this map"
    timepoint: Optional[ID]
    "The position you want to associate with this map"
    created_while: Optional[AssignationID] = Field(alias="createdWhile")
    "The assignation id"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class InputVector(Vectorizable, BaseModel):
    x: Optional[float]
    "X-coordinate"
    y: Optional[float]
    "Y-coordinate"
    z: Optional[float]
    "Z-coordinate"
    c: Optional[float]
    "C-coordinate"
    t: Optional[float]
    "T-coordinate"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class ViewInput(BaseModel):
    omero: ID
    "The stage this position belongs to"
    z_min: Optional[int] = Field(alias="zMin")
    "The x coord of the position (relative to origin)"
    z_max: Optional[int] = Field(alias="zMax")
    "The x coord of the position (relative to origin)"
    t_min: Optional[int] = Field(alias="tMin")
    "The x coord of the position (relative to origin)"
    t_max: Optional[int] = Field(alias="tMax")
    "The x coord of the position (relative to origin)"
    c_min: Optional[int] = Field(alias="cMin")
    "The x coord of the position (relative to origin)"
    c_max: Optional[int] = Field(alias="cMax")
    "The x coord of the position (relative to origin)"
    x_min: Optional[int] = Field(alias="xMin")
    "The x coord of the position (relative to origin)"
    x_max: Optional[int] = Field(alias="xMax")
    "The x coord of the position (relative to origin)"
    y_min: Optional[int] = Field(alias="yMin")
    "The x coord of the position (relative to origin)"
    y_max: Optional[int] = Field(alias="yMax")
    "The x coord of the position (relative to origin)"
    channel: Optional[ID]
    "The channel you want to associate with this map"
    position: Optional[ID]
    "The position you want to associate with this map"
    timepoint: Optional[ID]
    "The position you want to associate with this map"
    created_while: Optional[AssignationID] = Field(alias="createdWhile")
    "The assignation id"

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class ExportStageFragmentPositionsOmerosTimepointsEra(BaseModel):
    """Era(id, created_by, created_through, created_while, name, start, end, created_at)"""

    typename: Optional[Literal["Era"]] = Field(alias="__typename", exclude=True)
    name: str
    "The name of the era"

    class Config:
        frozen = True


class ExportStageFragmentPositionsOmerosTimepoints(BaseModel):
    """The relative position of a sample on a microscope stage"""

    typename: Optional[Literal["Timepoint"]] = Field(alias="__typename", exclude=True)
    era: ExportStageFragmentPositionsOmerosTimepointsEra
    delta_t: Optional[float] = Field(alias="deltaT")

    class Config:
        frozen = True


class ExportStageFragmentPositionsOmerosRepresentationFileorigins(BaseModel):
    typename: Optional[Literal["OmeroFile"]] = Field(alias="__typename", exclude=True)
    id: ID
    file: Optional[File]
    " the associaed file"

    class Config:
        frozen = True


class ExportStageFragmentPositionsOmerosRepresentationDerivedMetrics(BaseModel):
    typename: Optional[Literal["Metric"]] = Field(alias="__typename", exclude=True)
    id: ID
    key: str
    "The Key"
    value: Optional[MetricValue]
    "Value"

    class Config:
        frozen = True


class ExportStageFragmentPositionsOmerosRepresentationDerived(
    Representation, BaseModel
):
    """A Representation is 5-dimensional representation of an image

    Mikro stores each image as sa 5-dimensional representation. The dimensions are:
    - t: time
    - c: channel
    - z: z-stack
    - x: x-dimension
    - y: y-dimension

    This ensures a unified api for all images, regardless of their original dimensions. Another main
    determining factor for a representation is its variety:
    A representation can be a raw image representating voxels (VOXEL)
    or a segmentation mask representing instances of a class. (MASK)
    It can also representate a human perception of the image (RGB) or a human perception of the mask (RGBMASK)

    # Meta

    Meta information is stored in the omero field which gives access to the omero-meta data. Refer to the omero documentation for more information.


    #Origins and Derivations

    Images can be filtered, which means that a new representation is created from the other (original) representations. This new representation is then linked to the original representations. This way, we can always trace back to the original representation.
    Both are encapsulaed in the origins and derived fields.

    Representations belong to *one* sample. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    Each iamge has also a name, which is used to identify the image. The name is unique within a sample.
    File and Rois that are used to create images are saved in the file origins and roi origins repectively.


    """

    typename: Optional[Literal["Representation"]] = Field(
        alias="__typename", exclude=True
    )
    id: ID
    store: Optional[Store]
    name: Optional[str]
    "Cleartext name"
    metrics: Optional[
        Tuple[
            Optional[ExportStageFragmentPositionsOmerosRepresentationDerivedMetrics],
            ...,
        ]
    ]
    "Associated metrics of this Imasge"

    class Config:
        frozen = True


class ExportStageFragmentPositionsOmerosRepresentation(Representation, BaseModel):
    """A Representation is 5-dimensional representation of an image

    Mikro stores each image as sa 5-dimensional representation. The dimensions are:
    - t: time
    - c: channel
    - z: z-stack
    - x: x-dimension
    - y: y-dimension

    This ensures a unified api for all images, regardless of their original dimensions. Another main
    determining factor for a representation is its variety:
    A representation can be a raw image representating voxels (VOXEL)
    or a segmentation mask representing instances of a class. (MASK)
    It can also representate a human perception of the image (RGB) or a human perception of the mask (RGBMASK)

    # Meta

    Meta information is stored in the omero field which gives access to the omero-meta data. Refer to the omero documentation for more information.


    #Origins and Derivations

    Images can be filtered, which means that a new representation is created from the other (original) representations. This new representation is then linked to the original representations. This way, we can always trace back to the original representation.
    Both are encapsulaed in the origins and derived fields.

    Representations belong to *one* sample. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    Each iamge has also a name, which is used to identify the image. The name is unique within a sample.
    File and Rois that are used to create images are saved in the file origins and roi origins repectively.


    """

    typename: Optional[Literal["Representation"]] = Field(
        alias="__typename", exclude=True
    )
    store: Optional[Store]
    name: Optional[str]
    "Cleartext name"
    id: ID
    file_origins: Tuple[
        ExportStageFragmentPositionsOmerosRepresentationFileorigins, ...
    ] = Field(alias="fileOrigins")
    derived: Optional[
        Tuple[Optional[ExportStageFragmentPositionsOmerosRepresentationDerived], ...]
    ]
    "Derived Images from this Image"

    class Config:
        frozen = True


class ExportStageFragmentPositionsOmeros(Omero, BaseModel):
    """Omero is a through model that stores the real world context of an image

    This means that it stores the position (corresponding to the relative displacement to
    a stage (Both are models)), objective and other meta data of the image.

    """

    typename: Optional[Literal["Omero"]] = Field(alias="__typename", exclude=True)
    timepoints: Optional[
        Tuple[Optional[ExportStageFragmentPositionsOmerosTimepoints], ...]
    ]
    "Associated Timepoints"
    acquisition_date: Optional[datetime] = Field(alias="acquisitionDate")
    representation: ExportStageFragmentPositionsOmerosRepresentation

    class Config:
        frozen = True


class ExportStageFragmentPositions(Position, BaseModel):
    """The relative position of a sample on a microscope stage"""

    typename: Optional[Literal["Position"]] = Field(alias="__typename", exclude=True)
    name: str
    "The name of the possition"
    id: ID
    x: float
    "pixelSize for x in microns"
    z: float
    "pixelSize for z in microns"
    y: float
    "pixelSize for y in microns"
    omeros: Optional[Tuple[Optional[ExportStageFragmentPositionsOmeros], ...]]
    "Associated images through Omero"

    class Config:
        frozen = True


class ExportStageFragment(Stage, BaseModel):
    typename: Optional[Literal["Stage"]] = Field(alias="__typename", exclude=True)
    name: str
    "The name of the stage"
    positions: Optional[Tuple[Optional[ExportStageFragmentPositions], ...]]
    "Derived Images from this Image"

    class Config:
        frozen = True


class ExportDatasetFragmentOmerofiles(BaseModel):
    typename: Optional[Literal["OmeroFile"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    "The name of the file"
    type: OmeroFileType
    "The type of the file"
    file: Optional[File]
    " the associaed file"

    class Config:
        frozen = True


class ExportDatasetFragment(BaseModel):
    typename: Optional[Literal["Dataset"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    "The name of the experiment"
    omerofiles: Tuple[ExportDatasetFragmentOmerofiles, ...]

    class Config:
        frozen = True


class ExportRepresentationFragmentFileorigins(BaseModel):
    typename: Optional[Literal["OmeroFile"]] = Field(alias="__typename", exclude=True)
    name: str
    "The name of the file"
    created_at: datetime = Field(alias="createdAt")
    "The time the file was created"

    class Config:
        frozen = True


class ExportRepresentationFragmentOmeroPhysicalsize(PhysicalSize, BaseModel):
    """Physical size of the image

    Each dimensions of the image has a physical size. This is the size of the
    pixel in the image. The physical size is given in micrometers on a PIXEL
    basis. This means that the physical size of the image is the size of the
    pixel in the image * the number of pixels in the image. For example, if
    the image is 1000x1000 pixels and the physical size of the image is 3 (x params) x 3 (y params),
    micrometer, the physical size of the image is 3000x3000 micrometer. If the image

    The t dimension is given in ms, since the time is given in ms.
    The C dimension is given in nm, since the wavelength is given in nm."""

    typename: Optional[Literal["PhysicalSize"]] = Field(
        alias="__typename", exclude=True
    )
    x: Optional[float]
    "Physical size of *one* Pixel in the x dimension (in µm)"
    y: Optional[float]
    "Physical size of *one* Pixel in the t dimension (in µm)"
    z: Optional[float]
    "Physical size of *one* Pixel in the z dimension (in µm)"
    t: Optional[float]
    "Physical size of *one* Pixel in the t dimension (in ms)"
    c: Optional[float]
    "Physical size of *one* Pixel in the c dimension (in µm)"

    class Config:
        frozen = True


class ExportRepresentationFragmentOmeroTimepoints(BaseModel):
    """The relative position of a sample on a microscope stage"""

    typename: Optional[Literal["Timepoint"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        frozen = True


class ExportRepresentationFragmentOmero(Omero, BaseModel):
    """Omero is a through model that stores the real world context of an image

    This means that it stores the position (corresponding to the relative displacement to
    a stage (Both are models)), objective and other meta data of the image.

    """

    typename: Optional[Literal["Omero"]] = Field(alias="__typename", exclude=True)
    id: ID
    physical_size: Optional[ExportRepresentationFragmentOmeroPhysicalsize] = Field(
        alias="physicalSize"
    )
    timepoints: Optional[
        Tuple[Optional[ExportRepresentationFragmentOmeroTimepoints], ...]
    ]
    "Associated Timepoints"

    class Config:
        frozen = True


class ExportRepresentationFragmentRoisComments(BaseModel):
    """A comment

    A comment is a user generated comment on a commentable object. A comment can be a reply to another comment or a top level comment.
    Comments can be nested to any depth. A comment can be edited and deleted by the user that created it.
    """

    typename: Optional[Literal["Comment"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        frozen = True


class ExportRepresentationFragmentRoisCreator(BaseModel):
    """User

    This object represents a user in the system. Users are used to
    control access to different parts of the system. Users are assigned
    to groups. A user has access to a part of the system if the user is
    a member of a group that has the permission assigned to it.

    Users can be be "creator" of objects. This means that the user has
    created the object. This is used to control access to objects. A user
    can only access objects that they have created, or objects that they
    have access to through a group that they are a member of.

    See the documentation for "Object Level Permissions" for more information."""

    typename: Optional[Literal["User"]] = Field(alias="__typename", exclude=True)
    sub: Optional[str]

    class Config:
        frozen = True


class ExportRepresentationFragmentRoisVectors(BaseModel):
    typename: Optional[Literal["Vector"]] = Field(alias="__typename", exclude=True)
    x: Optional[float]
    "X-coordinate"
    y: Optional[float]
    "Y-coordinate"
    z: Optional[float]
    "Z-coordinate"
    t: Optional[float]
    "T-coordinate"
    c: Optional[float]
    "C-coordinate"

    class Config:
        frozen = True


class ExportRepresentationFragmentRoisDerivedrepresentationsMetrics(BaseModel):
    typename: Optional[Literal["Metric"]] = Field(alias="__typename", exclude=True)
    key: str
    "The Key"
    value: Optional[MetricValue]
    "Value"

    class Config:
        frozen = True


class ExportRepresentationFragmentRoisDerivedrepresentationsDerivedMetrics(BaseModel):
    typename: Optional[Literal["Metric"]] = Field(alias="__typename", exclude=True)
    key: str
    "The Key"
    value: Optional[MetricValue]
    "Value"

    class Config:
        frozen = True


class ExportRepresentationFragmentRoisDerivedrepresentationsDerivedTables(
    Table, BaseModel
):
    """A Table is a collection of tabular data.

    It provides a way to store data in a tabular format and associate it with a Representation,
    Sample or Experiment. It is a way to store data that might be to large to store in a
    Feature or Metric on this Experiments. Or it might be data that is not easily represented
    as a Feature or Metric.

    Tables can be easily created from a pandas DataFrame and can be converted to a pandas DataFrame.
    Its columns are defined by the columns of the DataFrame.


    """

    typename: Optional[Literal["Table"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    store: Optional[Parquet]
    "The parquet store for the table"

    class Config:
        frozen = True


class ExportRepresentationFragmentRoisDerivedrepresentationsDerived(
    Representation, BaseModel
):
    """A Representation is 5-dimensional representation of an image

    Mikro stores each image as sa 5-dimensional representation. The dimensions are:
    - t: time
    - c: channel
    - z: z-stack
    - x: x-dimension
    - y: y-dimension

    This ensures a unified api for all images, regardless of their original dimensions. Another main
    determining factor for a representation is its variety:
    A representation can be a raw image representating voxels (VOXEL)
    or a segmentation mask representing instances of a class. (MASK)
    It can also representate a human perception of the image (RGB) or a human perception of the mask (RGBMASK)

    # Meta

    Meta information is stored in the omero field which gives access to the omero-meta data. Refer to the omero documentation for more information.


    #Origins and Derivations

    Images can be filtered, which means that a new representation is created from the other (original) representations. This new representation is then linked to the original representations. This way, we can always trace back to the original representation.
    Both are encapsulaed in the origins and derived fields.

    Representations belong to *one* sample. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    Each iamge has also a name, which is used to identify the image. The name is unique within a sample.
    File and Rois that are used to create images are saved in the file origins and roi origins repectively.


    """

    typename: Optional[Literal["Representation"]] = Field(
        alias="__typename", exclude=True
    )
    id: ID
    name: Optional[str]
    "Cleartext name"
    store: Optional[Store]
    metrics: Optional[
        Tuple[
            Optional[
                ExportRepresentationFragmentRoisDerivedrepresentationsDerivedMetrics
            ],
            ...,
        ]
    ]
    "Associated metrics of this Imasge"
    tables: Optional[
        Tuple[
            Optional[
                ExportRepresentationFragmentRoisDerivedrepresentationsDerivedTables
            ],
            ...,
        ]
    ]
    "Associated tables"

    class Config:
        frozen = True


class ExportRepresentationFragmentRoisDerivedrepresentations(Representation, BaseModel):
    """A Representation is 5-dimensional representation of an image

    Mikro stores each image as sa 5-dimensional representation. The dimensions are:
    - t: time
    - c: channel
    - z: z-stack
    - x: x-dimension
    - y: y-dimension

    This ensures a unified api for all images, regardless of their original dimensions. Another main
    determining factor for a representation is its variety:
    A representation can be a raw image representating voxels (VOXEL)
    or a segmentation mask representing instances of a class. (MASK)
    It can also representate a human perception of the image (RGB) or a human perception of the mask (RGBMASK)

    # Meta

    Meta information is stored in the omero field which gives access to the omero-meta data. Refer to the omero documentation for more information.


    #Origins and Derivations

    Images can be filtered, which means that a new representation is created from the other (original) representations. This new representation is then linked to the original representations. This way, we can always trace back to the original representation.
    Both are encapsulaed in the origins and derived fields.

    Representations belong to *one* sample. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    Each iamge has also a name, which is used to identify the image. The name is unique within a sample.
    File and Rois that are used to create images are saved in the file origins and roi origins repectively.


    """

    typename: Optional[Literal["Representation"]] = Field(
        alias="__typename", exclude=True
    )
    id: ID
    name: Optional[str]
    "Cleartext name"
    store: Optional[Store]
    metrics: Optional[
        Tuple[
            Optional[ExportRepresentationFragmentRoisDerivedrepresentationsMetrics], ...
        ]
    ]
    "Associated metrics of this Imasge"
    derived: Optional[
        Tuple[
            Optional[ExportRepresentationFragmentRoisDerivedrepresentationsDerived], ...
        ]
    ]
    "Derived Images from this Image"

    class Config:
        frozen = True


class ExportRepresentationFragmentRois(ROI, BaseModel):
    """A ROI is a region of interest in a representation.

    This region is to be regarded as a view on the representation. Depending
    on the implementatoin (type) of the ROI, the view can be constructed
    differently. For example, a rectangular ROI can be constructed by cropping
    the representation according to its 2 vectors. while a polygonal ROI can be constructed by masking the
    representation with the polygon.

    The ROI can also store a name and a description. This is used to display the ROI in the UI.

    """

    typename: Optional[Literal["ROI"]] = Field(alias="__typename", exclude=True)
    id: ID
    comments: Optional[Tuple[Optional[ExportRepresentationFragmentRoisComments], ...]]
    creator: ExportRepresentationFragmentRoisCreator
    "The user that created the ROI"
    vectors: Optional[Tuple[Optional[ExportRepresentationFragmentRoisVectors], ...]]
    "The vectors of the ROI"
    type: ROIType
    "The Roi can have varying types, consult your API"
    derived_representations: Tuple[
        ExportRepresentationFragmentRoisDerivedrepresentations, ...
    ] = Field(alias="derivedRepresentations")

    class Config:
        frozen = True


class ExportRepresentationFragment(Representation, BaseModel):
    typename: Optional[Literal["Representation"]] = Field(
        alias="__typename", exclude=True
    )
    file_origins: Tuple[ExportRepresentationFragmentFileorigins, ...] = Field(
        alias="fileOrigins"
    )
    id: ID
    name: Optional[str]
    "Cleartext name"
    omero: Optional[ExportRepresentationFragmentOmero]
    rois: Optional[Tuple[Optional[ExportRepresentationFragmentRois], ...]]
    "Associated rois"
    store: Optional[Store]

    class Config:
        frozen = True


class GetExportStageQuery(BaseModel):
    stage: Optional[ExportStageFragment]
    'Get a single experiment by ID"\n    \n    Returns a single experiment by ID. If the user does not have access\n    to the experiment, an error will be raised.\n    \n    '

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ExportStage on Stage {\n  name\n  positions {\n    name\n    id\n    x\n    z\n    y\n    omeros {\n      timepoints {\n        era {\n          name\n        }\n        deltaT\n      }\n      acquisitionDate\n      representation {\n        store\n        name\n        id\n        fileOrigins {\n          id\n          file\n        }\n        derived(flatten: 4) {\n          id\n          store\n          name\n          metrics {\n            id\n            key\n            value\n          }\n        }\n      }\n    }\n  }\n}\n\nquery GetExportStage($id: ID!) {\n  stage(id: $id) {\n    ...ExportStage\n  }\n}"


class GetExportDatasetQuery(BaseModel):
    dataset: Optional[ExportDatasetFragment]
    'Get a single experiment by ID"\n    \n    Returns a single experiment by ID. If the user does not have access\n    to the experiment, an error will be raised.\n    \n    '

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ExportDataset on Dataset {\n  id\n  name\n  omerofiles {\n    id\n    name\n    type\n    file\n  }\n}\n\nquery GetExportDataset($id: ID!) {\n  dataset(id: $id) {\n    ...ExportDataset\n  }\n}"


class GetExportRepresentationQuery(BaseModel):
    representation: Optional[ExportRepresentationFragment]
    "Get a single Representation by ID\n\n    Returns a single Representation by ID. If the user does not have access\n    to the Representation, an error will be raised.\n    "

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ExportRepresentation on Representation {\n  fileOrigins {\n    name\n    createdAt\n  }\n  id\n  name\n  omero {\n    id\n    physicalSize {\n      x\n      y\n      z\n      t\n      c\n    }\n    timepoints {\n      id\n    }\n  }\n  rois {\n    id\n    comments {\n      id\n    }\n    creator {\n      sub\n    }\n    vectors {\n      x\n      y\n      z\n      t\n      c\n    }\n    type\n    derivedRepresentations {\n      id\n      name\n      store\n      metrics {\n        key\n        value\n      }\n      derived(flatten: 3) {\n        id\n        name\n        store\n        metrics {\n          key\n          value\n        }\n        tables {\n          id\n          name\n          store\n        }\n      }\n    }\n  }\n  store\n}\n\nquery GetExportRepresentation($id: ID!) {\n  representation(id: $id) {\n    ...ExportRepresentation\n  }\n}"


async def aget_export_stage(
    id: ID, rath: MikroRath = None
) -> Optional[ExportStageFragment]:
    """GetExportStage


     stage: An Stage is a set of positions that share a common space on a microscope and can
        be use to translate.





    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[ExportStageFragment]"""
    return (await aexecute(GetExportStageQuery, {"id": id}, rath=rath)).stage


def get_export_stage(id: ID, rath: MikroRath = None) -> Optional[ExportStageFragment]:
    """GetExportStage


     stage: An Stage is a set of positions that share a common space on a microscope and can
        be use to translate.





    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[ExportStageFragment]"""
    return execute(GetExportStageQuery, {"id": id}, rath=rath).stage


async def aget_export_dataset(
    id: ID, rath: MikroRath = None
) -> Optional[ExportDatasetFragment]:
    """GetExportDataset


     dataset:
        A dataset is a collection of data files and metadata files.
        It mimics the concept of a folder in a file system and is the top level
        object in the data model.




    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[ExportDatasetFragment]"""
    return (await aexecute(GetExportDatasetQuery, {"id": id}, rath=rath)).dataset


def get_export_dataset(
    id: ID, rath: MikroRath = None
) -> Optional[ExportDatasetFragment]:
    """GetExportDataset


     dataset:
        A dataset is a collection of data files and metadata files.
        It mimics the concept of a folder in a file system and is the top level
        object in the data model.




    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[ExportDatasetFragment]"""
    return execute(GetExportDatasetQuery, {"id": id}, rath=rath).dataset


async def aget_export_representation(
    id: ID, rath: MikroRath = None
) -> Optional[ExportRepresentationFragment]:
    """GetExportRepresentation


     representation: A Representation is 5-dimensional representation of an image

        Mikro stores each image as sa 5-dimensional representation. The dimensions are:
        - t: time
        - c: channel
        - z: z-stack
        - x: x-dimension
        - y: y-dimension

        This ensures a unified api for all images, regardless of their original dimensions. Another main
        determining factor for a representation is its variety:
        A representation can be a raw image representating voxels (VOXEL)
        or a segmentation mask representing instances of a class. (MASK)
        It can also representate a human perception of the image (RGB) or a human perception of the mask (RGBMASK)

        # Meta

        Meta information is stored in the omero field which gives access to the omero-meta data. Refer to the omero documentation for more information.


        #Origins and Derivations

        Images can be filtered, which means that a new representation is created from the other (original) representations. This new representation is then linked to the original representations. This way, we can always trace back to the original representation.
        Both are encapsulaed in the origins and derived fields.

        Representations belong to *one* sample. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
        Each iamge has also a name, which is used to identify the image. The name is unique within a sample.
        File and Rois that are used to create images are saved in the file origins and roi origins repectively.





    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[ExportRepresentationFragment]"""
    return (
        await aexecute(GetExportRepresentationQuery, {"id": id}, rath=rath)
    ).representation


def get_export_representation(
    id: ID, rath: MikroRath = None
) -> Optional[ExportRepresentationFragment]:
    """GetExportRepresentation


     representation: A Representation is 5-dimensional representation of an image

        Mikro stores each image as sa 5-dimensional representation. The dimensions are:
        - t: time
        - c: channel
        - z: z-stack
        - x: x-dimension
        - y: y-dimension

        This ensures a unified api for all images, regardless of their original dimensions. Another main
        determining factor for a representation is its variety:
        A representation can be a raw image representating voxels (VOXEL)
        or a segmentation mask representing instances of a class. (MASK)
        It can also representate a human perception of the image (RGB) or a human perception of the mask (RGBMASK)

        # Meta

        Meta information is stored in the omero field which gives access to the omero-meta data. Refer to the omero documentation for more information.


        #Origins and Derivations

        Images can be filtered, which means that a new representation is created from the other (original) representations. This new representation is then linked to the original representations. This way, we can always trace back to the original representation.
        Both are encapsulaed in the origins and derived fields.

        Representations belong to *one* sample. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
        Each iamge has also a name, which is used to identify the image. The name is unique within a sample.
        File and Rois that are used to create images are saved in the file origins and roi origins repectively.





    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[ExportRepresentationFragment]"""
    return execute(GetExportRepresentationQuery, {"id": id}, rath=rath).representation


DescendendInput.update_forward_refs()
OmeroRepresentationInput.update_forward_refs()
