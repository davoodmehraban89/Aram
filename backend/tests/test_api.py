def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_read_only_schema_catalog(client):
    entities = client.get("/api/v1/schema/entities")
    assert entities.status_code == 200
    assert len(entities.json()["entities"]) == 9
    assert client.post("/api/v1/schema/entities").status_code == 405


def test_enum_catalog(client):
    response = client.get("/api/v1/schema/enums")
    assert response.json()["fiscal_year_statuses"] == ["Draft", "Approved", "Locked"]
    assert response.json()["statement_types"] == ["BS", "IS", "CF", "EQ"]

