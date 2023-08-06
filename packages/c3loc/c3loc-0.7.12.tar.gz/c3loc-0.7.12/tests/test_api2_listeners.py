import pytest
import sqlalchemy as sa

from c3loc.db_next import listeners


@pytest.fixture
async def temporary_listener(engine):
    async with engine.connect() as conn:
        r = await conn.execute(
            listeners.insert().values({'id': 'aabbccddeeff',
                                       'attrs': {},
                                       'name': 'farts'}))
        await conn.commit()
        listener_id = r.inserted_primary_key[0]
    yield listener_id
    async with engine.connect() as conn:
        await conn.execute(
            listeners.delete().where(listeners.c.id == listener_id))
        await conn.commit()


@pytest.mark.asyncio
async def test_get_listeners_null(client):
    response = await client.get("/listeners")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_listener_default_name(client, engine):
    async with engine.connect() as conn:
        r = await conn.execute(
            listeners.insert().values({'id': 'aabbccddeeff',
                                       'attrs': {}}))
        await conn.commit()
        new_id = r.inserted_primary_key[0]

        resp = await client.get(f'/listeners/{new_id}')
        assert resp.status_code == 200
        assert resp.json()['name']


@pytest.mark.asyncio
async def test_patch_listener(client, temporary_listener):
    new_id = temporary_listener
    response = await client.patch(f'/listeners/{new_id}', json={'name': 'farts'})
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_bad_patch_listener(client, temporary_listener):
    new_id = temporary_listener
    response = await client.patch(f"/listeners/{new_id}", json={'attrs': 1})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_listener(client, temporary_listener):
    listener_id = temporary_listener
    response = await client.get(f'/listeners/{listener_id}')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_listeners(client, temporary_listener):
    listener_id = temporary_listener
    response = await client.get(f'/listeners')
    assert response.status_code == 200
    ls = response.json()
    assert len(ls) == 1
    assert ls[0]['id'] == listener_id

    response = await client.get('/listeners?offset=1')
    assert response.status_code == 200
    ls = response.json()
    assert len(ls) == 0

    response = await client.get('/listeners?limit=0')
    assert response.status_code == 200
    ls = response.json()
    assert len(ls) == 0


@pytest.mark.asyncio
async def test_listeners_404(client):
    response = await client.get('/listeners/1000')
    assert response.status_code == 404
    response = await client.patch('/listeners/1000', json={'name':'farts'})
    assert response.status_code == 404
