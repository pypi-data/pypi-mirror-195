import os

import aiohttp
import pytest
import pytest_asyncio
from aiohttp.client_exceptions import ClientConnectionError
from pytest import fixture

from aioairq import AirQ, DeviceInfo, InvalidAuth


@fixture
def ip():
    return os.environ["AIRQIP"]


@fixture
def mdns():
    return os.environ["AIRQMDNS"]


@fixture
def airq_id():
    return os.environ["AIRQID"]


@fixture
def passw():
    return os.environ["AIRQPASS"]


@pytest_asyncio.fixture
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.mark.asyncio
async def test_authentication(ip, passw, session):
    airq = AirQ(ip, passw, session)
    await airq.validate()


@pytest.mark.asyncio
async def test_connection_failure(ip, passw, session):
    wrong_ip = ".".join(reversed(ip.split(".")))  # must pass the validation
    airq = AirQ(wrong_ip, passw, session)
    with pytest.raises(ClientConnectionError):
        await airq.validate()


@pytest.mark.asyncio
async def test_authentication_failure(ip, passw, session):
    airq = AirQ(ip, "wrong" + passw, session)
    with pytest.raises(InvalidAuth):
        await airq.validate()


@pytest.fixture
def device_info_exp(airq_id):
    return DeviceInfo(
        id=airq_id,
        name=f"Device {airq_id[:5].upper()}",
        model="airQ Pro",
        suggested_area="Living Room",
        sw_version="1.20.2.r6_D_1.83.0-dev+1e23f",
        hw_version="D",
    )


@pytest.mark.asyncio
async def test_device_info(ip, passw, session, device_info_exp):
    airq = AirQ(ip, passw, session)
    device_info_obs = await airq.fetch_device_info()
    for field, value_obs in device_info_obs.items():
        assert value_obs == device_info_exp[field]


@pytest.mark.asyncio
async def test_get(ip, passw, session):
    airq = AirQ(ip, passw, session)
    for route in airq._supported_routes:
        await airq.get(route)
