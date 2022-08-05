import os

import pytest

from src.fshelper import (
    Credential,
    RequestService,
    AssetsEndPoint,
)


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


@pytest.mark.skip
def test_create_asset(fs_credential_and_domain):
    credential, domain = fs_credential_and_domain
    with RequestService(credential, domain) as fs_req_service:
        asset_endpoint = AssetsEndPoint(fs_req_service)
        response = asset_endpoint.create()
    pass
