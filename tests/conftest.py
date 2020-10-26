import pytest

from fshelper import Credential


@pytest.fixture(scope="function")
def fake_credential(faker):
    username = faker.hexify(text="^^^^^^^^^^^^^")
    password = faker.hexify(text="^^^^^^^^^^^^^")
    credential = Credential(username, password)
    return credential


@pytest.fixture(scope="function")
def fake_fs_domain(faker):
    return faker.hexify(text="^^^^^^^^^^^")
