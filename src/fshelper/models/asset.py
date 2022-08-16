from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel


class Asset(BaseModel):
    """Model for the data returned from the FS API.

    https://api.freshservice.com/#asset_attributes
    type_fields will be a dict, but the keys will be different from account to account.  They include an
    identifier in the key that seems to be related to the account but generated when custom fields are
    added.  Therefore, it's not defined with a separate model because we can't know the identifier
    beforehand.
    """

    id: Optional[int] = None
    display_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    asset_type_id: int
    impact: Optional[str] = None
    author_type: Optional[str] = None
    usage_type: Optional[str] = None
    asset_tag: Optional[str] = None
    user_id: Optional[int] = None
    department_id: Optional[int] = None
    location_id: Optional[int] = None
    agent_id: Optional[int] = None
    group_id: Optional[int] = None
    assigned_on: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    type_fields: Optional[Dict]
