from random import choice

import factory
from fshelper.models.asset import Asset
from pydantic_factories import ModelFactory, Use


class AssetFactory(factory.Factory):
    """Factory class to construct an asset.

    https://api.freshservice.com/#create_an_asset
    """
    class Meta:
        model = Asset

    id = factory.Faker("pyint")
    display_id = factory.Faker("pyint")
    name = factory.Faker("pystr")
    description = factory.Faker("sentence")
    impact = factory.Faker("random_choices", elements=("low", "medium", "high"))
    author_type = factory.Faker("random_choices", elements=("Discovery Agent", "Discovery Probe", "User"))
    usage_type = factory.Faker("random_choices", elements=("permanent", "loaner"))
    asset_tag = factory.Faker("pystr")
    user_id = factory.Faker("pyint")
    department_id = factory.Faker("pyint")
    location_id = factory.Faker("pyint")
    agent_id = factory.Faker("pyint")
    group_id = factory.Faker("pyint")
    assigned_on = factory.Faker("date_time")
    created_at = factory.Faker("date_time")
    updated_at = factory.Faker("date_time")
    type_fields = factory.Faker("pydict")


class PydanticAssetFactory(ModelFactory):
    """Factory class to construct an asset represented as JSON for use on an Azure storage queue.

    https://api.freshservice.com/#create_an_asset
    """
    __model__ = Asset

    impact = Use(choice, ("low", "medium", "high"))
    author_type = Use(choice, ("Discovery Agent", "Discovery Probe", "User"))
    usage_type = Use(choice, ("permanent", "loaner"))
