from random import choice

from fshelper.models.asset import AssetCreation
from pydantic_factories import ModelFactory, Use


class CreateAssetFactory(ModelFactory):
    """Factory class to construct an asset represented as JSON for use when creating an asset through the API.

    https://api.freshservice.com/#create_an_asset
    """

    __model__ = AssetCreation

    impact = Use(choice, ("low", "medium", "high"))
    usage_type = Use(choice, ("permanent", "loaner"))
