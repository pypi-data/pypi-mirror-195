import contextlib
from datetime import datetime, timedelta
import uuid
from typing import Dict, Union

from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from hypothesis import given, strategies as st, settings
import pytest
import sqlalchemy as sa

from c3loc.api2.main import app
from c3loc.api2.schemas.tags import TagPatch, IBeacon, SecureSmartRelay
from c3loc.api2.schemas.sensors import SensorType
from c3loc.config import CONFIG
from c3loc.db_next import history, sensors

from .test_api2_groups import temporary_group
from .test_api2_zones import temporary_zone

@pytest.fixture
def delete_tag():
    async def _del(tag_id: int) -> None:
        async with AsyncClient(app=app, base_url='http://test') as client:
            await client.delete(f'/tags/{tag_id}')
    return _del


@pytest.fixture
def new_sr_tag():
    async def _add() -> int:
        async with AsyncClient(app=app, base_url='http://test') as client:
            response = await client.post('/tags', json={
                'mac': '00:00:00:00:00:00',
                'type': 'SmartRelay',
                'name': 'Test Tag'})
        assert response.status_code == 201
        tag_id = int(response.headers['Location'].split('/')[-1])
        return tag_id
    return _add


@contextlib.asynccontextmanager
async def temporary_sr_tag():
    print("Creating SR")
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/tags', json={
            'mac': '00:00:00:00:00:00',
            'type': 'SmartRelay',
            'name': 'Test Tag'})
    assert response.status_code == 201
    tag_id = int(response.headers['Location'].split('/')[-1])
    try:
        yield tag_id
    finally:
        print("Destroying SR")
        async with AsyncClient(app=app, base_url='http://test') as client:
            await client.delete(f'/tags/{tag_id}')


@pytest.fixture
async def mock_history(engine):
    async with engine.connect() as conn:
        async with temporary_zone() as zone_id:
            async with temporary_sr_tag() as tag_id:
                insert = history.insert().values({
                    'tag_id': tag_id,
                    'zone_id': zone_id,
                    'start_ts': datetime.utcnow(),
                    'distance': 0})
                r = await conn.execute(insert)
                hist_id = r.inserted_primary_key[0]
                await conn.commit()
                yield tag_id
                await conn.execute(
                    history.delete().where(history.c.id == hist_id))
                await conn.commit()


@pytest.fixture
async def mock_contact(engine):
    async with engine.connect() as conn:
        async with temporary_sr_tag() as main_tag:
            async with temporary_zone() as zone_id:
                insert = history.insert().values({
                    'tag_id': main_tag,
                    'zone_id': zone_id,
                    'start_ts': datetime.utcnow(),
                    'distance': 0,
                    'zone_name': 'Farts'})
                await conn.execute(insert)
                async with temporary_sr_tag() as other_tag:
                    insert = history.insert().values({
                        'tag_id': other_tag,
                        'zone_id': zone_id,
                        'start_ts': datetime.utcnow(),
                        'distance': 0,
                        'zone_name': "Farts"})
                    await conn.execute(insert)
                    await conn.commit()
                    yield main_tag, other_tag
                    await conn.execute(history.delete())
                    await conn.commit()


@pytest.fixture
async def mock_no_contact(engine):
    async with engine.connect() as conn:
        async with temporary_sr_tag() as main_tag:
            async with temporary_zone() as zone_id:
                insert = history.insert().values({
                    'tag_id': main_tag,
                    'zone_id': zone_id,
                    'start_ts': datetime.utcnow()-timedelta(
                        minutes=10),
                    'end_ts': datetime.utcnow()-timedelta(
                        minutes=5),
                    'distance': 0,
                    'zone_name': 'Farts'})
                await conn.execute(insert)
                async with temporary_sr_tag() as other_tag:
                    insert = history.insert().values({
                        'tag_id': other_tag,
                        'zone_id': zone_id,
                        'start_ts': datetime.utcnow(),
                        'distance': 0,
                        'zone_name': "Farts"})
                    await conn.execute(insert)
                    await conn.commit()
                    yield main_tag, other_tag
                    await conn.execute(history.delete())
                    await conn.commit()


