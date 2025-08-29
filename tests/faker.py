import pytest_asyncio
from faker import Faker


@pytest_asyncio.fixture
def faker():
    return Faker()
