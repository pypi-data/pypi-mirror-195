import pytest
import sqlalchemy as sa

from c3loc.db_next import alarms
from .test_api2_tags import new_sr_tag, delete_tag


@pytest.fixture
def delete_alarm(db, delete_tag):
    async def _del(alarm_id: int) -> None:
        result = await db.execute(sa.select(alarms.c.tag_id).where(
            alarms.c.id == alarm_id))
        tag_id = result.scalar()
        await db.execute(
            alarms.delete().where(alarms.c.id == alarm_id))
        await db.commit()
        await delete_tag(tag_id)
    return _del


@pytest.fixture
def new_alarm(db, new_sr_tag):
    async def _add() -> int:
        tag_id = await new_sr_tag()
        result = await db.execute(alarms.insert().values({
            'tag_id': tag_id
        }))
        new_id = result.inserted_primary_key[0]
        await db.commit()
        return new_id
    return _add


@pytest.fixture
async def temporary_alarm(db, new_alarm, delete_alarm):
    alarm_id = await new_alarm()
    yield alarm_id
    await delete_alarm(alarm_id)


@pytest.mark.asyncio
async def test_get_alarms_null(client):
    response = await client.get("/alarms")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_patch_alarm(client, temporary_alarm):
    new_id = temporary_alarm
    response = await client.patch(f'/alarms/{new_id}',
                                  json={'acknowledged': True})
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_bad_patch_alarm(client, temporary_alarm):
    new_id = temporary_alarm
    response = await client.patch(f"/alarms/{new_id}", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_alarm(db, client, temporary_alarm):
    alarm_id = temporary_alarm
    response = await client.get(f'/alarms/{alarm_id}')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_alarms(client, temporary_alarm):
    alarm_id = temporary_alarm
    response = await client.get('/alarms')
    assert response.status_code == 200
    als = response.json()
    assert len(als) == 1
    assert als[0]['id'] == alarm_id

    response = await client.get('/alarms?offset=1')
    assert response.status_code == 200
    als = response.json()
    assert len(als) == 0

    response = await client.get('/alarms?limit=0')
    assert response.status_code == 200
    als = response.json()
    assert len(als) == 0


@pytest.mark.asyncio
async def test_alarms_404(client):
    response = await client.get('/alarms/1000')
    assert response.status_code == 404
    response = await client.patch('/alarms/1000', json={'acknowledged': True})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_alarms_no_post(client):
    response = await client.post('/alarms', json={})
    assert response.status_code == 405