@pytest.fixture
async def mock_sensor(engine):
    async with engine.connect() as conn:
        async with temporary_sr_tag() as tag_id:
            insert = sensors.insert().values({
                'tag_id': tag_id,
                'type': SensorType.SensorTempData,
                'value': b'\x00'})
            r = await conn.execute(insert)
            sensor_id = r.inserted_primary_key[0]
            await conn.commit()
            yield tag_id
            await conn.execute(
                sensors.delete().where(sensors.c.id == sensor_id))
            await conn.commit()


@pytest.mark.asyncio
async def test_get_contacts(mock_contact, client):
    main_tag, other_tag = mock_contact
    response = await client.get(f'/tags/{main_tag}/contacts')
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]['tag_id'] == other_tag

    response = await client.get(f'/tags/{main_tag}/contacts?offset=1')
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = await client.get(f'/tags/{main_tag}/contacts?limit=0')
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_get_contacts_exclude_non_contact(mock_no_contact, client):
    main_tag, other_tag = mock_no_contact
    response = await client.get(f'/tags/{main_tag}/contacts')
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 0


@pytest.mark.asyncio
async def test_get_contacts_404(client):
    response = await client.get(f'/tags/1000/contacts')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_contacts_time_filter(client, mock_contact):
    main_tag, _ = mock_contact
    response = await client.get(
            f'/tags/{main_tag}/contacts?start={datetime.utcnow().isoformat()}'
            f'&end={datetime.utcnow().isoformat()}')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_history(mock_history, client):
    new_id = mock_history
    response = await client.get(f'/tags/{new_id}/history')
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = await client.get(f'/tags/{new_id}/history?offset=1')
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = await client.get(f'/tags/{new_id}/history?limit=0')
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_get_history_404(client):
    response = await client.get(f'/tags/1000/history')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_history_time_filter(client):
    async with temporary_sr_tag() as tag_id:
        response = await client.get(
            f'/tags/{tag_id}/history?start={datetime.utcnow().isoformat()}'
            f'&end={datetime.utcnow().isoformat()}')
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_history_time_filter(client):
    async with temporary_sr_tag() as tag_id:
        response = await client.get(
            f'/tags/{tag_id}/history?start={datetime.utcnow().isoformat()}'
            f'&end={datetime.utcnow().isoformat()}')
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_history_time_filter_bad_iso(client):
    async with temporary_sr_tag() as tag_id:
        response = await client.get(f'/tags/{tag_id}/history?start=11')
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_tags_null(client):
    response = await client.get("/tags")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_tags(client):
    async with temporary_sr_tag() as tag_id:
        response = await client.get(f'/tags')
        assert response.status_code == 200
        ts = response.json()
        assert len(ts) == 1
        assert ts[0]['id'] == tag_id

        response = await client.get('/tags?offset=1')
        assert response.status_code == 200
        ts = response.json()
        assert len(ts) == 0

        response = await client.get('/tags?limit=0')
        assert response.status_code == 200
        ts = response.json()
        assert len(ts) == 0


