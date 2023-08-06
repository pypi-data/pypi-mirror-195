import pytest

from .test_api2_tags import temporary_sr_tag
from .test_api2_groups import temporary_group


@pytest.mark.asyncio
async def test_get_proximity_null(client):
    response = await client.get("/proximity")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_proximity(client):
    async with temporary_sr_tag() as tag_id:
        response = await client.get(f'/proximity')
        assert response.status_code == 200
        ls = response.json()
        assert len(ls) == 1

        response = await client.get('/proximity?offset=1')
        assert response.status_code == 200
        ls = response.json()
        assert len(ls) == 0

        response = await client.get('/listeners?limit=0')
        assert response.status_code == 200
        ls = response.json()
        assert len(ls) == 0


@pytest.mark.asyncio
async def test_proximity_filter_type(client):
    async with temporary_sr_tag() as new_id:
        response = await client.get('/proximity?type=SmartRelay')
        assert response.status_code == 200
        assert response.json()[0]['tag_id'] == new_id

        response = await client.get('/proximity?type=iBeacon')
        print('Response', response.json())
        assert response.status_code == 200
        assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_tags_filter_group(client):
    async with temporary_group() as group_id:
        async with temporary_sr_tag() as new_id:
            response = await client.patch(f'/tags/{new_id}', json={
                'group_id': group_id
            })
            assert response.status_code == 204

            response = await client.get(f'/proximity?group_id={group_id}')
            assert response.status_code == 200
            assert response.json()[0]['tag_id'] == new_id

            response = await client.get(f'/proximity?group_id={group_id+1}')
            assert response.status_code == 200
            assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_get_proximity_xml(client):
    async with temporary_sr_tag() as tag_id:
        response = await client.get(f'/proximity.xml')
        assert response.status_code == 200
        assert 'Content-Type' in response.headers
        assert response.headers['Content-Type'] == 'text/xml'
        assert len(response.text) > 20
