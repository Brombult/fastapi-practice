from fastapi import status


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.url.endswith("docs")