@pytest.mark.asyncio
async def test_tags_filter_type():
    async with temporary_sr_tag() as new_id:
        async with AsyncClient(app=app, base_url='http://test') as client:
            response = await client.get('/tags?type=SmartRelay')
            assert response.status_code == 200
            assert response.json()[0]['id'] == new_id

            response = await client.get('/tags?type=iBeacon')
            print('Response', response.json())
            assert response.status_code == 200
            assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_tags_filter_group():
    async with temporary_group() as group_id:
        async with temporary_sr_tag() as new_id:
            async with AsyncClient(app=app, base_url='http://test') as client:
                response = await client.patch(f'/tags/{new_id}', json={
                    'group_id': group_id
                })
                assert response.status_code == 204

                response = await client.get(f'/tags?group_id={group_id}')
                assert response.status_code == 200
                assert response.json()[0]['id'] == new_id

                response = await client.get(f'/tags?group_id={group_id+1}')
                assert response.status_code == 200
                assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_delete(new_sr_tag, client):
    new_id = await new_sr_tag()
    response = await client.delete(f'/tags/{new_id}')
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_tags_post_bad_no_type(client):
    tag = {'name': 'Test', 'mac': '00:00:00:00:00:00'}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_sr_bad_id_null(client):
    tag = {'name': 'Test', 'type': 'SmartRelay'}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_sr_bad_id_bid(client):
    tag = {'name': 'Test', 'type': 'SmartRelay', 'bid': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_sr_bad_id_uuid(client):
    tag = {'name': 'Test', 'type': 'SmartRelay',
           'uuid': 'f03b1170-9f91-4e10-b640-136d317d3228',
           'major': 0, 'minor': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_sr_bad_id_bid_out_of_range(client):
    tag = {'name': 'Test', 'type': 'SmartRelay',
           'bid': 2**32}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422

    tag = {'name': 'Test', 'type': 'SmartRelay',
           'bid': -1}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_sr_bad_mac(client):
    tag = {'name': 'Test', 'type': 'SmartRelay', 'mac': '00:00'}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_sr_default_name(client):
    tag = {'type': 'SmartRelay', 'mac': '00:00:00:00:00:00'}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 201
    new_id = int(response.headers['Location'].split('/')[-1])
    response = await client.get(f'/tags/{new_id}')
    assert response.status_code == 200
    name = response.json()['name']
    assert name


def format_mac(mac_bytes: bytes) -> str:
    return ':'.join([f'{x:02x}' for x in range(len(mac_bytes))])


@given(name=st.text(alphabet=st.characters(blacklist_categories=('Cc', 'Cs'))),
       mac_addr=st.builds(format_mac, st.binary(min_size=6, max_size=6)),
       attribs=st.one_of(
           st.none(),
           st.from_type(Dict[str, Union[str, int]])))
@settings(deadline=None)
@pytest.mark.asyncio
async def test_post_sr(name, mac_addr, attribs, engine):
    async with temporary_group() as group_id:
        async with temporary_zone() as zone_id:
            async with AsyncClient(app=app, base_url='http://test') as client:
                response = await client.post("/tags", json={
                    'name': name,
                    'mac': mac_addr,
                    'type': 'SmartRelay',
                    'attributes': attribs,
                    'group_id': group_id,
                    'zone_id': zone_id
                })
            assert response.status_code == 201
            async with engine.connect() as conn:
                await conn.execute(sa.text('delete from tags'))
                await conn.commit()


@pytest.mark.asyncio
async def test_tags_post_ssr_bad_id_null(client):
    tag = {'name': 'Test', 'type': 'SecureSmartRelay'}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_ssr_bad_id_mac(client):
    tag = {'name': 'Test', 'type': 'SecureSmartRelay',
           'mac': '00:00:00:00:00:00'}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_ssr_bad_id_uuid(client):
    tag = {'name': 'Test', 'type': 'SecureSmartRelay',
           'uuid': 'f03b1170-9f91-4e10-b640-136d317d3228',
           'major': 0, 'minor': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_ssr_bad_bid(client):
    tag = {'name': 'Test', 'type': 'SecureSmartRelay', 'bid': 2**32}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422

    tag = {'name': 'Test', 'type': 'SecureSmartRelay', 'bid': -1}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_ssr_default_name(client):
    tag = {'type': 'SecureSmartRelay', 'bid': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 201
    new_id = int(response.headers['Location'].split('/')[-1])
    response = await client.get(f'/tags/{new_id}')
    assert response.status_code == 200
    name = response.json()['name']
    assert name


@given(ssr=st.builds(SecureSmartRelay))
@settings(deadline=None)
@pytest.mark.asyncio
async def test_post_ssr(ssr, engine):
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/tags", json=ssr.dict())
    assert response.status_code == 201
    async with engine.connect() as conn:
        await conn.execute(sa.text('delete from tags'))


@pytest.mark.asyncio
async def test_tags_post_ib_bad_id_null(client):
    tag = {'name': 'Test', 'type': 'iBeacon'}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_ib_bad_id_mac(client):
    tag = {'name': 'Test', 'type': 'iBeacon',
           'mac': '00:00:00:00:00:00'}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_ib_bad_id_bid(client):
    tag = {'name': 'Test', 'type': 'iBeacon', 'bid': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_ib_bad_id_bad_major(client):
    tag = {'name': 'Test', 'type': 'iBeacon',
           'uuid': str(uuid.uuid4()), 'major': 2**16, 'minor': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422

    tag = {'name': 'Test', 'type': 'iBeacon',
           'uuid': str(uuid.uuid4()), 'major': -1, 'minor': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_ib_bad_id_bad_minor(client):
    tag = {'name': 'Test', 'type': 'iBeacon',
           'uuid': str(uuid.uuid4()), 'major': 0, 'minor': 2**16}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422

    tag = {'name': 'Test', 'type': 'iBeacon',
           'uuid': str(uuid.uuid4()), 'major': 0, 'minor': -1}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_ib_bad_uuid(client):
    tag = {'name': 'Test', 'type': 'iBeacon',
     'uuid': 'f03b1170-9f91', 'major': 0, 'minor': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_ib_missing_major(client):
    tag = {'name': 'Test', 'type': 'iBeacon',
           'uuid': 'f03b1170-9f91-4e10-b640-136d317d3228',
           'minor': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_post_ib_missing_minor(client):
    tag = {'name': 'Test', 'type': 'iBeacon',
           'uuid': 'f03b1170-9f91-4e10-b640-136d317d3228',
           'major': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tags_ib_default_name(client):
    tag = {'type': 'iBeacon',
           'uuid': 'f03b1170-9f91-4e10-b640-136d317d3228',
           'major': 0, 'minor': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 201
    new_id = int(response.headers['Location'].split('/')[-1])
    response = await client.get(f'/tags/{new_id}')
    assert response.status_code == 200
    name = response.json()['name']
    assert name


@pytest.mark.asyncio
async def test_tags_la_default_name(client):
    tag = {'type': 'iBeacon',
           'uuid': str(CONFIG['LA_UUID']),
           'major': 0, 'minor': 0}
    response = await client.post("/tags", json=tag)
    assert response.status_code == 201
    new_id = int(response.headers['Location'].split('/')[-1])
    response = await client.get(f'/tags/{new_id}')
    assert response.status_code == 200
    name = response.json()['name']
    assert name


@given(ib=st.builds(IBeacon))
@settings(report_multiple_bugs=False, deadline=None)
@pytest.mark.asyncio
async def test_post_ib(ib, engine):
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post("/tags", json=jsonable_encoder(ib))
        assert response.status_code == 201
    async with engine.connect() as conn:
        await conn.execute(sa.text('delete from tags'))


@given(patch=st.builds(TagPatch))
@pytest.mark.asyncio
async def test_patch_tag(patch):
    async with temporary_sr_tag() as new_id:
        async with AsyncClient(app=app, base_url='http://test') as client:
            response = await client.patch(f'/tags/{new_id}', json=patch.dict())
            assert response.status_code == 204
            response = await client.get(f'/tags/{new_id}')
            assert response.status_code == 200
            body = response.json()
            for k, v in patch.dict().items():
                assert body[k] == patch.dict()[k]


@pytest.mark.asyncio
async def test_tags_404(client):
    response = await client.get('/tags/1000')
    assert response.status_code == 404
    response = await client.patch('/tags/1000', json={'name': 'farts'})
    assert response.status_code == 404
    response = await client.delete('/tags/1000')
    assert response.status_code == 404
