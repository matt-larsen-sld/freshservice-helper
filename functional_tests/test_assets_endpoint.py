import os
from random import randint
from typing import Dict

import pytest

from src.fshelper import (
    Credential,
    RequestService,
    AssetsEndPoint,
)


@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return randint(111, 999)


@pytest.fixture
def fs_fake_laptop(faker) -> Dict:
    name = faker.pystr(10, 12)
    data = {
        "name": name,
        "asset_type_id": 11000293288,  # laptop type ID
        "description": faker.sentence(),
        "impact": "low",
        "asset_tag": f"TEST-{name}",
        "type_fields": {
            "product_11000293266": 11000010554,
            "asset_state_11000293266": "Sold",
        }
    }
    # TODO: type_fields.product_... and type_fields.asset_state_... creates lock in to our tenant.
    return data


@pytest.fixture
def fs_credential_and_domain():
    username = os.getenv("FreshServiceUsername")
    domain = os.getenv("FreshServiceDomain")
    credential = Credential(username, password="X")
    return credential, domain


@pytest.mark.slow
def test_get_all_assets(fs_credential_and_domain):
    credential, domain = fs_credential_and_domain
    with RequestService(credential, domain) as fs_req_service:
        assets_endpoint = AssetsEndPoint(fs_req_service)
        all_assets = []
        for assets in assets_endpoint.get_all(query="include=type_fields"):
            all_assets.extend(assets)
    assert len(all_assets) > 0


def test_get_single_asset(fs_credential_and_domain):
    credential, domain = fs_credential_and_domain
    with RequestService(credential, domain) as fs_req_service:
        asset_endpoint = AssetsEndPoint(fs_req_service)
        asset = asset_endpoint.get(1)
    assert asset["asset"]["display_id"] == 1


def test_create_delete_asset(fs_credential_and_domain, fs_fake_laptop):
    credential, domain = fs_credential_and_domain
    with RequestService(credential, domain) as fs_req_service:
        asset_endpoint = AssetsEndPoint(fs_req_service)
        response = asset_endpoint.create(fs_fake_laptop, enabled=True)
        assert response["asset"].get("name") == fs_fake_laptop.get("name")
        delete_response = asset_endpoint.delete(response["asset"].get("display_id"), permanently=True)
        assert delete_response is not None


def test_update_asset(fs_credential_and_domain, fs_fake_laptop):
    credential, domain = fs_credential_and_domain
    with RequestService(credential, domain) as fs_req_service:
        asset_endpoint = AssetsEndPoint(fs_req_service)
        create_response = asset_endpoint.create(fs_fake_laptop, enabled=True)
        update_data = {}
        update_response = asset_endpoint.update(create_response["asset"].get("display_id"), update_data)

