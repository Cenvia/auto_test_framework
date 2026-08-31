import pytest
from api.client import ApiClient

def test_get_posts(api_client):
    """测试获取帖子"""
    resp = api_client.get("posts/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert "title" in data
    print(f"✅ API测试通过: {data['title']}")

def test_create_post(api_client):
    """测试创建帖子"""
    new_data = {"title": "Windows Test", "body": "Running on Windows 11", "userId": 1}
    resp = api_client.post("posts", json=new_data)
    assert resp.status_code == 201
    assert resp.json()["title"] == "Windows Test"