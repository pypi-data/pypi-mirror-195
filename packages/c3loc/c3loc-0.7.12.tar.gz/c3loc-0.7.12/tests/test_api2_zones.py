import contextlib

from httpx import AsyncClient
import pytest
import sqlalchemy as sa

from c3loc.api2.main import app


@pytest.fixture
def delete_zone(client):
    async def _del(zone_id: int) -> None:
        await client.delete(f'/zones/{zone_id}')
    return _del


@pytest.fixture
def new_zone(client):
    async def _add(name: str = 'Test Zone') -> int:
        zone = {'name': name}
        response = await client.post('/zones', json=zone)
        assert 'Location' in response.headers
        new_id = int(response.headers['Location'].split('/')[-1])
        return new_id
    return _add


@contextlib.asynccontextmanager
async def temporary_zone(name: str = 'Test'):
    print("Creating Zone")
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/zones', json={
            'name': name})
    assert response.status_code == 201
    zone_id = int(response.headers['Location'].split('/')[-1])
    try:
        yield zone_id
    finally:
        print("Destroying Zone")
        async with AsyncClient(app=app, base_url='http://test') as client:
            await client.delete(f'/groups/{zone_id}')


# @pytest.fixture
# async def temporary_zone(client, new_zone, delete_zone):
#     zone_id = await new_zone()
#     yield zone_id
#     await delete_zone(zone_id)


@pytest.mark.asyncio
async def test_get_zones_null(client):
    response = await client.get("/zones")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_zone(client, db):
    zone = {'name': 'Test'}
    response = await client.post("/zones", json=zone)
    assert response.status_code == 201
    await db.execute(sa.text('delete from zones'))
    await db.commit()


@pytest.mark.asyncio
async def test_patch_zone(client):
    async with temporary_zone() as new_id:
        response = await client.patch(f'/zones/{new_id}', json={'name': 'farts'})
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_zone(client, new_zone):
    new_id = await new_zone()
    response = await client.delete(f'/zones/{new_id}')
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_bad_post_patch_zone(client):
    response = await client.post("/zones", json={})
    assert response.status_code == 422
    async with temporary_zone() as new_id:
        response = await client.patch(f"/zones/{new_id}", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_zone(client):
    async with temporary_zone() as new_id:
        response = await client.get(f'/zones/{new_id}')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_zones(client):
    async with temporary_zone() as new_id:
        response = await client.get(f'/zones')
    assert response.status_code == 200
    zones = response.json()
    assert len(zones) == 1
    assert zones[0]['id'] == new_id


@pytest.mark.asyncio
async def test_zones_404(client):
    response = await client.get('/zones/1000')
    assert response.status_code == 404
    response = await client.patch('/zones/1000', json={'name': 'farts'})
    assert response.status_code == 404
    response = await client.delete('/zones/1000')
    assert response.status_code == 404
