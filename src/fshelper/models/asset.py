from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, create_model


class TypeField(BaseModel):
    """Model for the type_fields field of an asset.
    This model will contain custom fields that vary by account.
    """
    class Config:
        extra = Extra.allow


class AssetCreation(BaseModel):
    """Model for the data necessary to create an asset through the FreshService api.

    https://api.freshservice.com/#asset_attributes
    type_fields will be a dict, but the keys will be different from account to account.  They include an
    identifier in the key that seems to be related to the account but generated when custom fields are
    added.  Therefore, it's not defined with a separate model because we can't know the identifier
    beforehand.
    """

    name: str
    """Mandatory field"""
    asset_type_id: int
    """Mandatory field"""
    description: Optional[str] = None
    impact: Optional[str] = None
    usage_type: Optional[str] = None
    asset_tag: Optional[str] = None
    user_id: Optional[int] = None
    department_id: Optional[int] = None
    location_id: Optional[int] = None
    agent_id: Optional[int] = None
    group_id: Optional[int] = None
    type_fields: Optional[TypeField] = None
    """Dynamic data specific to each FS account."""


class AssetUpdate(AssetCreation):
    """Model for the data used to update a FS asset through the API.
    These additional fields would be created dynamically by FS when left out of the data to create an asset through
    the API.
    """
    id: Optional[int] = None
    display_id: Optional[int] = None


class AssetFullData(AssetUpdate):
    """Model for the full data set of a FreshService asset in the FS API.
    This class includes the additional read-only fields that wouldn't be set when creating or updating an asset through
    the API.
    """
    author_type: Optional[str] = None
    assigned_on: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


def __create_type_field_model(*args, **kwargs) -> TypeField:
    """Dynamically create a TypeField model.

    :param __model_name: name of the created model
    :param __config__: config class to use for the new model
    :param __base__: base class for the new model to inherit from
    :param __module__: module of the created model
    :param __validators__: a dict of method names and @validator class methods
    :param __cls_kwargs__: a dict for class creation
    :param field_definitions: fields of the model (or extra fields if a base is supplied)
         in the format <name>=(<type>, <default default>) or <name>=<default value>, e.g. `foobar=(str, ...) or foobar=123, or, for complex use-cases, in the format <name>=<FieldInfo>, e.g. foo=Field(default_factory=datetime.utcnow, alias='bar')
    Params:
    __model_name – name of the created model
    __config__ – config class to use for the new model
    __base__ – base class for the new model to inherit from
    __module__ – module of the created model
    __validators__ – a dict of method names and @validator class methods
    __cls_kwargs__ – a dict for class creation
    field_definitions – fields of the model (or extra fields if a base is supplied) in the format ` =( ,  )` or ` = , e.g. `foobar=(str, ...)` or `foobar=123`, or, for complex use-cases, in the format ` = `, e.g. `foo=Field(default_factory=datetime.utcnow, alias='bar')`
    """
    kwargs["__base__"] == "TypeFields"
    dynamic_type_field_model = create_model(*args, **kwargs)
    return dynamic_type_field_model


validated_lookup_fields = (
    "user_id",
    "department_id",
    "location_id",
    "agent_id",
    "group_id",
)
"""Asset fields that can't be populated with mock data because they are used to lookup other objects."""
