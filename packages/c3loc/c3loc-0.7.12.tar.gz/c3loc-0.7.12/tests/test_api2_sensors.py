import contextlib
from typing import Tuple

import pytest
from httpx import AsyncClient
from hypothesis import given, settings, strategies as st

from c3loc.api2.main import app
from c3loc.api2.schemas.types import SensorType
from c3loc.db_next import sensors

from .conftest import get_engine
from .test_api2_tags import temporary_sr_tag


@pytest.fixture
async def add_sensor(engine):
    add_sensor.ids = set()
    async def f(t_id: int, t: SensorType, v: bytes) -> None:
        async with engine.connect() as conn:
            insert = sensors.insert().values({
                'tag_id': t_id,
                'type': t,
                'value': v,
                'device_ts': 0})
            r = await conn.execute(insert)
            add_sensor.ids.add(r.inserted_primary_key[0])
            await conn.commit()
    yield f


@pytest.mark.asyncio
async def test_dont_barf_on_unk_sensor_type(add_sensor, client, engine):
    async with temporary_sr_tag() as tag_id:
        await add_sensor(tag_id, 254, b'\x00')
        try:
            response = await client.get('/sensors')
            assert response.status_code == 200
            assert len(response.json()) == 0
        finally:
            async with engine.connect() as conn:
                await conn.execute(sensors.delete())
                await conn.commit()


@pytest.mark.asyncio
async def test_only_latest_sensor(add_sensor, client, engine):
    async with temporary_sr_tag() as tag_id:
        await add_sensor(tag_id, SensorType.SensorDataHumid, b'\x00')
        await add_sensor(tag_id, SensorType.SensorDataHumid, b'\x01')
        try:
            response = await client.get('/sensors')
            assert response.status_code == 200
            assert len(response.json()) == 1
            assert response.json()[0]['value'] == 1
        finally:
            async with engine.connect() as conn:
                await conn.execute(sensors.delete())
                await conn.commit()


@contextlib.asynccontextmanager
async def mock_sensor(typ: int = SensorType.SensorDataTemp,
                      value: bytes = b'\x00'):
    async with get_engine().connect() as conn:
        async with temporary_sr_tag() as tag_id:
            insert = sensors.insert().values({
                'tag_id': tag_id,
                'type': typ,
                'value': value,
                'device_ts': 0})
            r = await conn.execute(insert)
            sensor_id = r.inserted_primary_key[0]
            await conn.commit()
            try:
                yield tag_id
            finally:
                await conn.execute(sensors.delete().where(
                    sensors.c.id == sensor_id))
                await conn.commit()


@pytest.mark.asyncio
async def test_get_sensors_null(client):
    response = await client.get("/sensors")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_sensors(client):
    async with mock_sensor() as tag_id:
        response = await client.get(f'/sensors')
        assert response.status_code == 200
        ls = response.json()
        assert len(ls) == 1
        assert ls[0]['tag_id'] == tag_id

        response = await client.get('/proximity?offset=1')
        assert response.status_code == 200
        ls = response.json()
        assert len(ls) == 0

        response = await client.get('/listeners?limit=0')
        assert response.status_code == 200
        ls = response.json()
        assert len(ls) == 0


def make_raw_temp(temp: int) -> Tuple[int, bytes]:
    if temp > 2**7-1 or temp < -2**7:
        return temp, temp.to_bytes(2, 'little', signed=True)
    return temp, temp.to_bytes(1, 'little', signed=True)


@given(temp=st.builds(
    make_raw_temp, st.integers(min_value=-2732, max_value=2**15-1)))
@settings(report_multiple_bugs=False, deadline=None)
@pytest.mark.asyncio
async def test_sensors_temp(temp: Tuple[int, bytes]):
    target, raw_val = temp
    target = round(target / 10.0, 1)
    async with mock_sensor(SensorType.SensorDataTemp, raw_val) as tag_id:
        async with AsyncClient(app=app, base_url='http://test') as client:
            response = await client.get('/sensors/')
        assert response.status_code == 200
        assert response.json()[0]['value'] == target


def make_raw_humid(humid: int) -> bytes:
    return humid.to_bytes(1, 'little', signed=False)


@given(humid=st.builds(
    make_raw_humid, st.integers(min_value=0, max_value=100)))
@settings(report_multiple_bugs=False, deadline=None)
@pytest.mark.asyncio
async def test_sensors_humid(humid: bytes):
    target = int.from_bytes(humid, 'little', signed=False)
    async with mock_sensor(SensorType.SensorDataHumid, humid) as tag_id:
        async with AsyncClient(app=app, base_url='http://test') as client:
            response = await client.get('/sensors/')
        assert response.status_code == 200
        assert response.json()[0]['value'] == target


# @pytest.mark.asyncio
# async def test_proximity_filter_type(client):
#     async with temporary_sr_tag() as new_id:
#         response = await client.get('/proximity?type=SmartRelay')
#         assert response.status_code == 200
#         assert response.json()[0]['tag_id'] == new_id
#
#         response = await client.get('/proximity?type=iBeacon')
#         print('Response', response.json())
#         assert response.status_code == 200
#         assert len(response.json()) == 0
