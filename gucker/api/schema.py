from rath.scalars import ID
from mikro.funcs import execute, aexecute
from mikro.traits import Position, Representation, Omero, Stage
from enum import Enum
from mikro.scalars import Store, File
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Literal, Tuple
from mikro.rath import MikroRath


class ExportStageFragmentPositionsOmerosRepresentationFileorigins(BaseModel):
    typename: Optional[Literal["OmeroFile"]] = Field(alias="__typename", exclude=True)
    id: ID
    file: Optional[File]
    "The file"

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
    omeros: Optional[Tuple[Optional[ExportStageFragmentPositionsOmeros], ...]]
    "Associated images through Omero"

    class Config:
        frozen = True


class ExportStageFragment(Stage, BaseModel):
    typename: Optional[Literal["Stage"]] = Field(alias="__typename", exclude=True)
    name: str
    "The name of the stage"
    positions: Tuple[ExportStageFragmentPositions, ...]

    class Config:
        frozen = True


class GetExportStageQuery(BaseModel):
    stage: Optional[ExportStageFragment]
    'Get a single experiment by ID"\n    \n    Returns a single experiment by ID. If the user does not have access\n    to the experiment, an error will be raised.\n    \n    '

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ExportStage on Stage {\n  name\n  positions {\n    name\n    id\n    omeros {\n      acquisitionDate\n      representation {\n        store\n        name\n        id\n        fileOrigins {\n          id\n          file\n        }\n        derived(flatten: 4) {\n          id\n          store\n          name\n        }\n      }\n    }\n  }\n}\n\nquery GetExportStage($id: ID!) {\n  stage(id: $id) {\n    ...ExportStage\n  }\n}"


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
