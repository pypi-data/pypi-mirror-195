import contextlib

from httpx import AsyncClient
import pytest
import sqlalchemy as sa

from c3loc.api2.main import app


@pytest.fixture
def delete_group(client):
    async def _del(group_id: int) -> None:
        await client.delete(f'/groups/{group_id}')
    return _del


@pytest.fixture
def new_group(client):
    async def _add(name: str = 'Test Group') -> int:
        group = {'name': name}
        response = await client.post('/groups', json=group)
        assert 'Location' in response.headers
        new_id = int(response.headers['Location'].split('/')[-1])
        return new_id
    return _add


@contextlib.asynccontextmanager
async def temporary_group(name: str = 'Test'):
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/groups', json={
            'name': name})
    assert response.status_code == 201
    group_id = int(response.headers['Location'].split('/')[-1])
    print("Created Group: ", group_id)
    try:
        yield group_id
    finally:
        print("Destroying Group: ", group_id)
        async with AsyncClient(app=app, base_url='http://test') as client:
            await client.delete(f'/groups/{group_id}')


# @pytest.fixture
# async def temporary_group(new_group, delete_group):
#     group_id = await new_group()
#     yield group_id
#     await delete_group(group_id)


@pytest.mark.asyncio
async def test_get_groups_null(client):
    response = await client.get("/groups")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_group(client, db):
    group = {'name': 'Farts'}
    response = await client.post("/groups", json=group)
    assert response.status_code == 201
    await db.execute(sa.text('delete from groups'))


@pytest.mark.asyncio
async def test_patch_group(client):
    async with temporary_group() as new_id:
        response = await client.patch(f'/groups/{new_id}', json={'name': 'farts'})
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_group(client, new_group):
    new_id = await new_group()
    response = await client.delete(f'/groups/{new_id}')
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_bad_post_patch_group(client):
    response = await client.post("/groups", json={})
    assert response.status_code == 422
    async with temporary_group() as new_id:
        response = await client.patch(f"/groups/{new_id}", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_group(client):
    async with temporary_group() as group_id:
        response = await client.get(f'/groups/{group_id}')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_groups(client):
    async with temporary_group() as group_id:
        response = await client.get(f'/groups')
        assert response.status_code == 200
        groups = response.json()
        assert len(groups) == 1
        assert groups[0]['id'] == group_id

        response = await client.get('/groups?offset=1')
        assert response.status_code == 200
        als = response.json()
        assert len(als) == 0

        response = await client.get('/groups?limit=0')
        assert response.status_code == 200
        als = response.json()
        assert len(als) == 0


@pytest.mark.asyncio
async def test_groups_404(client):
    response = await client.get('/groups/1000')
    assert response.status_code == 404
    response = await client.patch('/groups/1000', json={'name': 'farts'})
    assert response.status_code == 404
    response = await client.delete('/groups/1000')
    assert response.status_code == 404
